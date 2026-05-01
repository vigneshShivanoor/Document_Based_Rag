from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore

# ---------------- CONFIG ----------------
PDF_PATH = r"C:\Users\VIGNESH\OneDrive\Desktop\Rag\Document.pdf"

QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "Docuement"
EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"
# ----------------------------------------

def ingest_pdf():
    print("📄 Loading PDF...")
    loader = PyPDFLoader(PDF_PATH)
    documents = loader.load()

    print("✂️ Splitting documents...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )
    chunks = splitter.split_documents(documents)

    print(f"🧠 Creating embeddings ({EMBEDDING_MODEL})...")
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    print("📦 Storing vectors in Qdrant...")
    QdrantVectorStore.from_documents(
        documents=chunks,
        embedding=embeddings,
        url=QDRANT_URL,
        collection_name=COLLECTION_NAME,
    )

    print("✅ Ingestion completed successfully")

if __name__ == "__main__":
    ingest_pdf()
