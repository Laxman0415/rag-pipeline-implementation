import streamlit as st
import requests
import os

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
API_BASE_URL = f"{BACKEND_URL}/rag"

st.set_page_config(page_title="RAG Q&A App", layout="centered")
st.title("📚 RAG Q&A Interface")

# Sidebar with buttons
st.sidebar.title("📌 Menu")
selected_page = st.sidebar.empty()

# State flags
if "page" not in st.session_state:
    st.session_state.page = "ingest"

# Navigation logic using buttons
if st.sidebar.button("📥 Data Ingestion"):
    st.session_state.page = "ingest"

if st.sidebar.button("❓ Ask a Question"):
    st.session_state.page = "query"

# -------------------------------
# 1. Data Ingestion Page
# -------------------------------
if st.session_state.page == "ingest":
    st.header("📥 Ingest a Document")

    document_url = st.text_input("Enter the Document URL")

    if st.button("Ingest Document"):
        if document_url.strip():
            with st.spinner("Ingesting document..."):
                try:
                    response = requests.post(
                        f"{API_BASE_URL}/ingest",
                        json={"document_web_url": document_url}
                    )
                    if response.status_code == 200:
                        st.success(response.json().get("message", "Document ingested successfully"))
                    else:
                        st.error(response.json().get("message", "Ingestion failed"))
                except Exception as e:
                    st.error(f"Request failed: {str(e)}")
        else:
            st.warning("Please enter a valid URL.")

# -------------------------------
# 2. Ask a Question Page
# -------------------------------
elif st.session_state.page == "query":
    st.header("❓ Ask a Question")

    # Load available documents
    try:
        doc_response = requests.get(f"{API_BASE_URL}/documents")
        documents = doc_response.json().get("message", []) if doc_response.status_code == 200 else []
    except Exception as e:
        st.error(f"Failed to load documents: {str(e)}")
        documents = []

    if documents:
        selected_doc = st.selectbox("Select a Document", documents,index=None)
        user_query = st.text_input("Enter your question")

        if st.button("Submit Query"):
            if user_query.strip() and selected_doc:
                with st.spinner("Querying..."):
                    try:
                        response = requests.post(
                            f"{API_BASE_URL}/query",
                            json={"question": user_query, "selected_document_name": selected_doc}
                        )
                        if response.status_code == 200:
                            st.success("✅ Answer:")
                            st.write(response.json().get("message", "No answer provided"))
                        else:
                            st.error(response.json().get("message", "Query failed"))
                    except Exception as e:
                        st.error(f"Request failed: {str(e)}")
            else:
                st.warning("Please enter a question and select a document.")
    else:
        st.warning("No documents available. Ingest a document first.")