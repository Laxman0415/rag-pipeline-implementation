import logging
import os

# Configure logging
logging.basicConfig(
    format="[ %(asctime)s ] %(name)s : %(funcName)s : %(lineno)d - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Create a logger instance
logger = logging.getLogger(__name__)