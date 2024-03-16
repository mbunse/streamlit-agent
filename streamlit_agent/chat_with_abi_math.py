import base64
import os
import streamlit as st
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from pinecone import Pinecone as Pinecone_orig
from langchain_community.vectorstores.pinecone import Pinecone
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain.callbacks.base import BaseCallbackHandler
from langchain.chains.query_constructor.base import AttributeInfo
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain.chains import LLMMathChain
from langchain_core.runnables import RunnableConfig
from langchain_community.callbacks import StreamlitCallbackHandler
from langchain.tools.retriever import create_retriever_tool
from langchain.agents import AgentType, initialize_agent
from langchain.agents import AgentExecutor, Tool, create_react_agent
from streamlit_agent.clear_results import with_clear_container
from langchain import hub

from langchain_core.prompts import (
    PromptTemplate,
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)


st.set_page_config(
    page_title="Chat mit Mathe Lehrer",
    page_icon="🧮",
)

st.markdown("# 🧮 Chat mit Mathe Lehrer")


class StreamHandler(BaseCallbackHandler):
    def __init__(self, container: st.delta_generator.DeltaGenerator, initial_text: str = ""):
        self.container = container
        self.text = initial_text
        self.run_id_ignore_token = None

    def on_llm_start(self, serialized: dict, prompts: list, **kwargs):
        # Workaround to prevent showing the rephrased question as output
        if prompts[0].startswith("Human"):
            self.run_id_ignore_token = kwargs.get("run_id")

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        if self.run_id_ignore_token == kwargs.get("run_id", False):
            return
        self.text += token
        self.container.markdown(self.text)


class PrintRetrievalHandler(BaseCallbackHandler):
    def __init__(self, container):
        self.status = container.status("**Context Retrieval**")

    def on_retriever_start(self, serialized: dict, query: str, **kwargs):
        self.status.write(f"**Frage:** {query}")
        self.status.update(label=f"**Context Retrieval:** {query}")

    def on_retriever_end(self, documents, **kwargs):
        for idx, doc in enumerate(documents):
            source = doc.metadata["source"]
            self.status.write(f"**{source}**")
            self.status.markdown(doc.page_content)
        self.status.update(state="complete")


openai_api_key = os.getenv("OPENAI_API_KEY", "not_supplied")

embedding = OpenAIEmbeddings()
index_name = "rvs-demo"

# {'Header 1': 'Abitur 2019 Mathematik Infinitesimalrechnung I',
#  'Header 2': 'Teilaufgabe Teil A 1 (5 BE)',
#  'source': '../data/2019_Infinitesimalrechnung_I.pdf',
#  'file_path': '../data/2019_Infinitesimalrechnung_I.pdf',
#  'pdf_id': '2024_03_15_a1b141dba6eb6e8ea5efg',
#  'year': '2019',
#  'topic': 'Infinitesimalrechnung',
#  'variant': 'I',
#  'use_case': 'abi_math',
#  'text': '# Abitur 2019 Mathematik Infinitesimalrechnung I  \n## Teilaufgabe Teil A 1 (5 BE)  \nGegeben ist die Funktion $f: x \\mapsto \\frac{e^{2 x}}{x}$ mit Definitionsbereich $D_{f}=\\mathbb{R} \\backslash\\{0\\}$. Bestimmen Sie Lage und Art des Extrempunkts des Graphen von $f$.  \nGegeben ist die in $\\mathbb{R} \\backslash\\{0\\}$ definierte Funktion $f: x \\mapsto 1-\\frac{1}{x^{2}}$, die die Nullstellen $x_{1}=-1$ und $x_{2}=1$ hat. Abbildung 1 zeigt den Graphen von $f$, der symmetrisch bezüglich der y-Achse ist. Weiterhin ist die Gerade $g$ mit der Gleichung $y=-3$ gegeben.  \n![](https://cdn.mathpix.com/cropped/2024_03_15_a1b141dba6eb6e8ea5efg-01.jpg?height=467&width=649&top_left_y=710&top_left_x=433)',
#  'test_part': 'A'}

metadata_field_info = [
    AttributeInfo(
        name="Header 1",
        description="Main header of the test, e.g. Abitur 2019 Mathematik Infinitesimalrechnung",
        type="string",
    ),
    AttributeInfo(
        name="Header 2",
        description="Secondary header of the test, e.g. Teilaufgabe Teil A 1 (5 BE)",
        type="string",
    ),
    AttributeInfo(
        name="topic",
        description="The topic of the test",
        type="string",
    ),
    AttributeInfo(
        name="test_part",
        description="The part of the test. A means part for which tools like a calculator are allowed, B means part for which no tools are allowed",
        type="string",
    ),
]
document_content_description = "Text extracts from math tests including solutions"

pc = Pinecone_orig(api_key=os.environ["PINECONE_API_KEY"])
pc.list_indexes()
index_name = "rvs-demo"
pc_index = pc.Index(index_name)
vector_store = Pinecone(pc_index, embedding, text_key="text")
model_name = st.sidebar.selectbox("model_name", ["gpt-3.5-turbo", "gpt-4"])

llm = ChatOpenAI(
    model_name="gpt-3.5-turbo", openai_api_key=openai_api_key, temperature=0, streaming=True
)
retriever = SelfQueryRetriever.from_llm(
    llm,
    vector_store,
    document_content_description,
    metadata_field_info,
    verbose=True,
)

retriever_tool = create_retriever_tool(
    retriever,
    "math_test_similar",
    "Search for similar extracts from German math tests. Test part A is for which tools like a calculator are allowed, for test part B no tools are allowed. Example: 'Statisikaufgabe ohne Taschenrechner zur Normalverteilung'",
)
llm_math_chain = LLMMathChain.from_llm(llm)

tools = [
    retriever_tool,
    Tool(
        name="Calculator",
        func=llm_math_chain.run,
        description="useful for when you need to answer questions about math",
    ),
]

react_agent = create_react_agent(
    llm,
    tools,
    PromptTemplate(
        input_variables=["agent_scratchpad", "input", "tool_names", "tools"],
        template="You are a math teacher. Construct a new task for a math test and provide a solution. You have access to the following tools:\n\n{tools}\n\nUse the following format:\n\nQuestion: the input question you must answer\nThought: you should always think about what to do\nAction: the action to take, should be one of [{tool_names}]\nAction Input: the input to the action\nObservation: the result of the action\n... (this Thought/Action/Action Input/Observation can repeat N times)\nThought: I now know the final answer\nFinal Answer: the final answer to the original input question **in German**!\n\nBegin!\n\nQuestion: {input}\nThought:{agent_scratchpad}",
    ),
)
mrkl = AgentExecutor(agent=react_agent, tools=tools)

with st.form(key="form"):
    user_input = st.text_input("Or, ask your own question")
    submit_clicked = st.form_submit_button("Submit Question")


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
    answer = mrkl.invoke({"input": user_input}, cfg)

    answer_container.write(answer["output"])
