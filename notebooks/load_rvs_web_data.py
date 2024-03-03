# %%
from langchain.docstore.document import Document
from langchain.indexes import VectorstoreIndexCreator
from langchain_community.utilities import ApifyWrapper
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
import pinecone
import os


# %%
pinecone.init(api_key=os.environ["PINECONE_API_KEY"], environment=os.environ["PINECONE_ENV"])


# %%


embedding = OpenAIEmbeddings()
index_name = "rvs-demo"
namespace = "my-namespace"
vectorstore = PineconeVectorStore(
    index_name=index_name,
    embedding=embedding,
)

# %%
apify = ApifyWrapper()
# Call the Actor to obtain text from the crawled webpages
url = "https://www.raiffeisen.at/rvs/de/privatkunden.html"
loader = apify.call_actor(
    actor_id="apify/website-content-crawler",
    run_input={
        "includeUrlGlobs": [{"glob": "https://www.raiffeisen.at/rvs/de/privatkunden/*/*"}],
        "maxCrawlDepth": 2,
        "maxResults": 10,
        "startUrls": [{"url": "https://www.raiffeisen.at/rvs/de/privatkunden.html"}],
        "maxCrawlPages": 1000,
        "saveMarkdown": True,
    },
    dataset_mapping_function=lambda item: Document(
        page_content=item["markdown"] or "",
        metadata={"source": item["url"], "date": datetime.now().isoformat()},
    ),
)


# %%
# load the document and split it into chunks
documents = loader.load()

# %%
pickle.dump(documents, open("documents.pkl", "wb"))

# %%
documents = pickle.load(open("documents.pkl", "rb"))

# %%
documents

# %%
headers_to_split_on = [
    ("#", "Header 1"),
    ("##", "Header 2"),
    ("###", "Header 3"),
]

markdown_splitter = MarkdownTextSplitter()
md_header_splits = markdown_splitter.split_documents(documents)
md_header_splits[0]

# %%
md_header_splits[0].metadata

# %%
chunk_size = 1500
chunk_overlap = 100
text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
split_documents = text_splitter.split_documents(documents)
split_documents[:4]

# %%
import IPython

IPython.display.Markdown(split_documents[0].page_content)

# %%
embeddings = OpenAIEmbeddings()
openai_lc_client = Chroma.from_documents(
    split_documents, embeddings, collection_name="rvs_webpages", client=persistent_client
)

# %%


# %%
list_of_urls = list({el["source"] for el in collection.get()["metadatas"]})
list_of_urls

# %%
persistent_client2 = chromadb.PersistentClient(path="./chroma_db")
persistent_client2.get_collection("rvs_webpages").get()["metadatas"][0]
