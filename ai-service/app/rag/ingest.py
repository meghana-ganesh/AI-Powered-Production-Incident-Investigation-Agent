from pathlib import Path

from langchain_chroma import Chroma #vectordb
from langchain_ollama import OllamaEmbeddings #embeddings - convert text to numerical vectors locally
from langchain_text_splitters import RecursiveCharacterTextSplitter #divides long docs into smallerchunks

BASE_DIR = Path(__file__).resolve().parents[2]
KNOWLEDGE_BASE_DIR = BASE_DIR / "knowledge_base"
VECTOR_STORE_DIR = BASE_DIR / "data" / "chroma_db"

EMBEDDING_MODEL = "nomic-embed-text"

#logical name for the collection inside chroma

COLLECTION_NAME = "incident_knowledge_base"

def load_documents():
    """Read markdown files from the knowledge base"""

    documents = []

    for file_path in KNOWLEDGE_BASE_DIR.rglob("*.md"): #rgglob searches the knowledge base folder and all its subfolders

        content = file_path.read_text(encoding="utf-8").strip()
        if not content:
            continue
        #save the documents and its source path
        documents.append(
            {
                "content": content,
                "source": str(file_path.relative_to(BASE_DIR)),
            }
        )

    return documents

def build_vector_store():
    """Split documents into chunks, embed them, and save them in Chroma."""

    documents = load_documents()

    if not documents:
        raise ValueError(f"No documents found in {KNOWLEDGE_BASE_DIR}")
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 600,
        chunk_overlap = 100,
        add_start_index = True
    )

    texts = []
    metadatas = []

    for document in documents:
        #split doc into smaller pieces and store them in texts and metadatas lists
        chunks = splitter.create_documents([document["content"]], metadatas=[{"source": document["source"]}])
        for chunk in chunks:
            texts.append(chunk.page_content)
            metadatas.append({**chunk.metadata, "start_index": chunk.metadata.get("start_index", 0)})

    #initialize local embedding model through Ollama
    embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)

    #connect to persistent chroma db
    vector_store = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=VECTOR_STORE_DIR
    )

    #Get IDs of previously indexed chunks in this collection
    existing_ids = vector_store.get()["ids"]
    #chroma uses embedding func to generate their vectors
    vector_store.add_texts(
        texts=texts,
        metadatas=metadatas,
    )

    return len(documents),len(texts)

if __name__ == "__main__":
    document_count, chunk_count = build_vector_store()
    print(f"documents loaded:{document_count}")
    print(f"Chunks indexed: {chunk_count}")
    print(f"Vector database: {VECTOR_STORE_DIR}")




