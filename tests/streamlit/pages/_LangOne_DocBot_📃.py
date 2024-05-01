import os
import logging
from io import StringIO
import tempfile

from langchain_community.llms import Ollama
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_community.vectorstores import FAISS
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

from langchain_core.prompts import ChatPromptTemplate

import streamlit as st
from pathlib import Path
import threading

# Create log directory if it doesn't exist
LOG_DIR = "log"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
log_file = Path(LOG_DIR) / "streamlit_langOneDoc.log"
file_handler = logging.FileHandler(log_file)
console_handler = logging.StreamHandler()  # Console handler
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)  # Set formatter for console handler
logger.addHandler(file_handler)
logger.addHandler(console_handler)  # Add console handler to logger

# Page Config
st.set_page_config(
    page_title="LangOne DocBot",
    page_icon="📃",
)

prompt = ChatPromptTemplate.from_template("""Answer the following question based only on the provided context:

    <context>
    {context}
    </context>

    Question: {input}""")

# Define the model path using Pathlib
HOME = Path.cwd()
MODEL_LIST = ['mistral', 'gemma', 'llama3', 'lllama2', 'zephyr']
MODEL = st.sidebar.selectbox("Select Ollama Model", MODEL_LIST)
UPLOADED_FILE = st.sidebar.file_uploader("Upload pdf file",type=".pdf")
if UPLOADED_FILE is not None:
    # Save the uploaded file to a temporary directory
    temp_dir = tempfile.TemporaryDirectory()
    file_path = os.path.join(temp_dir.name, UPLOADED_FILE.name)
    with open(file_path, 'wb') as f:
        f.write(UPLOADED_FILE.getvalue())

    # LLM Model Loading
    llm = Ollama(model=MODEL)

    # Document Loading
    loader_ = PyPDFLoader(file_path)
    docs_ = loader_.load()

    # Data Chunking
    text_splitter_ = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=200)
    documents_ = text_splitter_.split_documents(docs_)

    # Vector Embedding
    embeddings_ = OllamaEmbeddings(model=MODEL)

    # Vector Storage
    # db_ = Chroma.from_documents(documents_, embeddings_)
    db_ = FAISS.from_documents(documents_, embeddings_)
    # Document and Retrival Chain
    document_chain_ = create_stuff_documents_chain(llm, prompt)
    retriever_ = db_.as_retriever()
    retrieval_chain_ = create_retrieval_chain(retriever_, document_chain_)

# Initialize chat history if not already initialized
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
user_input = st.text_input("Ask LangOne DocBot Anything")
if user_input:
    # Add user message to chat history
    st.session_state.messages.append(
        {"role": "user", "content": user_input})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate response using retrieval chain
    try:
        response = retrieval_chain_.invoke({"input": user_input})
    except Exception as e:
        st.error(f"Error: {e}")
        st.stop()

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response["answer"])

    # Log assistant response
    logger.info(f"Assistant response: {response['answer']}")

    # Add assistant response to chat history
    st.session_state.messages.append(
        {"role": "assistant", "content": response["answer"]})
