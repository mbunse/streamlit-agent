import base64
import os
import streamlit as st
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_pinecone import PineconeVectorStore
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain.callbacks.base import BaseCallbackHandler
from langchain.chains import ConversationalRetrievalChain
from langchain_core.prompts import (
    PromptTemplate,
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from pinecone import Pinecone

st.set_page_config(
    page_title="Chat mit RVS Website",
    page_icon="./streamlit_agent/static/ai_act.png",
)

logo_image = "./streamlit_agent/static/ai_act.png"
logo_image_data = base64.b64encode(open(logo_image, "rb").read()).decode()
st.markdown(
    f'# <img src="data:image/png;base64,{logo_image_data}" alt="Illustration zur EU KI Verordnung" width="100"/> Chat mit EU KI Verordnung',
    unsafe_allow_html=True,
)


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
pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
pc_index = pc.Index(index_name)
openai_lc_client = PineconeVectorStore(pc_index, embedding)
retriever = openai_lc_client.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k": 4,
        "fetch_k": 20,
    },
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
llm = ChatOpenAI(
    model_name="gpt-3.5-turbo", openai_api_key=openai_api_key, temperature=0, streaming=True
)
condense_question_prompt = PromptTemplate(
    input_variables=["chat_history", "question"],
    template="""Formulieren Sie folgenden Chat-Verlauf und die anschließende Frage so um, dass sie eine eigenständige Frage des Kunden ist.


Chat-Verlauf:
{chat_history}
anschließende Frage des Mandanten: {question}
eigenständige Frage des Mandanten:""",
)

answer_prompt_template = ChatPromptTemplate(
    input_variables=["context", "question"],
    messages=[
        SystemMessagePromptTemplate(
            prompt=PromptTemplate(
                input_variables=["context"],
                template="""Sie sind ein für KI-Recht spezialisierter Jurist. Beantworten Sie die Frage am Ende des Textes anhand der folgenden Texte aus der EU Verordnung zur künstlichen Intelligenz (KI), auch AI Act genannt. Wenn Sie die Antwort nicht wissen, sagen Sie einfach, dass Sie es nicht wissen, versuchen Sie nicht, eine Antwort zu erfinden.
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
