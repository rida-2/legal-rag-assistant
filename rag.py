import chromadb

from sentence_transformers import SentenceTransformer

from flashrank import Ranker, RerankRequest


# ------------------------------------
# Embedding model
# ------------------------------------

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

# ------------------------------------
# FlashRank reranker
# ------------------------------------

ranker = Ranker()

# ------------------------------------
# ChromaDB
# ------------------------------------

client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_or_create_collection(
    name="legal_cases"
)


# ------------------------------------
# Add document
# ------------------------------------

def add_document(chunk_id, text, metadata):

    embedding = model.encode(text).tolist()

    try:

        collection.add(
            ids=[chunk_id],
            embeddings=[embedding],
            documents=[text],
            metadatas=[metadata]
        )

    except:
        pass


# ------------------------------------
# Token optimization
# ------------------------------------

def clean_chunk(text):

    text = text.replace("\n", " ")

    text = " ".join(text.split())

    MAX_CHARS = 1500

    return text[:MAX_CHARS]


# ------------------------------------
# Search + rerank
# ------------------------------------

def search_documents(query, n_results=5):

    query_embedding = model.encode(
        query
    ).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=20
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    if len(documents) == 0:

        return {
            "documents": [[]],
            "metadatas": [[]]
        }

    passages = []

    for idx, (doc, meta) in enumerate(
            zip(documents, metadatas)):

        passages.append({
            "id": idx,
            "text": clean_chunk(doc),
            "meta": meta
        })

    rerank_request = RerankRequest(
        query=query,
        passages=passages
    )

    reranked = ranker.rerank(
        rerank_request
    )

    top_documents = []
    top_metadatas = []

    for item in reranked[:n_results]:

        top_documents.append(
            clean_chunk(item["text"])
        )

        top_metadatas.append(
            item["meta"]
        )

    return {
        "documents": [top_documents],
        "metadatas": [top_metadatas]
    }


# ------------------------------------
# CRUD
# ------------------------------------

def delete_document(file_name):

    collection.delete(
        where={
            "file": file_name
        }
    )


def get_all_documents():

    docs = collection.get()

    files = []

    for meta in docs["metadatas"]:

        if meta["file"] not in files:

            files.append(meta["file"])

    return files


# ------------------------------------
# DB stats
# ------------------------------------

def get_document_count():

    docs = collection.get()

    return len(docs["ids"])