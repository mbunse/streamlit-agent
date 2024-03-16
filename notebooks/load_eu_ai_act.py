# %%
from langchain.docstore.document import Document
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from datetime import datetime
import pickle
import re
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
from pinecone import Pinecone, PodSpec
import os
import pandas as pd


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
# pc_index.delete(
#     filter={
#         "use_case": {"$eq": "ai_regulation"},
#     }
# )

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
edited_md_files = [
    "TA-9-2024-0138_DE_utf8.md",
]
documents = []
for filename in edited_md_files:
    with open(filename, "r", encoding="utf8") as f:
        content = f.read()
        content = content.replace("\xa0", " ")
        documents.append(Document(content, metadata={"source": filename}))
documents

# %%
documents[0].metadata["use_case"] = "ai_regulation"
documents[0].metadata["regulation"] = "EU KI-Verordnung"
documents[0].metadata["date"] = "2024-03-13"

# %%
headers_to_split_on = [
    ("#", "chapter"),
    ("##", "section"),
    ("###", "article"),
]

splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on, strip_headers=False)

md_header_splits = []
for doc in documents:
    split_docs = splitter.split_text(doc.page_content)
    for split_doc in split_docs:
        split_doc.metadata.update(doc.metadata)
    md_header_splits.extend(split_docs)

md_header_splits[20].metadata

# %%
for doc in md_header_splits:
    # extract article number
    if not "article" in doc.metadata:
        doc.metadata["article"] = ""
        doc.metadata["article_no"] = 0
    else:
        article = doc.metadata["article"]
        match = re.match(r"Artikel (\d+)", article)
        if match:
            article_no = int(match.group(1))
            doc.metadata["article_no"] = article_no
        else:
            doc.metadata["article_no"] = 0
md_header_splits[89].metadata

# %%
md_header_splits[:2]

# %%
import IPython

IPython.display.Markdown(md_header_splits[0].page_content[:1000])

# %% [markdown]
# Anzahl der Dokumente nach Split

# %%
len(md_header_splits)

# %%
splitted_docs = RecursiveCharacterTextSplitter(
    chunk_size=700, chunk_overlap=100, add_start_index=True
).split_documents(md_header_splits)
splitted_docs[10].metadata

# %% [markdown]
# Dokumente in Vector Store ablegen.

# %%
embedding = OpenAIEmbeddings()
pc_vector_store = PineconeVectorStore(pc_index, embedding).from_documents(
    splitted_docs,
    embedding=embedding,
    index_name=index_name,
)

# %%
pc_index.describe_index_stats()

# %%
pc_vector_store.search("Kreditwürdigkeit", search_type="mmr")

# %%

doc_dicts = [dict(doc) for doc in md_header_splits]
df = pd.DataFrame([{"page_content": doc["page_content"]} | doc["metadata"] for doc in doc_dicts])
df.to_pickle("ai_act_df.pkl")
df.head()
