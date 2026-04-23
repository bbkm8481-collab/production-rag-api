# Simple FastAPI + Sentence Transformers + FAISS

from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

app = FastAPI()

demo_sentences = [
    "I love machine learning.",
    "FastAPI is great for APIs.",
    "Python is a versatile language.",
    "Transformers are powerful for NLP.",
    "FAISS enables fast similarity search."
]

model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(demo_sentences)
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(np.array(embeddings, dtype=np.float32))

class Query(BaseModel):
    text: str

@app.post("/search")
def search(query: Query):
    query_embedding = model.encode([query.text])
    D, I = index.search(np.array(query_embedding, dtype=np.float32), k=2)
    results = [demo_sentences[i] for i in I[0]]
    return {"query": query.text, "results": results}
