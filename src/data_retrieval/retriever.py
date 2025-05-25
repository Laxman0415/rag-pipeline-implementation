from utility.utils import get_google_embedding_model, load_metadata
from langchain_community.vectorstores import FAISS
from utility.custom_logger import logger
from utility.custom_exception import CustomException
import os
import sys

current_path = os.path.dirname(os.path.abspath(__name__))
metadata_path = os.path.join(current_path,"config","faiss_index_metadata.json")
metadata_file_path = os.path.abspath(metadata_path)

index_path = os.path.join(current_path,"faiss_index")
index_dir_path = os.path.abspath(index_path)

logger.info(f"Index Dir Path : {index_dir_path}")
logger.info(f"Metadata File Path : {metadata_file_path}")

class DataRetriever:

    def __init__(self,web_doc_url):
        logger.info(f"Selected Document URL is : {web_doc_url=}")
        self.web_doc_url = web_doc_url

    def get_retriver(self):
        try:
            pre_stored_metadata_config =  load_metadata(metadata_file_path)
            # Generating the unique index filename for this Knowledge Base
            index_filename_data = pre_stored_metadata_config.get(self.web_doc_url,{}) 
            logger.info(f"{index_filename_data=}")
            index_filename = index_filename_data.get("vector_store_index",None)  # Assigning a new index if not found
            if index_filename != None:
                index_path = os.path.join(index_dir_path, index_filename)

                if os.path.exists(index_path):
                    logger.info(f"Loading existing FAISS index for {self.web_doc_url}...")
                    pre_stored_knowledge_base_flag = True
                    logger.info("Knowledge Base Was Already Ingested in DB")
                    embedding = get_google_embedding_model()
                    vector_store = FAISS.load_local(index_path, embedding,allow_dangerous_deserialization=True)
                    retriever = vector_store.as_retriever()
                    return retriever #, vector_store
                else:
                    logger.error(f"Selected Document is Not Present in VectorDB")
                    return None
            else:
                logger.error(f"Selected Document is Not Present in VectorDB")
                return None
        except Exception as e:
            raise CustomException(e,sys)
        
if __name__ == "__main__":
    retriever_obj = DataRetriever("https://www.gutenberg.org/cache/epub/13421/pg13421.txt")
    retriever = retriever_obj.get_retriver()