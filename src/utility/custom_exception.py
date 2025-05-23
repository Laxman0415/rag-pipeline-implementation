import sys
    
def error_message_details(error, error_details: sys):
    # Retrieve the exception type, exception value, and traceback object
    _, _, exc_tb = error_details.exc_info()
    
    # Get the filename where the exception occurred
    file_name = exc_tb.tb_frame.f_code.co_filename
    
    # Get the line number where the exception occurred
    line_number = exc_tb.tb_lineno
    
    # Convert the error message to a string
    error_message = str(error)
    
    # Format the error message with the filename, line number, and original error message
    formatted_error_message = "Error occurred in Python script [{0}] at line number [{1}]: {2}".format(
        file_name, line_number, error_message)
    
    return formatted_error_message

    
class CustomException(Exception):
    
    def __init__(self,error_message,error_details:sys):
        super().__init__(error_message)
        self.error_message = error_message_details(error_message,error_details)
        
    def __str__(self):
        return self.error_message