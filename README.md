
# Production-Grade RAG API with Automated MLOps Pipeline

This repository contains a full-stack MLOps implementation of a Retrieval-Augmented Generation (RAG) service. It demonstrates the transition from a "local ML script" to a scalable, containerized, and monitored production microservice.

## Project Architecture
The system is built with a focus on **High Availability** and **Observability**:
1. **AI Service:** FastAPI application serving a RAG pipeline using LangChain, HuggingFace Embeddings, and FAISS.
2. **CI/CD:** Jenkins pipeline for automated testing, Docker image optimization, and zero-downtime deployment.
3. **Observability Stack:** Prometheus for metrics collection and Grafana for real-time telemetry (latency, request counts, system health).

---

## Tech Stack
* **Language:** Python 3.10+
* **ML Frameworks:** LangChain, Sentence-Transformers, FAISS
* **API Framework:** FastAPI (Pydantic for data validation)
* **DevOps:** Docker, Docker Compose, Jenkins
* **Monitoring:** Prometheus, Grafana, Prometheus-FastAPI-Instrumentator

---

## 🌟 Key MLOps Features

### 1. Optimized Containerization
* **CPU-Only Optimization:** Custom Dockerfile configurations to install CPU-specific PyTorch builds, reducing image size by ~80% and improving deployment speed.
* **Multi-Stage thinking:** Ensuring environment consistency across development and production.

### 2. Automated CI/CD Pipeline
* **Jenkins Integration:** Fully automated pipeline that handles:
    * Dependency management via Virtual Environments.
    * Automated Docker builds and version tagging.
    * Continuous Deployment: Automatically replaces old containers with new builds upon successful testing.

### 3. Real-time Telemetry & Monitoring
* **Prometheus Instrumentation:** The API exposes a `/metrics` endpoint tracking request latency and throughput.
* **Grafana Dashboards:** Custom visualization of API health and model inference spikes, allowing for proactive system management.

---

## 🚀 Getting Started

### Prerequisites
* Docker & Docker Compose
* Jenkins (local or server)
* Python 3.9+

### Setup & Deployment
1. **Clone the repo:**
   ```bash
   git clone [https://github.com/bbkm8481-collab/production-rag-api.git](https://github.com/bbkm8481-collab/production-rag-api.git)
   cd production-rag-api
Launch the Monitoring Stack:

Bash
docker-compose up -d
Run the API (Manual):

Bash
docker build -t mlops-rag-api .
docker run -p 8000:8000 mlops-rag-api
