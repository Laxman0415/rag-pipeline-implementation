import os
import sys
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

from utility.custom_logger import logger
from utility.custom_exception import CustomException

from utility.utils import load_metadata, get_google_embedding_model , save_metadata 


current_path = os.path.dirname(os.path.abspath(__name__))
metadata_path = os.path.join(current_path,"config","faiss_index_metadata.json")
metadata_file_path = os.path.abspath(metadata_path)

index_path = os.path.join(current_path,"faiss_index")
index_dir_path = os.path.abspath(index_path)

class DocumentIngestion:

    def __init__(self,web_doc_url):
        logger.info(f"Document URL is : {web_doc_url=}")
        self.web_doc_url = web_doc_url
           
    def get_raw_document(self):
        """        
        """
        try:
            logger.info("Loading Uploaded Document")
            loader = UnstructuredURLLoader(urls=[self.web_doc_url])
            # Load the document
            documents = loader.load()
            logger.info(f"Uploaded Document : {self.web_doc_url} is Successfully Loaded")
            return documents
        
        except Exception as e:
            raise CustomException(e,sys)
        
    def document_chunking(self):
        """
            # Chunking
            # If Chunking is not require , we can directly do and store the embeddings
            # Chunked Doc , Just a Way to Arrange the metadata 
        """
        try:

            text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1000,chunk_overlap =200)
            raw_document = self.get_raw_document()
            logger.info("Chunking Started")
            chunked_data = text_splitter.split_documents(raw_document)
            logger.info("Chunking Completed")
            return chunked_data
        
        except Exception as e:
            raise CustomException(e,sys)
        
    @staticmethod    
    def vector_store_save_document(chunked_data,embedding,index_path):
        """
        # Configuring VECTOR DB
        # WE are using FAISS (In Memory Database) Facebook AI Similarity Search 

        # It was a mathematical algorithm to perform indexing on top of data

        # FAISS.from_documents(documents=docs,embedding=hf_embeddings)
        """
        try:
            vector_store = FAISS.from_documents(documents=chunked_data,embedding=embedding)
            vector_store.save_local(index_path) 
        except Exception as e:
            raise CustomException(e,sys)
    

    def run_data_ingestion(self):
        try:
            pre_stored_metadata_config =  load_metadata(metadata_file_path)
            pre_stored_knowledge_base_flag = False
            # Generating the unique index filename for this Knowledge Base
            index_filename_data = pre_stored_metadata_config.get(self.web_doc_url,{}) 
            index_filename = index_filename_data.get("vector_store_index",f"{len(pre_stored_metadata_config)}.faiss")  # Assigning a new index if not found
            index_path = os.path.join(index_dir_path, index_filename)
            logger.info(f"index path is: {index_path=}")

            if not os.path.exists(index_dir_path):
                os.makedirs(index_dir_path)  # Creating a directory as it doesn't exist

            if os.path.exists(index_path):
                logger.info(f"Loading existing FAISS index for {self.web_doc_url}...")
                pre_stored_knowledge_base_flag = True
                logger.info("Knowledge Base was Already Ingested in DB")
            else:
                logger.info(f"Generating new FAISS index for newly injested Book : {self.web_doc_url}...")
                logger.info("Starting the Data Ingestion Process from Scratch")
                queried_web_doc_metadata = {}
                queried_web_doc_metadata["vector_store_index"] = index_filename
                chunked_data = self.document_chunking()
                google_embedding = get_google_embedding_model()
                DocumentIngestion.vector_store_save_document(chunked_data, google_embedding,index_path)
                
                pre_stored_metadata_config[self.web_doc_url] = queried_web_doc_metadata
                logger.info(f"{pre_stored_metadata_config=}")
                save_metadata(pre_stored_metadata_config,metadata_file_path)
            
            return pre_stored_knowledge_base_flag
        except Exception as e:
            raise CustomException(e,sys)


if __name__ == "__main__":
    document_ingestion = DocumentIngestion("https://www.gutenberg.org/cache/epub/13421/pg13421.txt")
    document_ingestion.get_raw_document()