from fastapi import FastAPI
from pydantic import BaseModel
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from prometheus_fastapi_instrumentator import Instrumentator 

app = FastAPI(title="MLOps RAG Service", version="1.0")

Instrumentator().instrument(app).expose(app)

print("Loading embedding model...")
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

dummy_data = [
    Document(page_content="EdgeVerve provides enterprise software solutions, including the Finacle banking platform."),
    Document(page_content="An MLOps Engineer bridges the gap between machine learning development and production deployment."),
    Document(page_content="Bhaskar is architecting a highly available RAG pipeline using Docker, FastAPI, and Jenkins.")
]
vector_db = FAISS.from_documents(dummy_data, embeddings)

class QueryRequest(BaseModel):
    question: str

@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "Model API is running."}

@app.post("/retrieve")
def retrieve_context(request: QueryRequest):
    results = vector_db.similarity_search(request.question, k=1)
    best_match = results[0].page_content if results else "No relevant context found."
    return {
        "user_question": request.question,
        "retrieved_information": best_match,
        "status": "success"
    }
