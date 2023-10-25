import os
import requests
import logging
from tqdm import tqdm
from pathlib import Path

# Configuration Constants
MODEL_URL = "https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML/resolve/main/llama-2-7b-chat.ggmlv3.q4_0.bin"
MODEL_PATH = "..\models\llama-2-7b-chat.ggmlv3.q4_0.bin"

# Set up logging
log_directory = os.path.join(os.path.dirname(os.path.dirname(__file__)), "log")
log_file = os.path.join(log_directory, "test_module.log")

# Ensure the log directory exists, and configure logging
os.makedirs(log_directory, exist_ok=True)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Create a logger for this module
logger = logging.getLogger(__name__)

# Create a StreamHandler to log to the console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
logger.addHandler(console_handler)

# Create a FileHandler to save log messages to a file
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.INFO)
logger.addHandler(file_handler)

def download_model():
    """
    Download the model file if it doesn't exist locally.
    """
    if not os.path.exists(MODEL_PATH):
        try:
            logger.info(f"Downloading model from {MODEL_URL}...")
            response = requests.get(MODEL_URL, stream=True)  # Use streaming to download in chunks
            total_size = int(response.headers.get('content-length', 0))
            block_size = 1024  # 1 KB

            # Create a progress bar using tqdm
            with open(MODEL_PATH, 'wb') as file, tqdm(
                total=total_size, unit='B', unit_scale=True, unit_divisor=1024
            ) as pbar:
                for data in response.iter_content(block_size):
                    file.write(data)
                    pbar.update(len(data))

            logger.info(f"Downloaded model to {MODEL_PATH}")
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            raise

def initialize_llm():
    """
    Initialize the GPT4All model.
    """
    download_model()

    from langchain.llms import GPT4All
    llm = GPT4All(
        model=MODEL_PATH,
        max_tokens=2048
    )
    return llm

if __name__ == "__main__":
    try:
        llm = initialize_llm()
        # Proceed with your code using 'llm'
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")

# Additional code and testing goes here
