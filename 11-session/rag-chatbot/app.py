import os

import streamlit as st
from dotenv import load_dotenv
from google.genai.errors import APIError
from llama_index.core import Settings, SimpleDirectoryReader, VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.google_genai import GoogleGenAI

load_dotenv()
DATA_DIR = "data"


def get_api_key():
    """Check that the Gemini API key was loaded; stop with help if not."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        st.error(
            "GEMINI_API_KEY is missing. Create a .env file next to app.py "
            "containing GEMINI_API_KEY=your-key, then restart the app."
        )
        st.stop()
    return api_key


def validate_data_dir():
    """Check that DATA_DIR exists and holds at least one real document."""
    if not os.path.isdir(DATA_DIR):
        st.error(
            f"Data folder '{DATA_DIR}/' not found. Create it next to app.py "
            "and put the student handbook PDF inside."
        )
        st.stop()
    # Ignore hidden files like .DS_Store: they are not documents
    files = [f for f in os.listdir(DATA_DIR) if not f.startswith(".")]
    if not files:
        st.error(
            f"Data folder '{DATA_DIR}/' is empty. Add at least one document "
            "(e.g., the student handbook PDF), then restart the app."
        )
        st.stop()


@st.cache_resource(show_spinner="Indexing the handbook (first run only)...")
def get_query_engine(api_key):
    """Build the index once per session and return a query engine."""
    Settings.llm = GoogleGenAI(model="gemini-3.8-flash", api_key=api_key)
    Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
    documents = SimpleDirectoryReader(DATA_DIR).load_data()
    index = VectorStoreIndex.from_documents(documents)
    return index.as_query_engine()


st.title("Babson Student Handbook Chatbot")

# Fail fast: validate configuration before doing any work
api_key = get_api_key()
validate_data_dir()

# Fail fast: the app is useless if the engine cannot be built
try:
    query_engine = get_query_engine(api_key)
except Exception as e:
    st.error(
        f"Could not build the document index: {e}. Check the files in "
        f"'{DATA_DIR}/' and your internet connection, then restart the app."
    )
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if question := st.chat_input("Ask about the student handbook"):
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)
    with st.chat_message("assistant"):
        answer = None
        with st.spinner("Searching..."):
            # Fallback: one failed question should not kill the app
            try:
                answer = query_engine.query(question).response
            except APIError as e:
                st.error(
                    f"The model request failed ({e.code}). This is usually a "
                    "rate limit or an invalid key — wait a moment and ask again."
                )
            except Exception as e:
                st.error(
                    f"Something went wrong answering that question: {e}. "
                    "Check your internet connection and try again."
                )
        if answer is not None:
            st.write(answer)
            st.session_state.messages.append(
                {"role": "assistant", "content": answer}
            )
