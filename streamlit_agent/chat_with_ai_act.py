import base64
import os
import re
from operator import itemgetter
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
from langchain_core.runnables import RunnablePassthrough, RunnableConfig, RunnableLambda
from langchain_community.callbacks import StreamlitCallbackHandler
from langchain_core.prompts import (
    ChatPromptTemplate,
    PromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_core.prompts import format_document
from langchain_core.messages import get_buffer_string
from streamlit_agent.callbacks.capturing_callback_handler import playback_callbacks
from streamlit_agent.clear_results import with_clear_container
from streamlit.runtime.scriptrunner import add_script_run_ctx, get_script_run_ctx
from langchain_pinecone.vectorstores import PineconeVectorStore


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

ctx = get_script_run_ctx()


class StreamHandler(BaseCallbackHandler):
    def __init__(self, container: st.delta_generator.DeltaGenerator, initial_text: str = ""):
        self.container = container
        self.text = initial_text
        self.run_id_ignore_token = None

    def on_llm_start(self, serialized: dict, prompts: list, **kwargs):
        add_script_run_ctx(threading.current_thread(), ctx)

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
        add_script_run_ctx(threading.current_thread(), ctx)
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
pc = Pinecone_orig(api_key=os.environ["PINECONE_API_KEY"])
pc.list_indexes()
index_name = "rvs-demo"
pc_index = pc.Index(index_name)
vectorstore = PineconeVectorStore(
    index=pc_index,
    embedding=embedding,
)


from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage


class StreamlitThreadChatMessageHistory(BaseChatMessageHistory):
    """
    Chat message history that stores messages in Streamlit session state.

    Args:
        key: The key to use in Streamlit session state for storing messages.
    """

    def __init__(self, key: str = "langchain_messages"):
        if key not in st.session_state:
            st.session_state[key] = []
        self._key = key

    @property
    def messages(self):
        """Retrieve the current list of messages"""
        add_script_run_ctx(threading.current_thread(), ctx)
        return st.session_state[self._key]

    @messages.setter
    def messages(self, value) -> None:
        add_script_run_ctx(threading.current_thread(), ctx)
        st.session_state[self._key] = value

    def add_message(self, message: BaseMessage) -> None:
        """Add a message to the session memory"""
        add_script_run_ctx(threading.current_thread(), ctx)
        self.messages.append(message)

    def clear(self) -> None:
        """Clear session memory"""
        self.messages.clear()


# Setup memory for contextual conversation
msgs = StreamlitThreadChatMessageHistory()
memory = ConversationBufferMemory(
    memory_key="chat_history",
    chat_memory=msgs,
    return_messages=True,
    output_key="answer",
    input_key="question",
)
loaded_memory = RunnablePassthrough.assign(
    chat_history=RunnableLambda(memory.load_memory_variables) | itemgetter("chat_history"),
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

# Now we calculate the standalone question
standalone_question = {
    "standalone_question": {
        "question": lambda x: x["question"],
        "chat_history": lambda x: get_buffer_string(x["chat_history"]),
    }
    | condense_question_prompt
    | ChatOpenAI(temperature=0)
    | StrOutputParser(),
}

# Now we retrieve the documents
retrieved_documents = {
    "docs": itemgetter("standalone_question")
    | vectorstore.as_retriever(search_kwargs={"k": 2, "filter": {"use_case": "ai_regulation"}}),
    "question": lambda x: x["standalone_question"],
}
DEFAULT_DOCUMENT_PROMPT = PromptTemplate.from_template(template="{page_content}")


def _combine_documents(docs, document_prompt=DEFAULT_DOCUMENT_PROMPT, document_separator="\n\n"):
    doc_strings = [format_document(doc, document_prompt) for doc in docs]
    return document_separator.join(doc_strings)


# Now we construct the inputs for the final prompt
final_inputs = {
    "context": lambda x: _combine_documents(x["docs"]),
    "question": itemgetter("question"),
}

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

# And finally, we do the part that returns the answers
answer = {
    "answer": final_inputs | answer_prompt_template | ChatOpenAI(),
    "docs": itemgetter("docs"),
}
# And now we put it all together!
final_chain = (
    {"question": RunnablePassthrough()}
    | loaded_memory
    | standalone_question
    | retrieved_documents
    | answer
    | itemgetter("answer")
    | StrOutputParser()
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
        cfg = RunnableConfig()
        cfg["callbacks"] = [retrieval_handler, ConsoleCallbackHandler()]
        st.write(final_chain.stream(user_query, cfg))
