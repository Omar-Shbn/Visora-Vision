import os
import glob
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

PDF_DIR = "../"
DB_DIR = "./chroma_db"

def ingest():
    pdf_paths = glob.glob(os.path.join(PDF_DIR, "*.pdf"))
    if not pdf_paths:
        print(f"No PDFs found in {PDF_DIR}")
        return

    print(f"Found {len(pdf_paths)} PDF(s): {[os.path.basename(p) for p in pdf_paths]}")

    all_splits = []
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

    for pdf_path in pdf_paths:
        print(f"Loading {os.path.basename(pdf_path)}...")
        loader = PyPDFLoader(pdf_path)
        docs = loader.load()
        splits = text_splitter.split_documents(docs)
        print(f"  -> {len(splits)} chunks")
        all_splits.extend(splits)

    print(f"\nTotal chunks across all documents: {len(all_splits)}")
    print("Initializing embeddings...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    print(f"Writing to Vector DB at {DB_DIR}...")
    vectorstore = Chroma.from_documents(documents=all_splits, embedding=embeddings, persist_directory=DB_DIR)

    print("Ingestion complete! Vector database is ready.")

if __name__ == "__main__":
    ingest()
