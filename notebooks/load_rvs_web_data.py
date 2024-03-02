# %%
from langchain.docstore.document import Document
from langchain.indexes import VectorstoreIndexCreator
from langchain_community.utilities import ApifyWrapper
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import HTMLHeaderTextSplitter, RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from datetime import datetime

import chromadb


# %%
persistent_client = chromadb.PersistentClient(path="./chroma_db")
collection = persistent_client.get_or_create_collection("rvs_webpages")
# collection.add(ids=["1", "2", "3"], documents=["a", "b", "c"])

# %%
collection.get()

# %%
apify = ApifyWrapper()
# Call the Actor to obtain text from the crawled webpages
url = "https://www.raiffeisen.at/rvs/de/privatkunden.html"
loader = apify.call_actor(
    actor_id="apify/website-content-crawler",
    run_input={
        "aggressivePrune": False,
        "clickElementsCssSelector": '[aria-expanded="false"]',
        "clientSideMinChangePercentage": 15,
        "debugLog": False,
        "debugMode": False,
        "ignoreCanonicalUrl": False,
        "includeUrlGlobs": [{"glob": "https://www.raiffeisen.at/rvs/de/privatkunden/*/*"}],
        "maxCrawlDepth": 2,
        "maxResults": 1000,
        "proxyConfiguration": {"useApifyProxy": True},
        "readableTextCharThreshold": 100,
        "removeCookieWarnings": True,
        "removeElementsCssSelector": 'nav, footer, script, style, noscript, svg,\n[role="alert"],\n[role="banner"],\n[role="dialog"],\n[role="alertdialog"],\n[role="region"][aria-label*="skip" i],\n[aria-modal="true"]',
        "renderingTypeDetectionPercentage": 10,
        "saveFiles": False,
        "saveHtml": False,
        "saveMarkdown": True,
        "saveScreenshots": False,
        "startUrls": [{"url": "https://www.raiffeisen.at/rvs/de/privatkunden.html"}],
        "useSitemaps": False,
        "crawlerType": "playwright:firefox",
        "excludeUrlGlobs": [],
        "maxCrawlPages": 1000,
        "initialConcurrency": 0,
        "maxConcurrency": 200,
        "initialCookies": [],
        "maxSessionRotations": 10,
        "maxRequestRetries": 5,
        "requestTimeoutSecs": 60,
        "dynamicContentWaitSecs": 10,
        "maxScrollHeightPixels": 5000,
        "htmlTransformer": "readableText",
    },
    dataset_mapping_function=lambda item: Document(
        page_content=item["text"] or "",
        metadata={"source": item["url"], "date": datetime.now().isoformat()},
    ),
)


# %%
# load the document and split it into chunks
documents = loader.load()

# %%
documents

# %%
chunk_size = 500
chunk_overlap = 30
text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
split_documents = text_splitter.split_documents(documents)
split_documents[:4]

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
