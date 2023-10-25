from pathlib import Path
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms import GPT4All
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
import chainlit as cl


MODEL_NAME = "mistral-7b-openorca.Q4_0.gguf"
MODEL_DIR = r"./models"
MODEL_PATH = "./models/mistral-7b-openorca.Q4_0.gguf"

callbacks = [StreamingStdOutCallbackHandler()]

template = """Question: {question}

Answer: Let's think step by step."""

@cl.on_chat_start
def main():
    # Instantiate the chain for that user session
    prompt = PromptTemplate(template=template, input_variables=["question"])
    LLM = GPT4All(model=MODEL_PATH, verbose=True)
    llm_chain = LLMChain(prompt=prompt, llm=LLM, verbose=True)

    # Store the chain in the user session
    cl.user_session.set("llm_chain", llm_chain)


@cl.on_message
async def main(message: cl.Message):
    # Retrieve the chain from the user session
    llm_chain = cl.user_session.get("llm_chain")  # type: LLMChain

    # Call the chain asynchronously
    res = await llm_chain.acall(message.content, callbacks=[cl.AsyncLangchainCallbackHandler()])

    # Do any post processing here

    # "res" is a Dict. For this chain, we get the response by reading the "text" key.
    # This varies from chain to chain, you should check which key to read.
    await cl.Message(content=res["text"]).send()
