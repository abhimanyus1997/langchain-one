import streamlit as st
import requests

# Function to send requests to the FastAPI server
def send_request(server_url, endpoint, data):
    url = f"{server_url}{endpoint}"
    response = requests.post(url, json=data)
    return response.json()

# Streamlit UI for summarization
def summarize(server_url):
    st.title("Text Summarization")
    content = st.text_area("Enter text to summarize")
    if st.button("Summarize"):
        data = {'input':{"content": content}}
        response = send_request(server_url, "/summary/invoke", data)
        st.subheader("Summary")
        st.write(response["output"])

# Streamlit UI for paraphrasing
def paraphrase(server_url):
    st.title("Text Paraphrasing")
    content = st.text_area("Enter text to paraphrase")
    if st.button("Paraphrase"):
        data = {'input':{"content": content}}
        response = send_request(server_url, "/paraphrase/invoke", data)
        st.subheader("Paraphrased Text")
        st.write(response["output"])

# Main function to run the Streamlit app
def main():
    default_server_url = "http://localhost:8000"
    st.sidebar.title("LangchainOne Client")
    server_url = st.sidebar.text_input(
        "Enter FastAPI server URL", value=default_server_url)

    if server_url:
        option = st.sidebar.radio(
            "Select an option", ("Summarize", "Paraphrase"))

        if option == "Summarize":
            summarize(server_url)
        elif option == "Paraphrase":
            paraphrase(server_url)
    else:
        st.sidebar.warning("Please enter the FastAPI server URL.")


if __name__ == "__main__":
    main()
