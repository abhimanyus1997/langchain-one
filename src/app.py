import os
import torch
import keras_ocr # Image processing for OCR
import tensorflow

from transformers import pipeline
from ctransformers import AutoModelForCausalLM


from pathlib import Path
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
# from langchain.llms import GPT4All
from langchain.llms import CTransformers
from langchain.llms.huggingface_pipeline import HuggingFacePipeline

from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
import chainlit as cl
import pypdf




config = {
    "max_new_tokens": 1024,
    "repetition_penalty": 1.1,  # reducing the probability of generating the same token again
    "temperature": 0.5,  # randomness
    "top_k": 50,    # selecting top recommendations
    "top_p": 0.9,   # nucleus sampling
    "stream": True,  # continuous streaming of data
    "threads": int(os.cpu_count() / 2)  # parallel processing
}


llm_init = CTransformers(
    model="TheBloke/OpenHermes-2.5-Mistral-7B-GGUF",
    model_file="openhermes-2.5-mistral-7b.Q4_K_S.gguf",
    model_type="mistral",
    lib="avx2",
    callbacks=[StreamingStdOutCallbackHandler()],
    ** config,
    verbose = True,
    # gpu_layers=50,
    # **config
)

pipeline = keras_ocr.pipeline.Pipeline()

# Zero Shot Inference Template
template = """Question: {question}

Answer: Please refer to factual information and don't make up fictional data/information.
"""


@cl.on_chat_start
def main():
    # Instantiate the chain for that user session
    prompt = PromptTemplate(template=template, input_variables=["question"])
    # Using LLM Model
    llm_chain = LLMChain(prompt=prompt, llm=llm_init, verbose=True)
    # Store the chain in the user session
    cl.user_session.set("llm_chain", llm_chain)


@cl.on_message
async def main(msg: cl.Message):

    # IMAGE INPUT PROCESSING USING KERAS_OCR

    if not msg.elements:
        await cl.Message(content="No file attached").send()
        return

    # Processing images exclusively
    images = [file for file in msg.elements if "image" in file.mime]

    # Accessing the bytes of a specific image
    image_bytes = images[0].content

    # Using Keras OCR to perform text extraction
    image = keras_ocr.tools.read(image_bytes)
    predictions = pipeline.recognize([image])

    # Extract text from predictions
    extracted_text = ''
    for prediction in predictions:
        for word, box in zip(prediction[0], prediction[1]):
            extracted_text += f"{word} "

    # Retrieve the chain from the user session
    llm_chain = cl.user_session.get("llm_chain")  # type: LLMChain

    # Call the chain asynchronously
    res = await llm_chain.acall(msg.content, callbacks=[cl.AsyncLangchainCallbackHandler()])

    # Do any post processing here
    await cl.Message(content=f"Received {len(images)} image(s)\nDATA:\t {extracted_text}").send()

    # "res" is a Dict. For this chain, we get the response by reading the "text" key.
    # This varies from chain to chain, you should check which key to read.
    await cl.Message(content=res["text"]).send()
