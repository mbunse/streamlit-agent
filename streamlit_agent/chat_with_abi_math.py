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
from langchain.chains import ConversationalRetrievalChain
from langchain_core.prompts import (
    PromptTemplate,
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
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

llm_retriever = ChatOpenAI(
    model_name="gpt-3.5-turbo", openai_api_key=openai_api_key, temperature=0, streaming=True
)
retriever = SelfQueryRetriever.from_llm(
    llm_retriever,
    vector_store,
    document_content_description,
    metadata_field_info,
    verbose=True,
)

# Setup memory for contextual conversation
msgs = StreamlitChatMessageHistory()
memory = ConversationBufferMemory(
    memory_key="chat_history",
    chat_memory=msgs,
    ai_prefix="Anwalt",
    human_prefix="Mandant",
    return_messages=True,
)

# Setup LLM and QA chain
model_name = st.sidebar.selectbox("model_name", ["gpt-3.5-turbo", "gpt-4"])
llm = ChatOpenAI(
    model_name=model_name, openai_api_key=openai_api_key, temperature=0, streaming=True
)
condense_question_prompt = PromptTemplate(
    input_variables=["chat_history", "question"],
    template="""Formulieren Sie folgenden Chat-Verlauf und die anschließende Frage so um, dass sie eine eigenständige Frage des Lehrer-Kollegen ist.


Chat-Verlauf:
{chat_history}
anschließende Frage des Lehrer-Kollegen: {question}
eigenständige Frage des Lehrer-Kollegen:""",
)

answer_prompt_template = ChatPromptTemplate(
    input_variables=["context", "question"],
    messages=[
        SystemMessagePromptTemplate(
            prompt=PromptTemplate(
                input_variables=["context"],
                template="""Sie sind ein für Mathematik-Lehrer. Beantworten Sie die Frage am Ende des Textes anhand der folgenden Texte aus alten Klausuren und versuchen Sie sich unbedingt an den Stil der alten Klausuraufgaben bei ihrer Antowrt zu orientieren.
----------------
{context}
----------------
""",
            )
        ),
        HumanMessagePromptTemplate(
            prompt=PromptTemplate(input_variables=["question"], template="{question}")
        ),
    ],
)
qa_chain = ConversationalRetrievalChain.from_llm(
    llm,
    retriever=retriever,
    memory=memory,
    verbose=True,
    condense_question_prompt=condense_question_prompt,
    combine_docs_chain_kwargs={"prompt": answer_prompt_template},
)

if len(msgs.messages) == 0 or st.sidebar.button("Chat-Verlauf löschen"):
    msgs.clear()
    # msgs.add_ai_message("Wie kann ich helfen?")

avatars = {"human": "user", "ai": "assistant"}
for msg in msgs.messages:
    st.chat_message(avatars[msg.type]).write(msg.content)

if user_query := st.chat_input(placeholder="Frage mich etwas!"):
    st.chat_message("user").write(user_query)

    with st.chat_message("assistant"):
        retrieval_handler = PrintRetrievalHandler(st.container())
        stream_handler = StreamHandler(st.empty())
        response = qa_chain.run(user_query, callbacks=[retrieval_handler, stream_handler])
