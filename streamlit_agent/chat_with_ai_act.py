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
from langchain_community.callbacks import StreamlitCallbackHandler, LLMThoughtLabeler
from langchain_core.prompts import (
    ChatPromptTemplate,
    PromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain.agents import AgentExecutor, tool
from langchain_core.prompts import format_document
from langchain_core.messages import get_buffer_string
from streamlit_agent.callbacks.capturing_callback_handler import playback_callbacks
from streamlit_agent.clear_results import with_clear_container
from streamlit.runtime.scriptrunner import add_script_run_ctx, get_script_run_ctx
from langchain_pinecone.vectorstores import PineconeVectorStore
from langchain.tools.retriever import create_retriever_tool
from streamlit.external.langchain.streamlit_callback_handler import LLMThought

import pandas as pd

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
            chapter = doc.metadata["chapter"]
            regulation = doc.metadata["regulation"]
            article = doc.metadata["article"]
            self.status.write(f"**{regulation}**, {chapter}, {article}")
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

df_ai_act = pd.read_pickle("notebooks/ai_act_df.pkl")


@tool
def ai_act_article(query: int) -> str:
    """Zeige den Inhalt des betreffenden Artikels der EU KI Verordnung."""
    return df_ai_act.query(f"article_no == {query}").iloc[0]["page_content"]


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


class StreamlitThreadCallbackHandler(BaseCallbackHandler):
    def __init__(
        self,
        parent_container,
        *,
        max_thought_containers: int = 4,
        expand_new_thoughts: bool = False,
        collapse_completed_thoughts: bool = False,
        thought_labeler=None,
    ):
        """Construct a new StreamlitCallbackHandler. This CallbackHandler is geared
        towards use with a LangChain Agent; it displays the Agent's LLM and tool-usage
        "thoughts" inside a series of Streamlit expanders.

        Parameters
        ----------

        parent_container
            The `st.container` that will contain all the Streamlit elements that the
            Handler creates.

        max_thought_containers

            .. note::
                This parameter is deprecated and is ignored in the latest version of
                the callback handler.

            The max number of completed LLM thought containers to show at once. When
            this threshold is reached, a new thought will cause the oldest thoughts to
            be collapsed into a "History" expander. Defaults to 4.

        expand_new_thoughts
            Each LLM "thought" gets its own `st.expander`. This param controls whether
            that expander is expanded by default. Defaults to False.

        collapse_completed_thoughts
            If True, LLM thought expanders will be collapsed when completed.
            Defaults to False.

        thought_labeler
            An optional custom LLMThoughtLabeler instance. If unspecified, the handler
            will use the default thought labeling logic. Defaults to None.
        """
        self._parent_container = parent_container
        self._history_parent = parent_container.container()
        self._current_thought = None
        self._completed_thoughts = []
        self._max_thought_containers = max(max_thought_containers, 1)
        self._expand_new_thoughts = expand_new_thoughts
        self._collapse_completed_thoughts = collapse_completed_thoughts
        self._thought_labeler = thought_labeler or LLMThoughtLabeler()

    def _require_current_thought(self) -> LLMThought:
        """Return our current LLMThought. Raise an error if we have no current
        thought.
        """
        if self._current_thought is None:
            raise RuntimeError("Current LLMThought is unexpectedly None!")
        return self._current_thought

    def _get_last_completed_thought(self):
        """Return our most recent completed LLMThought, or None if we don't have one."""
        if len(self._completed_thoughts) > 0:
            return self._completed_thoughts[len(self._completed_thoughts) - 1]
        return None

    def _complete_current_thought(self, final_label=None) -> None:
        """Complete the current thought, optionally assigning it a new label.
        Add it to our _completed_thoughts list.
        """
        thought = self._require_current_thought()
        thought.complete(final_label)
        self._completed_thoughts.append(thought)
        self._current_thought = None

    def on_llm_start(self, serialized: dict, prompts: list, **kwargs) -> None:
        add_script_run_ctx(threading.current_thread(), ctx)
        if self._current_thought is None:
            self._current_thought = LLMThought(
                parent_container=self._parent_container,
                expanded=self._expand_new_thoughts,
                collapse_on_complete=self._collapse_completed_thoughts,
                labeler=self._thought_labeler,
            )

        self._current_thought.on_llm_start(serialized, prompts)

        # We don't prune_old_thought_containers here, because our container won't
        # be visible until it has a child.

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        add_script_run_ctx(threading.current_thread(), ctx)
        self._require_current_thought().on_llm_new_token(token, **kwargs)

    def on_llm_end(self, response, **kwargs) -> None:
        self._require_current_thought().on_llm_end(response, **kwargs)

    def on_llm_error(self, error: BaseException, *args, **kwargs) -> None:
        self._require_current_thought().on_llm_error(error, **kwargs)

    def on_tool_start(self, serialized: dict, input_str: str, **kwargs) -> None:
        add_script_run_ctx(threading.current_thread(), ctx)
        self._require_current_thought().on_tool_start(serialized, input_str, **kwargs)

    def on_tool_end(
        self,
        output: str,
        color=None,
        observation_prefix=None,
        llm_prefix=None,
        **kwargs,
    ) -> None:
        self._require_current_thought().on_tool_end(
            output, color, observation_prefix, llm_prefix, **kwargs
        )
        self._complete_current_thought()

    def on_tool_error(self, error: BaseException, *args, **kwargs) -> None:
        self._require_current_thought().on_tool_error(error, **kwargs)

    def on_agent_action(self, action, color=None, **kwargs):
        add_script_run_ctx(threading.current_thread(), ctx)
        self._require_current_thought().on_agent_action(action, color, **kwargs)

    def on_agent_finish(self, finish, color=None, **kwargs) -> None:
        if self._current_thought is not None:
            self._current_thought.complete(self._thought_labeler.get_final_agent_thought_label())
            self._current_thought = None


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

# Setup LLM and QA chain
model_name = st.sidebar.selectbox("model_name", ["gpt-3.5-turbo", "gpt-4"])
llm = ChatOpenAI(
    model_name=model_name, openai_api_key=openai_api_key, temperature=0, streaming=True
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

document_prompt = PromptTemplate(
    input_variables=["page_content", "article", "chapter"],
    template="{page_content}\nQuelle:{chapter}, {article}",
)

ai_act_retriever_tool = create_retriever_tool(
    vectorstore.as_retriever(search_kwargs={"k": 4, "filter": {"use_case": "ai_regulation"}}),
    "search_eu_ai_act",
    "Suche in der EU KI Verordnung nach passenden Abschnitten.",
    document_prompt=document_prompt,
)

DEFAULT_DOCUMENT_PROMPT = PromptTemplate.from_template(template="{page_content}")

tool_list = [ai_act_article, ai_act_retriever_tool]

MEMORY_KEY = "chat_history"
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Sie sind ein auf KI spezialisierter Jurist. Sie recherchieren mithilfe von Tools, über die sie auf Rechtstexte Zugriff haben, um die Frage zu beantworten. Nennen Sie zum Abschluss ihrer Antwort die wichtigsten Quellen als Liste.",
        ),
        MessagesPlaceholder(variable_name=MEMORY_KEY),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

from langchain.agents.format_scratchpad.openai_tools import (
    format_to_openai_tool_messages,
)
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser

llm_with_tools = llm.bind_tools(tool_list)

agent = (
    {
        "input": lambda x: x["input"],
        "agent_scratchpad": lambda x: format_to_openai_tool_messages(x["intermediate_steps"]),
        "chat_history": lambda x: x["chat_history"],
    }
    | prompt
    | llm_with_tools
    | OpenAIToolsAgentOutputParser()
)
agent_executor = AgentExecutor(agent=agent, tools=tool_list, verbose=True)


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
                template="""Beantworten Sie die Frage am Ende des Textes anhand der folgenden Texte aus der EU Verordnung zur künstlichen Intelligenz (KI), auch AI Act genannt. Wenn Sie die Antwort nicht wissen, sagen Sie einfach, dass Sie es nicht wissen, versuchen Sie nicht, eine Antwort zu erfinden.
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
# final_chain = (
#     {"question": RunnablePassthrough()}
#     | loaded_memory
#     | standalone_question
#     | retrieved_documents
#     | answer
#     | itemgetter("answer")
#     | StrOutputParser()
# )
final_chain = (
    {"input": RunnablePassthrough()}
    | loaded_memory
    | agent_executor
    | itemgetter("output")
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
        # retrieval_handler = PrintRetrievalHandler(st.container())
        cfg = RunnableConfig()
        # Add ConsoleCallbackHandler(),
        cfg["callbacks"] = [StreamlitThreadCallbackHandler(st.container())]
        st.write(final_chain.stream(user_query, cfg))
