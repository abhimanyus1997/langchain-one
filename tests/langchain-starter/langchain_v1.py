import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama

import os
from dotenv import load_dotenv

print(os.getcwd())
# Load environment variables
load_dotenv(".env")

# Set up Langsmith API environment variables
os.environ["LANGCHAIN_TRACKING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGSMITH_API")

# Define Streamlit UI
st.title("LangchainOne - Streamlit App powered by Ollama")
st.write("Welcome to LangchainOne")

# Input for user question
input_text = st.text_input("Ask me anything:")

# Define the prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Your name is LangchainOne, created by Abhimanyu Singh (A research fellow and robotics engineer). Please response to user queries"),
    ("user", "Question: {question}")
])

# Initialize Ollama LLM
llm = Ollama(model="gemma")
output_parser = StrOutputParser()
chain = prompt | llm | output_parser

# # Generate and display response
if input_text:
    output = chain.invoke({"question": input_text})
    st.markdown(output)


# # Generate and display Streaming response
# output_placeholder = st.empty()  # Placeholder for streaming output
# if input_text:
#     output_chunks = []
#     for chunks in chain.stream({"question": input_text}):
#         output_chunks.append(chunks)
#     output_text = "\n".join(output_chunks)
#     output_placeholder.write(output_text)
