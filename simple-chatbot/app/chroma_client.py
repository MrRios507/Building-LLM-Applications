import os
import time

import chromadb

CHROMA_HOST = os.getenv("CHROMA_HOST", "localhost")
CHROMA_PORT = os.getenv("CHROMA_PORT", "8001")
COLLECTION_NAME = os.getenv("CHROMA_COLLECTION", "tourism_collection")

def get_chroma_client():
    client = chromadb.HttpClient(
        host=CHROMA_HOST,
        port=CHROMA_PORT
    )

    # Waiting for Chroma is available
    for attempt in range(10):
        try:
            client.heartbeat()
            print("Connecting to ChromaDB...")

            return client
        except Exception:
            if attempt == 9:
                raise

            print("Waiting to ChromaDB...")
            time.sleep(2)
    raise RuntimeError("Cannot connected to ChromaDB.")

def get_collection():
    client = get_chroma_client()

    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"description": "Tourism Collection"}
    )
