# %%
from langchain.docstore.document import Document
from langchain.indexes import VectorstoreIndexCreator
from langchain_community.document_loaders import Docx2txtLoader
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import (
    HTMLHeaderTextSplitter,
    RecursiveCharacterTextSplitter,
    MarkdownTextSplitter,
)
from langchain_openai import OpenAIEmbeddings
from datetime import datetime
import pickle
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
from pinecone import Pinecone, PodSpec
import os


# %%
# configure client
pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
pc.list_indexes()

# %%
index_name = "rvs-demo"
pc_index = pc.Index(index_name)
pc_index.describe_index_stats()

# %%
pc.delete_index(index_name)

# %%
pc.create_index(
    name=index_name,
    dimension=1536,
    metric="cosine",
    spec=PodSpec(environment=os.environ["PINECONE_ENV"], pod_type="starter", pods=1),
)

# %%
embedding = OpenAIEmbeddings()

# %% [markdown]
# Text von https://www.europarl.europa.eu/news/en/press-room/20240308IPR19015/artificial-intelligence-act-meps-adopt-landmark-law

# %%
loader = Docx2txtLoader("TA-9-2024-0138_DE.docx")

# %%
# load the document and split it into chunks
documents = loader.load()

# %%
documents

# %%
chunk_size = 1500
chunk_overlap = 300
text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
split_documents = text_splitter.split_documents(documents)
split_documents[:4]

# %%
import IPython

IPython.display.Markdown(split_documents[0].page_content)

# %% [markdown]
# Anzahl der Dokumente nach Split

# %%
len(split_documents)

# %% [markdown]
# Dokumente in Vector Store ablegen.

# %%
embedding = OpenAIEmbeddings()
pc_vector_store = PineconeVectorStore(pc_index, embedding).from_documents(
    split_documents,
    embedding=embedding,
    index_name=index_name,
)

# %%
pc_index.describe_index_stats()

# %%
pc_vector_store.search("Kredit", search_type="similarity")
