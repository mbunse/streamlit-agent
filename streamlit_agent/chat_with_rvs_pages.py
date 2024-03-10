import os
import tempfile
from operator import itemgetter
import streamlit as st
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_pinecone import PineconeVectorStore
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain.callbacks.base import BaseCallbackHandler
from langchain.chains import ConversationalRetrievalChain
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import AIMessage, HumanMessage, get_buffer_string
from langchain_core.prompts import format_document, ChatPromptTemplate, PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnableLambda, RunnablePassthrough

from pinecone import Pinecone

st.set_page_config(page_title="LangChain: Chat with Documents", page_icon="🦜")
st.title("🦜 LangChain: Chat with Documents")


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
retriever = openai_lc_client.as_retriever(search_type="mmr", search_kwargs={"k": 4, "fetch_k": 20})


# Setup memory for contextual conversation
msgs = StreamlitChatMessageHistory()
memory = ConversationBufferMemory(memory_key="chat_history", chat_memory=msgs, return_messages=True)


_template = """Formuliere den folgenden Chatverlauf und die anschließende Frage so um, dass die anschließende Frage eine eigenständige Frage ist.

Chatverlauf:
{chat_history}
Frage: {question}
eigenständige Frage:"""
CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template(_template)

template = """Beantworte die Frage basierend auf folgendem Kontext:
{context}

Question: {question}
"""
ANSWER_PROMPT = ChatPromptTemplate.from_template(template)

# Setup LLM and QA chain
llm = ChatOpenAI(
    model_name="gpt-3.5-turbo", openai_api_key=openai_api_key, temperature=0, streaming=True
)

DEFAULT_DOCUMENT_PROMPT = PromptTemplate.from_template(template="{page_content}")


def _combine_documents(docs, document_prompt=DEFAULT_DOCUMENT_PROMPT, document_separator="\n\n"):
    doc_strings = [format_document(doc, document_prompt) for doc in docs]
    return document_separator.join(doc_strings)


_inputs = RunnableParallel(
    standalone_question=RunnablePassthrough.assign(
        chat_history=lambda x: get_buffer_string(x["chat_history"])
    )
    | CONDENSE_QUESTION_PROMPT
    | ChatOpenAI(temperature=0)
    | StrOutputParser(),
)
_context = {
    "context": itemgetter("standalone_question") | retriever | _combine_documents,
    "question": lambda x: x["standalone_question"],
}
conversational_qa_chain = _inputs | _context | ANSWER_PROMPT | llm

if len(msgs.messages) == 0 or st.sidebar.button("Chatverlauf löschen"):
    msgs.clear()
    msgs.add_ai_message("Wie kann ich helfen?")

avatars = {"human": "user", "ai": "assistant"}
for msg in msgs.messages:
    st.chat_message(avatars[msg.type]).write(msg.content)

if user_query := st.chat_input(placeholder="Frage mich etwas!"):
    st.chat_message("user").write(user_query)

    with st.chat_message("assistant"):
        retrieval_handler = PrintRetrievalHandler(st.container())
        stream_handler = StreamHandler(st.empty())

        response = conversational_qa_chain.invoke(
            {"question": user_query, "chat_history": msgs.messages},
            config={"callbacks": [retrieval_handler, stream_handler]},
        )
