import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv
from pathlib import Path

st.set_page_config(page_title="LangchainOne Sandbox", page_icon="⌛")



HOME = Path.cwd()
# Load environment variables
load_dotenv(".env")

# Set up Langsmith API environment variables
os.environ["LANGCHAIN_TRACKING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGSMITH_API")

# Define Streamlit UI
st.title("LangchainOne - AI assistant")
st.write("Welcome to LangchainOne")

# Input for user question
input_text = st.text_input("Ask me anything:")

# Sidebar option to select LLM
llm_selection = st.sidebar.selectbox(
    "Select LLM Framework:", ["CTransformer", "Ollama"])
MODEL_NAME = st.sidebar.selectbox(
    'Select LLM Model',
    ('mistral', 'gemma', 'llama','mistral 0.2')
)

TEMPERATURE = st.sidebar.slider(
    'Model Creativity (Temperature):', min_value=0.0, max_value=1.0, step=0.1, value=0.7)

# Define the prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Your name is LangchainOne, created by Abhimanyu Singh (A research fellow and robotics engineer). Please response to user queries"),
    ("user", "Question: {question}")
])

# Initialize LLM based on selection
if llm_selection == "Ollama":
    from langchain_community.llms import Ollama
    llm = Ollama(model=MODEL_NAME)
elif llm_selection == "CTransformer":
    from langchain_community.llms import CTransformers
    if MODEL_NAME == 'mistral':
        llm = CTransformers(
            model=Path(HOME).joinpath("models/mistral-7b-openorca.Q4_0.gguf").as_posix(),
            model_type=MODEL_NAME,
            temperature = TEMPERATURE,
            gpu_layers=50
            )
    elif MODEL_NAME == 'mistral 0.2':
        llm = CTransformers(
            # model="E:\projects\langchain-one\models\mistral-7b-instruct-v0.2.Q4_K_M.gguf",
            model=Path(HOME).joinpath(
                "models/mistral-7b-instruct-v0.2.Q4_K_M.gguf").as_posix(),
            model_type=MODEL_NAME,
            temperature=TEMPERATURE,
            gpu_layers=50
        )
    else:
        pass
output_parser = StrOutputParser()
chain = prompt | llm | output_parser

# Generate and display response
if input_text:
    output = chain.invoke({"question": input_text})
    st.markdown(output)

# # Chat input and output
# user_input = st.text_input("Say something:")

# if st.button("Send"):
#     if user_input:
#         st.write("You: " + user_input)
#         output = chain.invoke({"question": user_input})
#         st.write("Assistant: " + output)
