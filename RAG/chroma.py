import chromadb
from chromadb.config import Settings

# ChromaDB management functions

def get_chroma_client(db_path="./chroma_store"):
    return chromadb.PersistentClient(
        path=db_path,
        settings=Settings(anonymized_telemetry=False)
    )

def get_or_create_collection(client, collection_name):
    return client.get_or_create_collection(collection_name)

# Add embeddings to ChromaDB

def add_embeddings(collection, chunks, embeddings, ids, metadatas):
    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=chunks,
        metadatas=metadatas
    )

# Delete embeddings from ChromaDB by ids

def delete_embeddings(collection, ids):
    collection.delete(ids=ids)

# Search ChromaDB

def search_chroma(collection, query_embedding, top_k=3):
    res = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    return res['documents'][0] if 'documents' in res and res['documents'] else []