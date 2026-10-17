from app.chroma_client import get_collection

def retrieve_context(question: str, top_k: int = 3):
    collection = get_collection()

    if collection.count() == 0:
        return []

    results = collection.query(
        query_texts=[question],
        n_results=top_k
    )

    results_text = results['documents'][0][0]
    return results_text
