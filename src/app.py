import os
# import torch
import numpy as np
import io  # Import io module for handling byte streams

import easyocr
from PIL import Image

# import tensorflow

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


# ... (imports and configuration)

@cl.on_chat_start
def main():
    # Instantiate the chain for that user session
    prompt_template = """
    Question: {question}

    Extracted Text from image uploaded by User:
    {extracted_text}

    Answer: Please refer to factual information and use image provided and don't make up fictional data/information.
    """

    # Store the prompt template in the user session
    cl.user_session.set("prompt_template", prompt_template)

    # Using LLM Model
    llm_chain = LLMChain(prompt=PromptTemplate(
        template=prompt_template, input_variables=["question"]), llm=llm_init, verbose=True)
    # Store the chain in the user session
    cl.user_session.set("llm_chain", llm_chain)


@cl.on_message
async def main(msg: cl.Message):
    # IMAGE INPUT PROCESSING USING EasyOCR

    if not msg.elements:
        await cl.Message(content="No file attached").send()
        pass

    # Processing images exclusively
    images = [file for file in msg.elements if "image" in file.mime]

    # Accessing the bytes of a specific image
    image_bytes = images[0].content

    # Perform OCR on the image using easyocr
    reader = easyocr.Reader(['en', 'hi'])
    img = Image.open(io.BytesIO(image_bytes))
    extracted_data = reader.readtext(np.array(img))

    # Extracting only the text from the extracted data
    extracted_text = [data[1] for data in extracted_data]
    formatted_extracted_text = "\n".join(extracted_text)

    # Retrieve the chain from the user session
    llm_chain = cl.user_session.get("llm_chain")  # type: LLMChain

    # Retrieve the prompt template from the user session
    prompt_template = cl.user_session.get("prompt_template")

    # Generate the prompt with extracted text
    prompt_with_extracted_text = prompt_template.format(
        question=msg.content,
        extracted_text=formatted_extracted_text
    )

    # Call the chain asynchronously
    res = await llm_chain.acall(prompt_with_extracted_text, callbacks=[cl.AsyncLangchainCallbackHandler()])

    # Do any post processing here
    await cl.Message(content=f"Received {len(images)} image(s)\nDATA:\t {extracted_text}").send()

    # Send the response generated by the chain
    await cl.Message(content=res["text"]).send()
