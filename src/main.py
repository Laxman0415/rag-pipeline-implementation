from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from data_ingestion.document_ingestion import DocumentIngestion
from document_selection.doc_selection import ListIngestedDocuments
from data_generation.response_generation import InvokeResponseGeneration
from utility.custom_exception import CustomException
from utility.custom_logger import logger
from pydantic import BaseModel
import uvicorn

import sys


# Initialize FastAPI app
app = FastAPI(title="RAG Q&A", summary="RAG API")

# CORS for frontend compatibility
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Defining API Router with prefix "/rag" and tag "API"
router = APIRouter(prefix="/rag", tags=["API"])

class IngestRequest(BaseModel):
    document_web_url: str

class QueryRequest(BaseModel):
    question: str
    selected_document_name: str

# ---- API Endpoints ----

@router.get("/")
async def index():
    return "Hello"

@router.post("/ingest")
async def ingest_document(payload: IngestRequest):
    """
    Ingest a document: read content, generate embeddings, and store them.
    """
    try:
        logger.info("New Data Ingestion Request Recieved.")
        document_ingestion = DocumentIngestion(payload.document_web_url)
        pre_stored_knowledge_base_flag = document_ingestion.run_data_ingestion()
        if pre_stored_knowledge_base_flag:
            return {"message": "Document Was Already Ingested in DB", "doc_name": payload.document_web_url, "status_code":200, "status":"Success"}
        else:
            logger.info("Data Ingestion Completed Successfully.")
            return {"message": "Document ingested", "doc_name": payload.document_web_url, "status_code":200, "status":"Success"}
    except Exception as e:
        logger.error("Data Ingestion Failed")
        return {"message":CustomException(e,sys).error_message,"doc_name": payload.document_web_url, "status_code":500, "status":"Failed"}


@router.get("/documents")
async def list_documents():
    """
    List all available documents.
    
    """
    try:
        logger.info("Listing All the Ingested Documents")
        list_ingested_documents = ListIngestedDocuments()
        ingested_document = list_ingested_documents.get_ingested_document()
        logger.info(f"Ingested Documents are : {ingested_document}")
        return {"message": ingested_document, "status_code":200, "status":"Success"}
    except Exception as e:
        logger.error("Listing Ingested Documents Fails")
        return {"message": CustomException(e,sys).error_message, "status_code":500, "status":"Failed"}


@router.post("/query")
async def query_rag(request: QueryRequest):
    """
    RAG: Retrieve relevant chunks and generate an answer.
    """
    try:
        
        if not request.question and not request.selected_document_name:
            raise HTTPException(status_code=400, detail="Question & Doscument is required")
        logger.info("New Query Recived for Q&A.")
        logger.info(f"User Query is : {request.question}")
        logger.info(f"User Queried Document is {request.selected_document_name}")
        invoke = InvokeResponseGeneration(request.question,request.selected_document_name)
        response = invoke.invoke_chain()
        if response != None:
            logger.info("Answer Generated Successfully.")
            return {"message": response, "question": request.question, "status_code":200, "status":"Success"}
        else:
            logger.info("Selected Document is Not Present in VectorDB")
            return {"message": "Selected Document is Not Present in VectorDB", "question": request.question, "status_code":500, "status":"Failed"}

    except Exception as e:
        logger.error("Error while Querying to System.")
        return {"message": CustomException(e,sys).error_message,"question": request.question, "status_code":500, "status":"Failed"}
    
# Include the router in the FastAPI app
app.include_router(router)

# -------------------------- Run Uvicorn Server --------------------------
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)