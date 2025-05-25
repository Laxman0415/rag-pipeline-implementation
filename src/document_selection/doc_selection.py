from utility.utils import load_metadata
from dotenv import load_dotenv, find_dotenv
from utility.custom_exception import CustomException
from utility.custom_logger import logger
import os
import sys


# laoding env file for API KEY
env_path = find_dotenv(
    filename="env",
    raise_error_if_not_found=True
)

if env_path:
    load_dotenv(env_path)

current_path = os.path.dirname(os.path.abspath(__name__))
metadata_path = os.path.join(current_path,"config","faiss_index_metadata.json")
metadata_file_path = os.path.abspath(metadata_path)
 

class ListIngestedDocuments:

    def __init__(self):
        self.ingested_document = []

    def get_ingested_document(self):
        try:
            data = list(load_metadata(metadata_file_path).keys())
            return data
        except Exception as e:
            raise CustomException(e,sys)
    
if __name__ == "__main__":
    list_ingested_documents = ListIngestedDocuments()
    ingested_document = list_ingested_documents.get_ingested_document()
