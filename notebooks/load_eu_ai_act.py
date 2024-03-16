# %%
from langchain_community.document_loaders import MathpixPDFLoader
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from datetime import datetime
import pickle
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
from pinecone import Pinecone, PodSpec
import os
import re
import itertools

# %% [markdown]
# https://www.abiturloesung.de/abitur/Bayern/Gymnasium

# %%
# data =[]
# data_dir = "../data"
# for filename in os.listdir(data_dir):
#     if os.path.isfile(os.path.join(data_dir, filename)):
#         file_path = os.path.join(data_dir, filename)
#         print(file_path)
#         loader = MathpixPDFLoader(file_path)
#         data.extend(loader.load())

# %%
# pickle.dump(data, open("abi_mathe.pkl", "wb"))

# %%
data = pickle.load(open("abi_mathe.pkl", "rb"))
data[:1]

# %%
data[0].metadata

# %%
for doc in data:
    filename = os.path.basename(doc.metadata["source"]).split(".")[0]
    out_path = f"../data/md/{filename}.md"

    # write the markdown file
    with open(out_path, "w") as f:
        f.write(doc.page_content)


# %%
edited_md_files = [
    "../data/md/2015_Stochastik_III.md",
    "../data/md/2015_Stochastik_IV.md",
]
data = []
for filename in edited_md_files:
    with open(filename, "r") as f:
        content = f.read()
        data.append(Document(content, metadata={"source": filename}))
data

# %%
data[0].metadata

# %%
import IPython

IPython.display.Markdown(data[0].page_content)

# %%
for doc in data:
    doc.metadata["year"] = re.search(r"20\d{2}", doc.metadata["source"]).group(0)
    doc.metadata["topic"] = re.search(r"_([A-Za-z]*)_", doc.metadata["source"]).group(1)
    doc.metadata["variant"] = re.search(r"_([A-Za-z]*)_([IVX]*)", doc.metadata["source"]).group(2)
    new_content = []
    for line in doc.page_content.split("\n"):
        if line.startswith("Abitur"):
            line = "# " + line
        if line.startswith("Teilaufgabe"):
            line = "## " + line
        if line.startswith("Lösung zu "):
            line = "## " + line
        new_content.append(line)
    doc.page_content = "\n".join(new_content)

# %%
data[0].metadata

# %%
data[0].page_content

# %%
headers_to_split_on = [
    ("#", "exam"),
    ("##", "task"),
]

splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on, strip_headers=False)

md_header_splits = []
for doc in data:
    split_docs = splitter.split_text(doc.page_content)
    for split_doc in split_docs:
        split_doc.metadata.update(doc.metadata)
    md_header_splits.extend(split_docs)

md_header_splits[0].metadata

# %%
for doc in md_header_splits:
    doc.metadata["use_case"] = "abi_math"
    if "task" in doc.metadata and " A" in doc.metadata["task"]:
        doc.metadata["test_part"] = "A"
    elif "task" in doc.metadata and " B" in doc.metadata["task"]:
        doc.metadata["test_part"] = "B"
md_header_splits[0].metadata

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
pc_vector_store = PineconeVectorStore(pc_index, embedding).from_documents(
    md_header_splits,
    embedding=embedding,
    index_name=index_name,
)

# %%
pc_index.describe_index_stats()
