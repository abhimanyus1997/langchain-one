from langchain_community.llms import CTransformers
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import streamlit as st
from pathlib import Path

# Define the model path using Pathlib
HOME = Path.cwd()
MODEL_PATH = HOME / "models" / "mistral-7b-instruct-v0.2.Q4_K_M.gguf"

st.set_page_config(
    page_title="LangOne GPT",
    page_icon="🔗",
)

# Initialize Langchain LLM
llm = CTransformers(model=MODEL_PATH.as_posix())

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
    return response

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
    assistant_response = generate_response(prompt)

    # Remove everything before "Assistant:" or "LangchainOne:" whichever is there
    assistant_response = assistant_response.split(
        "Assistant:", 1)[-1].split("LangchainOne:", 1)[-1]


    # Parse and display assistant response in chat message container
    with st.chat_message("assistant"):
        parsed_response = output_parser.parse(assistant_response)
        # Remove leading and trailing whitespaces
        st.write(parsed_response.strip())

    # Add assistant response to chat history
    st.session_state.messages.append(
        {"role": "assistant", "content": assistant_response})
