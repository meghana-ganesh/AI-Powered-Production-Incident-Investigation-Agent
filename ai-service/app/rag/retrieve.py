from pathlib import Path

from langchain_chroma import Chroma

from langchain_ollama import OllamaEmbeddings



BASE_DIR = Path(__file__).resolve().parents[2]

VECTOR_STORE_DIR = BASE_DIR / "data" / "chroma_db"

EMBEDDING_MODEL = "nomic-embed-text"
COLLECTION_NAME = "incident_knowledge_base"


def get_vector_store():
    """Open the existing persistent vector database."""

    embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)

    vector_store = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=str(VECTOR_STORE_DIR),
    )

    return vector_store


def retrieve_relevant_documents(query: str, k: int = 3):
    """Retrieve the top-k document chunks relevant to a query."""

    if not query or not query.strip():
        raise ValueError("Query must not be empty.")

    # Avoid requesting zero or a negative number of results.
    if k < 1:
        raise ValueError("k must be at least 1.")

    vector_store = get_vector_store()

    # Search for the k most similar chunks using vector similarity.
    # Each result contains a Document and a distance score.
    results = vector_store.similarity_search_with_score(
        query=query,
        k=k,
    )

    # Convert LangChain Document objects into simple dictionaries
    # that can later be passed to the investigation workflow or API.
    retrieved_documents = []

    for document, distance in results:
        retrieved_documents.append(
            {
                # The retrieved text chunk.
                "content": document.page_content,

                # The original Markdown file path from ingestion.
                "source": document.metadata.get("source", "unknown"),

                # Approximate character position within the source document.
                "start_index": document.metadata.get("start_index", 0),

                # Chroma's distance score; lower generally means closer.
                "distance": float(distance),
            }
        )

    # Return the retrieved chunks with their source information.
    return retrieved_documents


# Run this example only when executing this file directly.
if __name__ == "__main__":

    query = (
        "The API is slow and requests time out because "
        "the database connection pool is exhausted."
    )

    # Retrieve the three most similar chunks from the knowledge base.
    results = retrieve_relevant_documents(query, k=3)

    for index, result in enumerate(results, start=1):
        print(f"\n--- Result {index} ---")
        print(f"Source: {result['source']}")
        print(f"Distance: {result['distance']:.4f}")
        print(f"Content:\n{result['content']}")