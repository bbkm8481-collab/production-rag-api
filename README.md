

# 🚀 MLOps Project: Production-Grade RAG API with CI/CD

**Objective:** Build a scalable, highly available Retrieval-Augmented Generation (RAG) system, containerize it optimally, and automate its deployment lifecycle using Jenkins CI/CD.

## Phase 1: AI Foundation (FastAPI + RAG)
Instead of a standard Jupyter Notebook, we built the ML model directly into a high-speed web framework (FastAPI) to simulate enterprise microservices.

**1. Environment Setup:**
```bash
python -m venv venv
source venv/bin/activate
pip install fastapi uvicorn langchain sentence-transformers faiss-cpu pydantic
```

**2. The Application Code (`main.py`):**
We implemented `HuggingFaceEmbeddings` and Meta's `FAISS` vector database to allow the LLM to retrieve context. We also used Pydantic `BaseModel` for strict API payload validation.

```python
from fastapi import FastAPI
from pydantic import BaseModel
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

app = FastAPI(title="MLOps RAG Service", version="1.0")

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
```

---

## Phase 2: Containerization & Optimization (Docker)
Machine Learning libraries are massive. We encountered a storage bloat issue where standard PyTorch installations consumed gigabytes of disk space.

**1. Docker Cleanup (To reclaim space):**
```bash
docker system prune -a --volumes
```

**2. MLOps Optimization (The CPU-only Trick):**
We rewrote the `Dockerfile` to force the installation of the lightweight, CPU-only version of PyTorch, drastically reducing the image size and build time.

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .

# PRO MLOPS TRICK: Install the CPU-only version of PyTorch first!
RUN pip install torch --index-url https://download.pytorch.org/whl/cpu

RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## Phase 3: Version Control & The Git Size Limit Fix
We attempted to push the code to GitHub but hit a fatal error: the hidden `venv` folder containing 400MB+ AI libraries was being tracked by Git, violating GitHub's 100MB file limit. 

**The Fix (Erasing Git's memory and ignoring dependencies):**
```bash
# 1. Delete corrupted git history
rm -rf .git

# 2. Create a bulletproof .gitignore
echo "venv/" > .gitignore
echo ".venv/" >> .gitignore
echo "__pycache__/" >> .gitignore

# 3. Start fresh and push safely
git init
git add .
git commit -m "Initial commit: FastAPI RAG with Docker and Jenkinsfile"
git branch -M main
git remote add origin https://github.com/bbkm8481-collab/production-rag-api.git
git push -u origin main --force
```
*Result:* We successfully pushed a clean, professional 2.87 KB repository instead of uploading gigabytes of redundant dependencies.

---

## Phase 4: CI/CD Automation (Jenkins)
We wrote a declarative pipeline to ensure that every time the model or API code is updated, it is automatically tested, containerized, and tagged.

**The `Jenkinsfile`:**
```groovy
pipeline {
    agent any
    environment {
        IMAGE_NAME = "mlops-rag-api"
        IMAGE_TAG = "v${env.BUILD_ID}"
    }
    stages {
        stage('Setup Environment') {
            steps {
                echo "Setting up Python virtual environment..."
                sh '''
                python3 -m venv venv
                source venv/bin/activate
                pip install -r requirements.txt
                '''
            }
        }
        stage('Build Docker Image') {
            steps {
                echo "Building Docker Image: ${IMAGE_NAME}:${IMAGE_TAG}"
                sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
                sh "docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${IMAGE_NAME}:latest"
            }
        }
        stage('Security & Cleanup') {
            steps {
                echo "Cleaning up dangling images to save space..."
                sh "docker system prune -f"
            }
        }
    }
    post {
        success {
            echo "✅ Pipeline Succeeded! The RAG API is containerized and ready for deployment."
        }
        failure {
            echo "❌ Pipeline Failed! Please check the logs."
        }
    }
}
```

**Final Validation:** The Jenkins job was hooked up to the GitHub repository. Upon building, Jenkins successfully cloned the repo, established the virtual environment, and executed the dependency installations exactly as defined in the automated pipeline.

***
