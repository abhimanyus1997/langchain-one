import os
import logging
from langchain_community.llms import CTransformers
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
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
log_file = Path(LOG_DIR) / "streamlit_langOneGPT.log"
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
    page_title="LangOne GPT",
    page_icon="🔗",
)


# Define the model path using Pathlib
HOME = Path.cwd()
MODELS_FOLDER = HOME / "models"
DOWNLOADED_MODELS = [model.name for model in MODELS_FOLDER.iterdir(
) if model.is_file() and model.suffix == ".gguf"]
USER_MODEL = st.sidebar.selectbox(
    "Select LLM Model", DOWNLOADED_MODELS, index=0)
MODEL_PATH = MODELS_FOLDER / USER_MODEL



# Model Type options
MODEL_TYPES = {
    "Mistral": "mistral",
    "Falcon": "falcon",
    "LLaMA, LLaMA 2": "llama",
    "GPT-2": "gpt2",
    "GPT-J, GPT4All-J": "gptj",
    "GPT-NeoX, StableLM": "gpt_neox",
    "MPT": "mpt",
    "StarCoder, StarChat": "gpt_bigcode",
    "Dolly V2": "dolly-v2",
    "Replit": "replit",
    "Gemma" : "gemma"
}
selected_model_type = st.sidebar.selectbox(
    "Select Model Type", list(MODEL_TYPES.keys()))
# Check if MODEL_PATH exists, otherwise show Streamlit alert
if not MODEL_PATH.exists():
    st.error(
        "Error: Model file not found. Please make sure the model file exists at the specified path.")
    st.stop()

# Running Gemma on Ollama Framework
if MODEL_TYPES[selected_model_type] == "gemma":
    from langchain_community.llms import Ollama
    llm = Ollama(model=MODEL_TYPES[selected_model_type])
else:
    # Initialize Langchain LLM
    max_new_tokens = st.sidebar.number_input(
        "Max New Tokens (Output)", value=256, step=1)
    seed = st.sidebar.number_input(
        "Seed", value=-1, step=1)
    CONTEXT_LENGTH = st.sidebar.number_input(
        "Max Context Length", value=-1, step=1)
    llm = CTransformers(model=MODEL_PATH.as_posix(),
                        model_type=MODEL_TYPES[selected_model_type],
                        context_length=CONTEXT_LENGTH,
                        max_new_tokens=max_new_tokens,
                        seed=seed
                        )


# Define the prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Your name is LangOneGPT, created by Abhimanyu Singh (A research fellow and robotics engineer). Please response to user queries"),
    ("user", "Question: {question}")
])

# Initialize the output parser
output_parser = StrOutputParser()

# Combine prompt, llm, and output_parser into a chain
chain = prompt | llm | output_parser

# Function to generate responses using Langchain LLM


def generate_response(prompt):
    response = chain.invoke({"question": prompt})  # Use the provided prompt
    # Log LLM model information in a separate thread to avoid blocking
    threading.Thread(target=log_model_info, args=(
        USER_MODEL, MODEL_PATH)).start()
    return response

# Function to log LLM model information


def log_model_info(user_model, model_path):
    logger.info(f"LLM Model Used: {user_model}")
    logger.info(f"LLM Model Path: {model_path}")


st.title("LangOne GPT Assistant")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response using Langchain LLM
    try:
        assistant_response = generate_response(prompt)
    except Exception as e:
        st.error(f"Error: {e}")
        st.stop()

    # Retain only the portion of the response after the last occurrence of "Assistant:" or "LangchainOne:",
    # whichever comes last in the string
    assistant_response = assistant_response.rsplit("Assistant:", 1)[-1].rsplit(
        "LangchainOne:", 1)[-1].rsplit("LangOneGPT:", 1)[-1].rsplit("LangOneGTP:", 1)[-1]

    # Parse and display assistant response in chat message container
    with st.chat_message("assistant"):
        parsed_response = output_parser.parse(assistant_response)
        # Remove leading and trailing whitespaces
        st.write(parsed_response.strip())

    # Log assistant response
    logger.info(f"Assistant response: {assistant_response}")

    # Add assistant response to chat history
    st.session_state.messages.append(
        {"role": "assistant", "content": assistant_response})
