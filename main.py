from fastapi import FastAPI
from pydantic import BaseModel
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

app = FastAPI(title="MLOps RAG Service", version="1.0")

# 1. Initialize the Embedding Model 
# (This will download a ~80MB model to your machine the very first time it runs)
print("Loading embedding model...")
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# 2. Create a Dummy Knowledge Base (The "Retrieval" part of RAG)
# In production, this data would come from S3, a database, or Confluence.
dummy_data = [
    Document(page_content="EdgeVerve provides enterprise software solutions, including the Finacle banking platform."),
    Document(page_content="An MLOps Engineer bridges the gap between machine learning development and production deployment."),
    Document(page_content="Bhaskar is architecting a highly available RAG pipeline using Docker, FastAPI, and Jenkins.")
]
# Build the vector database in memory
vector_db = FAISS.from_documents(dummy_data, embeddings)

# 3. Define the Input Data Schema using Pydantic (Crucial for API validation)
class QueryRequest(BaseModel):
    question: str

@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "Model API is running."}

# 4. Create the new AI Endpoint
@app.post("/retrieve")
def retrieve_context(request: QueryRequest):
    # Search the vector database for the sentence most similar to the user's question
    results = vector_db.similarity_search(request.question, k=1)
    
    best_match = results[0].page_content if results else "No relevant context found."
    
    return {
        "user_question": request.question,
        "retrieved_information": best_match,
        "status": "success"
    } 