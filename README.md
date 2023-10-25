# 🚀 langchain-one

<a target="_blank" href="https://colab.research.google.com/github/abhimanyus1997/langchain-one">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>

LLM App made using [LangChain Framework](#langchain-framework) for Custom Data

## LLM Models available

* [**Mistral-7b openorca**](https://gpt4all.io/models/gguf/mistral-7b-openorca.Q4_0.gguf) - Best overall fast chat model
* [**gpt4all Falcon-q4_0**](https://gpt4all.io/models/gguf/gpt4all-falcon-q4_0.gguf) - Very fast model with good quality
* [**Mistral-7b instruct**](https://gpt4all.io/models/gguf/mistral-7b-instruct-v0.1.Q4_0.gguf) - Best overall fast instruction following model

## LangChain Framework

LangChain is an open-source framework designed to simplify the creation of applications using large language models (LLMs). It provides a standardized interface, prompt management, and external integrations, making it easier for developers to leverage LLMs for a variety of natural language processing tasks. LangChain follows a general pipeline where a user interacts with the language model, which utilizes its vector database and other components to generate responses.

### Key Features

LangChain offers a wide range of features and capabilities for developers:

* Off-the-shelf chains: LangChain provides pre-built chains for common applications.
* Component library: Customize existing chains and build new ones using a library of modular components.
* Memory module: Enhance an LLM's capability to remember and contextualize interactions.
* External integrations: Easily integrate LangChain with external sources of computation and data.

### Applications

LangChain is a versatile framework that can be used to develop various LLM-powered applications, including:

* Document analysis and summarization.
* Chatbots: Create natural and interactive chatbots for customer assistance and more.
* Code analysis: Analyze code for potential bugs and security vulnerabilities.
* Question answering using sources: Answer questions by searching through diverse sources like text, code, and data.
* Data augmentation: Generate new data similar to existing data for training machine learning models.
* Text classification: Perform text classifications and sentiment analysis.
* Text summarization: Summarize text to a specified length.
* Machine translation: Translate text into different languages.

### Key Concepts

LangChain is built around the following key concepts:

* **Components**: These are modular building blocks, including LLM Wrappers, Prompt Templates, and Indexes, designed for easy application development.
* **Chains**: Chains combine components to solve specific tasks, offering a modular approach to building complex applications.
* **Agents**: Agents enable LLMs to interact with their environment, including external APIs for performing specific actions.

LangChain is a powerful and adaptable framework that is continually evolving and supported by a dedicated community of users and contributors.

## How to Run

To get Langchain-one up and running, follow these steps:

1. Clone the repository to your local machine.
 
    ```
    git clone https://github.com/abhimanyus1997/langchain-one.git
    cd langchain-one
    ```

    
2. Create a virtual environment using conda or your preferred virtual environment tool and Install the required packages from the `requirements.txt` file:

    ```
    conda create --name langchain-one-env
    conda activate langchain-one-env
    pip install -r requirements.txt
    ```
    
3. Run the following command to start Langchain-one:

    ```
    chainlit run /src/app.py -w
    ```

This will launch the Langchain-one application in your local environment. You can then access it through your web browser. Enjoy exploring the power of LLMs without privacy concerns!

Author: Abhimanyu Singh
Email: [abhimanyus1997@gmail.com](mailto:abhimanyus1997@gmail.com)
LinkedIn: [Let's Connect](https://www.linkedin.com/in/abhimanyus1997)
