Here's the revised version of the README with further improvements:

---

# 🚀 Langchain-One (Work in Progress)

Langchain-One is an advanced application leveraging the LangChain Framework to harness the capabilities of large language models (LLMs) for various natural language processing tasks. It provides a standardized interface, prompt management, and external integrations to simplify the development of LLM-powered applications.

## Run LangOneGPT

To run LangOneGPT, follow these steps:

1. Activate the virtual environment using the provided script:

    ```powershell
    .venv/Scripts/activate.ps1
    ```

2. Run the LangOneGPT script:

    ```powershell
    streamlit run tests\streamlit\LangchainOne_Home.py
    ```

## Tech Stack

LangchainOne makes use of the following technologies:

- **Langchain Ecosystem (Langchain and Langsmith)**: Provides the foundation for language processing and understanding.
- **cTransformers**: A powerful framework for deploying and utilizing large language models.
- **Ollama**: Another advanced language model framework contributing to LangchainOne's capabilities.
- **Hugging Face**: A key provider of pre-trained models and libraries for natural language processing tasks.
- **Streamlit**: Powers the user-friendly interface for interacting with LangchainOne.

## LLM Models (Recommended)

### Integrated LLMs

* [**Mistral-7b openorca**](https://gpt4all.io/models/gguf/mistral-7b-openorca.Q4_0.gguf): A high-quality, fast chat model suitable for various applications.

### Other Recommended LLM Integrations

* [**gpt4all Falcon-q4_0**](https://gpt4all.io/models/gguf/gpt4all-falcon-q4_0.gguf): A very fast model with good quality, suitable for rapid responses.
* [**Mistral-7b instruct**](https://gpt4all.io/models/gguf/mistral-7b-instruct-v0.1.Q4_0.gguf): A fast instruction-following model ideal for instructional text tasks.

## How to Run Langchain-One

To run Langchain-One on your local machine, follow these steps:

1. **Download Model**: Download the LLM model and place it in the `model` directory.

2. **Clone Repository**: Clone the Langchain-One repository to your local machine.

    ```sh
    git clone https://github.com/abhimanyus1997/langchain-one.git
    cd langchain-one
    ```

3. **Create Virtual Environment**: Create a virtual environment and install required packages from `requirements.txt`.

    ```sh
    conda create --name langchain-one-env
    conda activate langchain-one-env
    pip install -r requirements.txt
    ```

4. **Run Langchain-One**: Run the following command to start Langchain-One.

    ```sh
    chainlit run /src/app.py -w
    ```

    This will launch the Langchain-One application in your local environment.

## Author Information

**Author:** Abhimanyu Singh  
**Email:** [abhimanyus1997@gmail.com](mailto:abhimanyus1997@gmail.com)  
**LinkedIn:** [Connect on LinkedIn](https://www.linkedin.com/in/abhimanyus1997)  
