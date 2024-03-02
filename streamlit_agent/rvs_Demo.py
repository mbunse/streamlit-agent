import os
from pathlib import Path

import streamlit as st

from langchain import hub
from langchain.agents import AgentExecutor, Tool, create_react_agent
from langchain.chains import LLMMathChain
from langchain_community.callbacks import StreamlitCallbackHandler
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper, SQLDatabase
from langchain_core.runnables import RunnableConfig
from langchain_experimental.sql import SQLDatabaseChain
from langchain_openai import OpenAI
from sqlalchemy import create_engine
import sqlite3

from streamlit_agent.callbacks.capturing_callback_handler import playback_callbacks
from streamlit_agent.clear_results import with_clear_container

DB_PATH = (Path(__file__).parent / "Chinook.db").absolute()

SAVED_SESSIONS = {
    "Who is Leo DiCaprio's girlfriend? What is her current age raised to the 0.43 power?": "leo.pickle",
    "What is the full name of the female artist who recently released an album called "
    "'The Storm Before the Calm' and are they in the FooBar database? If so, what albums of theirs "
    "are in the FooBar database?": "alanis.pickle",
}

st.set_page_config(
    page_title="MRKL", page_icon="🦜", layout="wide", initial_sidebar_state="collapsed"
)

"# 🦜🔗 RV Salzburg Demo 2"

openai_api_key = os.getenv("OPENAI_API_KEY", "not_supplied")
enable_custom = True

# Tools setup
llm = OpenAI(temperature=0, openai_api_key=openai_api_key, streaming=True)
search = DuckDuckGoSearchAPIWrapper(region="at-de")
llm_math_chain = LLMMathChain.from_llm(llm)

# Make the DB connection read-only to reduce risk of injection attacks
# See: https://python.langchain.com/docs/security
creator = lambda: sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
db = SQLDatabase(create_engine("sqlite:///", creator=creator))

db_chain = SQLDatabaseChain.from_llm(llm, db)
tools = [
    Tool(
        name="Search",
        func=search.run,
        description="nützlich, wenn Sie Fragen zu aktuellen Ereignissen beantworten müssen. Sie sollten gezielte Fragen stellen",
    ),
    Tool(
        name="Calculator",
        func=llm_math_chain.run,
        description="nützlich, wenn Sie Fragen zur Mathematik beantworten müssen",
    ),
    Tool(
        name="FooBar DB",
        func=db_chain.run,
        description="nützlich, wenn Sie Fragen zu FooBar beantworten müssen. Die Eingabe sollte in Form einer Frage mit vollständigem Kontext erfolgen",
    ),
]

# Initialize agent
# english hwchase17/react, see https://smith.langchain.com/hub/johannhartmann/german-react?organizationId=28e5b177-3196-509d-8304-0dee6e834c0a
react_agent = create_react_agent(llm, tools, hub.pull("johannhartmann/german-react"))
mrkl = AgentExecutor(agent=react_agent, tools=tools)

with st.form(key="form"):
    if enable_custom:
        user_input = st.text_input("Stelle eine Frage")
    submit_clicked = st.form_submit_button("senden")

output_container = st.empty()
if with_clear_container(submit_clicked):
    output_container = output_container.container()
    output_container.chat_message("user").write(user_input)

    answer_container = output_container.chat_message("assistant", avatar="🦜")
    st_callback = StreamlitCallbackHandler(answer_container)
    cfg = RunnableConfig()
    cfg["callbacks"] = [st_callback]

    # If we've saved this question, play it back instead of actually running LangChain
    # (so that we don't exhaust our API calls unnecessarily)
    if user_input in SAVED_SESSIONS:
        session_name = SAVED_SESSIONS[user_input]
        session_path = Path(__file__).parent / "runs" / session_name
        print(f"Playing saved session: {session_path}")
        answer = playback_callbacks([st_callback], str(session_path), max_pause_time=2)
    else:
        answer = mrkl.invoke({"input": user_input}, cfg)

    answer_container.write(answer["output"])
