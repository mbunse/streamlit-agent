from typing import Any
import base64
import os
import re
import threading
import streamlit as st
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from pinecone import Pinecone as Pinecone_orig
from langchain_community.vectorstores.pinecone import Pinecone
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain.callbacks.base import BaseCallbackHandler
from langchain.callbacks.tracers import ConsoleCallbackHandler
from langchain.chains.query_constructor.base import AttributeInfo
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableConfig
from langchain_community.callbacks import StreamlitCallbackHandler
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema.output import LLMResult
from streamlit_agent.callbacks.capturing_callback_handler import playback_callbacks
from streamlit_agent.clear_results import with_clear_container
from streamlit.runtime.scriptrunner import add_script_run_ctx, get_script_run_ctx
import pypandoc

from langchain_pinecone.vectorstores import PineconeVectorStore

st.set_page_config(
    page_title="Chat mit Mathe Lehrer",
    page_icon="🧮",
)

st.markdown("# 🧮 Chat mit Mathe Lehrer")

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


pc = Pinecone_orig(api_key=os.environ["PINECONE_API_KEY"])
pc.list_indexes()
index_name = "rvs-demo"
pc_index = pc.Index(index_name)
vectorstore = PineconeVectorStore(
    index=pc_index,
    embedding=embedding,
)


# Setup LLM and QA chain
model_name = st.sidebar.selectbox("model_name", ["gpt-3.5-turbo", "gpt-4-turbo-preview"])
llm = ChatOpenAI(
    model_name=model_name, openai_api_key=openai_api_key, temperature=0, streaming=True
)

template = """Sie sind ein Mathematik-Lehrer und sollen eine Abitur-Klausuraufgabe inkl. Lösung erstellen. Gehen sie dabei auf den Wunsch des Kollegen am Ende des Chat-Verlaufs ein und orientieren Sie sich bzgl. Schwierigkeitsgrad, Anspruch und Inhalt anhand der folgenden Beispiel aus alten Abitur-Klausuren.
----------------
{context}
----------------
Berückstichtigen Sie für die Klausur-Aufgabe dabei bitte die Folgendes: {question}
"""
prompt = ChatPromptTemplate.from_template(template)


def format_docs(docs):
    return "\n\n---------\n\n".join(
        [f"Aus {d.metadata['exam']}:\n\n{d.page_content}" for d in docs]
    )


ctx = get_script_run_ctx()

with st.form(key="form"):
    topic = st.selectbox(
        "Thema",
        [
            "Stochastik",
        ],
    )
    test_part = st.selectbox("Teil der Klausur", ["A", "B"])
    user_input = st.text_area(
        "Was soll bei der Erstellung der Klausur-Aufgabe berücksichtigt werden?"
    )
    submit_clicked = st.form_submit_button("Aufgabe erstellen")

chain = (
    {
        "context": vectorstore.as_retriever(
            search_kwargs={
                "k": 2,
                "filter": {"topic": topic, "test_part": test_part, "use_case": "abi_math"},
            }
        )
        | format_docs,
        "question": RunnablePassthrough(),
    }
    | prompt
    | llm
    | StrOutputParser()
)


class StreamHandler(BaseCallbackHandler):
    def __init__(self, container: st.delta_generator.DeltaGenerator, initial_text: str = ""):
        self.container = container
        self.text = initial_text
        self.run_id_ignore_token = None

    def on_llm_start(self, serialized: dict, prompts: list, **kwargs):
        # Workaround to prevent showing the rephrased question as output
        add_script_run_ctx(threading.current_thread(), ctx)
        if prompts[0].startswith("Human"):
            self.run_id_ignore_token = kwargs.get("run_id")

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        if self.run_id_ignore_token == kwargs.get("run_id", False):
            return
        self.text += token
        self.container.markdown(self.text)

    def on_llm_end(self, response: LLMResult, **kwargs) -> Any:
        add_script_run_ctx(threading.current_thread(), ctx)
        pypandoc.convert_text(
            response.generations[0][0].text, "docx", format="md", outputfile="output.docx"
        )
        with open("output.docx", "rb") as output:
            self.container.download_button(
                "Download",
                output,
                "output.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )


class PrintRetrievalHandler(BaseCallbackHandler):
    def __init__(self, container):
        self.status = container.status("**Context Retrieval**")

    def on_retriever_start(self, serialized: dict, query: str, **kwargs):
        add_script_run_ctx(threading.current_thread(), ctx)
        self.status.write(f"**Frage:** {query}")
        self.status.update(label=f"**Context Retrieval:** {query}")

    def on_chain_end(self, outputs: dict, **kwargs):
        if "repr" in outputs:
            match = re.search(r"filter=(.*?),", outputs["repr"])
            if match:
                self.status.write(f"**Filter:** {match.group(1)}")

    def on_retriever_end(self, documents, **kwargs):
        for idx, doc in enumerate(documents):
            source = doc.metadata["source"]
            self.status.write(f"**{source}**")
            self.status.markdown(doc.page_content)
        self.status.update(state="complete")


output_container = st.empty()
if with_clear_container(submit_clicked):
    output_container = output_container.container()
    output_container.chat_message("user").write(user_input)

    answer_container = output_container.chat_message("assistant", avatar="🧮")

    with answer_container:
        retrieval_handler = PrintRetrievalHandler(st.container())
        stream_handler = StreamHandler(st.empty())
    # st_callback = StreamlitCallbackHandler(answer_container)
    cfg = RunnableConfig()
    # cfg["callbacks"] = [st_callback]
    cfg["callbacks"] = [retrieval_handler, stream_handler, ConsoleCallbackHandler()]
    # cfg["max_concurrency"] = 0

    # If we've saved this question, play it back instead of actually running LangChain
    # (so that we don't exhaust our API calls unnecessarily)
    answer = chain.stream(user_input, cfg)

    answer_container.write(answer)
