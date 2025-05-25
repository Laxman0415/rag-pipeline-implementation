from langchain_groq import ChatGroq
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv, find_dotenv
import sys
import os
import json

from utility.custom_logger import logger
from utility.custom_exception import CustomException

# laoding env file for API KEY
env_path = find_dotenv(
    filename="env",
    raise_error_if_not_found=True
)

if env_path:
    load_dotenv(env_path)

def get_groq_chat_model(model_name ="llama3-8b-8192" ):
    """
    # Improting/Loading Language Model
    # https://console.groq.com/playground
    # Load Chat Model
    """
    try:
        llm_groq = ChatGroq(model=model_name)

        return llm_groq
    
    except Exception as e:
        raise CustomException(e,sys)
    
def get_gemini_chat_model(model_name ="gemini-1.5-pro" ):
    """
    """
    try:
        llm_gemini=ChatGoogleGenerativeAI(model=model_name)

        return llm_gemini
    
    except Exception as e:
        raise CustomException(e,sys)

def get_hf_embedding_model(model_name = "BAAI/bge-small-en"):
    """
    # Improting/Loading Embedding Model
    # Load Embedding Model

    # Not Requires HF API Key because it is a Public Repo

    # https://huggingface.co/BAAI
    """
    try:
        mdl_name = model_name
        model_kwargs = {"device":"cpu"}  # Where the model need to be load my model , CPU/GPU Machine
        encode_kwargs = {"normalize_embeddings":True}   # For faster embedding and search with normaalize for now 
        hf_embeddings = HuggingFaceBgeEmbeddings(
            model_name =  mdl_name , model_kwargs = model_kwargs , encode_kwargs = encode_kwargs
        )
        return hf_embeddings
    except Exception as e:
        raise CustomException(e,sys)

def get_google_embedding_model(model_name = "models/embedding-001"):
    """
    """
    try:
        google_embeddings = GoogleGenerativeAIEmbeddings(model=model_name)
        return google_embeddings
    except Exception as e:
        raise CustomException(e,sys)
    
def load_metadata(METADATA_FILE):
    """Loading metadata of Prestored Knowledge Base to check if it exists; otherwise, return an empty dictionary."""
    if os.path.exists(METADATA_FILE):
        with open(METADATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_metadata(metadata,METADATA_FILE):
    """Saving metadata of Knowledge Base to a file faiss_index_metadata.json"""
    with open(METADATA_FILE, "w") as f:
        json.dump(metadata, f, indent=4)