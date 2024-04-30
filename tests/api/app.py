from fastapi import FastAPI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langserve import add_routes

from langchain.llms import CTransformers
from langchain_community.llms import Ollama

import os
import uvicorn
from dotenv import load_dotenv
from pathlib import Path

# MODEL FILE
MODEL_FILE = Path("models\mistral-7b-instruct-v0.2.Q4_K_M.gguf")

llm = CTransformers(
    model=Path(MODEL_FILE).as_posix(),
    model_type="mistral",
    streaming=True,
    verbose=True,
)

config = {
    # reducing the probability of generating the same token again
    "max_new_tokens": 2048,
    "context_length" : 8192,
    "stream": True,  # continuous streaming of data
    "threads": int(os.cpu_count() / 2)  # parallel processing
}

# more context length for summary
summary_llm = CTransformers(
    model=Path(MODEL_FILE).as_posix(),
    model_type="mistral",
    ** config,
    verbose=True,
)
# summary_llm = Ollama(model="gemma:7b-instruct-q4_K_S")

# Load environment variables from .env file
load_dotenv(".env")

# Initialize FastAPI application
app = FastAPI(
    title="LangchainOne Server",
    version="0.0.1",
    description="A basic LangchainOne API Server"
)



# Define prompt templates
summary_prompt = ChatPromptTemplate.from_template(
    "Compose a concise summary by condensing the provided content without omitting crucial details and refraining from including any non-factual information.\nContent:{content}")

paraphrase_prompt = ChatPromptTemplate.from_template(
    "Rephrase the provided text while maintaining its original meaning and context, using different vocabulary and expressions. Ensure that all essential information is retained within a similar word limit.\nContent:{content}")

# Add routes for summarization and paraphrasing
add_routes(
    app,
    summary_prompt | summary_llm,
    path="/summary"
)

add_routes(
    app,
    paraphrase_prompt | llm,
    path="/paraphrase"
)

if __name__ == "__main__":
    # Run the FastAPI server
    uvicorn.run(app, host="0.0.0.0", port=8000)
