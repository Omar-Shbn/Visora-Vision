import traceback

try:
    from langchain_community.vectorstores import Chroma
    from langchain_community.embeddings import HuggingFaceEmbeddings
    from langchain_community.llms import Ollama
    from langchain.chains import RetrievalQA
    
    DB_DIR = "./chroma_db"
    print("Loading Vector Database...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = Chroma(persist_directory=DB_DIR, embedding_function=embeddings)
    
    llm = Ollama(model="qwen2.5vl:7b")
    print("AI load successful")
except Exception as e:
    print(traceback.format_exc())
