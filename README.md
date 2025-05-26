# RAG Q\&A Application Documentation

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [Directory Structure](#directory-structure)
4. [Backend (FastAPI)](#backend-fastapi)

   * API Endpoints
   * Docker Setup
5. [Frontend (Streamlit)](#frontend-streamlit)

   * Features
   * Docker Setup
6. [Running Locally with Docker Compose](#running-locally-with-docker-compose)
7. [Deployment on Render.com](#deployment-on-rendercom)
8. [Environment Variables](#environment-variables)
9. [Final Deployment URLs](#final-deployment-urls)
10. [Troubleshooting](#troubleshooting)
11. [License](#license)

---

## 🎥 Demo Walkthrough

<video width="800" controls>
  <source src="https://raw.githubusercontent.com/Laxman0415/rag-pipeline-implementation/blob/master/rag-pipeline.webm" type="video/webm">
  Your browser does not support the video tag.
</video>

---

## Project Overview

This Retrieval-Augmented Generation (RAG) Q\&A Application enables users to ingest documents, store their embeddings using FAISS, and query the knowledge base through a natural language interface. It includes a FastAPI backend and a Streamlit frontend, both deployed as web services on Render.com.

---

## Architecture

* **Backend:** FastAPI REST API for document ingestion, vector storage, retrieval, and response generation.
* **Frontend:** Streamlit UI that interacts with the backend via REST APIs.
* **Vector Store:** FAISS for high-performance vector similarity search.
* **Deployment:** Hosted on Render.com as two separate web services.

---

## Directory Structure

```
project-root/
├── .gitignore
├── LICENSE
├── README.md
├── docker-compose.yml                      # For local development/testing
├── frontend                                # Streamlit frontend
│   ├── .env
│   ├── Dockerfile                          # Front End User Interaction
│   ├── requirements.txt        
│   └── streamlit_app.py
├── src                                     # FastAPI backend
    ├── .dockerignore
    ├── Dockerfile                          # Backend uvicorn services
    ├── config
    │   ├── __init__.py
    │   └── faiss_index_metadata.json
    ├── data_generation
    │   ├── __init__.py
    │   └── response_generation.py
    ├── data_ingestion
    │   ├── __init__.py
    │   └── document_ingestion.py
    ├── data_retrieval
    │   ├── __init__.py
    │   └── retriever.py
    ├── document_selection
    │   ├── __ini__.py
    │   └── doc_selection.py
    ├── env
    ├── faiss_index
    │   ├── 0.faiss
    │       ├── index.faiss
    │       └── index.pkl       
    ├── main.py                              # FastAPI Services
    ├── notebook
    │   └── rag.ipynb
    ├── prompt_registry
    │   └── knowledge_base.txt
    ├── requirements.txt
    └── utility
        ├── __init__.py
        ├── custom_exception.py
        ├── custom_logger.py
        └── utils.py
```

---

## Backend (FastAPI)

### API Endpoints

| Endpoint         | Method | Description                          |
| ---------------- | ------ | ------------------------------------ |
| `/rag/`          | GET    | Health check                         |
| `/rag/ingest`    | POST   | Ingest a document by URL             |
| `/rag/documents` | GET    | List all ingested documents          |
| `/rag/query`     | POST   | Ask a question on ingested documents |

### Docker Setup

```bash
# Build backend Docker image
cd src
docker build -t rag-backend .

# Run backend container
docker run -p 8000:8000 rag-backend
```

---

## Frontend (Streamlit)

### Features

* Upload and ingest documents
* Ask natural language queries
* Display LLM-generated answers

### Docker Setup

```bash
# Build frontend Docker image
cd frontend
docker build -t rag-frontend .

# Run frontend container
# Replace BACKEND_URL with your actual backend URL
docker run -p 8501:8501 -e BACKEND_URL="http://localhost:8000" rag-frontend
```

---

## Running Locally with Docker Compose

### Prerequisites

* Docker
* Docker Compose

### Sample `docker-compose.yml`

```yaml
version: "3.9"
services:
  backend:
    build:
      context: ./src
    container_name: rag-backend
    ports:
      - "8000:8000"

  frontend:
    build:
      context: ./frontend
    container_name: rag-frontend
    ports:
      - "8501:8501"
    environment:
      - BACKEND_URL=http://backend:8000
    depends_on:
      - backend
```

### Run with Docker Compose

```bash
docker-compose up --build --force-recreate --no-deps --remove-orphans
```

### Access Locally

* **Frontend (Streamlit):** [http://localhost:8501](http://localhost:8501)
* **Backend (FastAPI):** [http://localhost:8000](http://localhost:8000)

---

## Deployment on Render.com

### Backend (FastAPI)

* **Service Type:** Web Service
* **Build Command:** `pip install -r requirements.txt`
* **Start Command:** `uvicorn main:app --host 0.0.0.0 --port 8000`
* **Environment:** Python 3.x
* **URL:** `https://rag-backend-service.onrender.com` (example)

### Frontend (Streamlit)

* **Service Type:** Web Service
* **Build Command:** `pip install -r requirements.txt`
* **Start Command:** `streamlit run streamlit_app.py --server.port=10000 --server.address=0.0.0.0`
* **Environment Variable:**

  * `BACKEND_URL=https://rag-backend-service.onrender.com`
* **URL:** `https://rag-frontend-app.onrender.com` (example)

---

## Environment Variables

### Frontend

* `BACKEND_URL`: The full backend URL deployed on Render.com

### Backend

* Configure using `env` or Render dashboard:

  * `GROQ_API_KEY`
  * `GOOGLE_API_KEY`
  * Other custom configurations

---

## Final Deployment URLs

### Deployment 1: Streamlit Cloud + Render

* **Frontend (Streamlit Community Cloud):** [https://rag-frontend.streamlit.app/](https://rag-frontend.streamlit.app/)
* **Backend (Render Web Service):** [https://rag-pipeline-backend.onrender.com/rag](https://rag-pipeline-backend.onrender.com/rag)

### Deployment 2: Fully on Render

* **Frontend (Render Web Service):** [https://rag-pipeline-frontend.onrender.com/](https://rag-pipeline-frontend.onrender.com/)
* **Backend (Render Web Service):** [https://rag-pipeline-backend.onrender.com/rag](https://rag-pipeline-backend.onrender.com/rag)

---

## Troubleshooting

| Issue                       | Solution                                                             |
| --------------------------- | -------------------------------------------------------------------- |
| `Connection refused`        | Ensure `BACKEND_URL` in frontend matches deployed backend Render URL |
| `Failed to fetch documents` | Backend must be running and publicly accessible                      |
| `env not found`            | Set env variables in Render dashboard's Environment section           |
| `CORS errors`               | Add CORSMiddleware in FastAPI to allow frontend origin               |

---

## License

Specify your license here (e.g., MIT License).

---
