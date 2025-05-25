from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from data_retrieval.retriever import DataRetriever
from langchain_core.prompts import ChatPromptTemplate
from utility.custom_exception import CustomException
from utility.custom_logger import logger
from utility.utils import get_groq_chat_model
import os,sys

current_path = os.path.dirname(os.path.abspath(__name__))
prompt_template_path = os.path.join(current_path,"prompt_registry","knowledge_base.txt")
prompt_path = os.path.abspath(prompt_template_path)


with open(prompt_path,"r") as fp:
    PROMPT_TEMPLATES = fp.read()

class InvokeResponseGeneration:

    def __init__(self,query,selected_document_name):
        self.query = query
        self.selected_document_name = selected_document_name

    def invoke_chain(self):
        try:
            retriever = DataRetriever(self.selected_document_name).get_retriver()
            if retriever != None:
                prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATES)
                llm = get_groq_chat_model()
                chain=(
                    {"context": retriever, "question": RunnablePassthrough()}
                    | prompt
                    | llm
                    | StrOutputParser()
                
                )
                
                output=chain.invoke(self.query)
                
                return output
            else:
                return None

        except Exception as e:
            raise CustomException(e,sys)

if __name__ == "__main__":
    query = "What is SYDNEY BUXTON's Amendment ?"
    selected_document_name = "https://www.gutenberg.org/cache/epub/13421/pg13421.txt"
    invoke = InvokeResponseGeneration(query,selected_document_name)
    response = invoke.invoke_chain()