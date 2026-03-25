import streamlit as st
import time

from ingestion.github_loader import load_github_repo
from config import GITHUB_TOKEN
from ingestion.splitter import split_documents
from embeddings.embedding_model import get_embedding_model
from vectorstore.faiss_store import create_vectorstore, load_vectorstore
from retrieval.retriever import get_retriever
from chains.rag_chain import run_rag, get_llm

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(page_title="RepoMind AI", layout="wide")

# -------------------------------
# Custom CSS
# -------------------------------
st.markdown("""
<style>
    .stChatMessage {
        border-radius: 12px;
        padding: 10px;
        margin-bottom: 10px;
    }
    .stChatMessage[data-testid="stChatMessage-user"] {
        background-color: #1e293b;
    }
    .stChatMessage[data-testid="stChatMessage-assistant"] {
        background-color: #0f172a;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------
# Premium Header
# -------------------------------
st.markdown("""
<h1 style='text-align: center; 
background: linear-gradient(to right, #00c6ff, #0072ff);
-webkit-background-clip: text;
color: transparent;'>
🚀 RepoMind AI
</h1>
<p style='text-align: center;'>🧠 Understand Any GitHub Repository Instantly</p>
""", unsafe_allow_html=True)

# -------------------------------
# Session State
# -------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "repo_processed" not in st.session_state:
    st.session_state.repo_processed = False

if "chunks" not in st.session_state:
    st.session_state.chunks = 0

# -------------------------------
# Sidebar
# -------------------------------
with st.sidebar:
    st.markdown("## ⚙️ Controls")

    repo_url = st.text_input("🔗 GitHub Repo URL")

    # Show repo name
    if "repo_name" in st.session_state:
        st.markdown(f"### 📂 {st.session_state.repo_name}")

    # Status (KEEP THIS — working fine)
    if st.session_state.repo_processed:
        st.success("✅ Repository Ready")
        st.info(f"📦 Chunks: {st.session_state.chunks}")

    # Process Repo
    if st.button("📦 Process Repository"):
        if not repo_url:
            st.warning("Please enter a repository URL")
        else:
            with st.spinner("Fetching & processing repo..."):
                try:
                    docs = load_github_repo(repo_url, GITHUB_TOKEN)

                    if not docs:
                        st.error("No valid files found")
                    else:
                        split_docs = split_documents(docs)

                        embedding_model = get_embedding_model()
                        create_vectorstore(split_docs, embedding_model)

                        # Save repo info
                        st.session_state.repo_processed = True
                        st.session_state.chunks = len(split_docs)
                        st.session_state.repo_name = repo_url.split("/")[-1]

                        st.success("Repository processed successfully!")

                except Exception as e:
                    st.error(str(e))

    # Reset Repo
    if st.button("🔄 Reset Repository"):
        st.session_state.repo_processed = False
        st.session_state.messages = []
        st.session_state.chunks = 0
        if "repo_name" in st.session_state:
            del st.session_state.repo_name
        st.success("Reset complete")

    # Clear Chat
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.success("Chat cleared")

# -------------------------------
# Welcome Message
# -------------------------------
if not st.session_state.messages:
    st.markdown("### 👋 Ask me anything about your repository!")

# -------------------------------
# Example Questions
# -------------------------------
st.markdown("### 💡 Try asking:")

col1, col2 = st.columns(2)

quick_q1 = "What does this repository do?"
quick_q2 = "Explain the architecture of this project"

if col1.button("📌 What does this repo do?"):
    user_input = quick_q1
else:
    user_input = None

if col2.button("🏗 Explain architecture"):
    user_input = quick_q2

# -------------------------------
# Chat Display
# -------------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -------------------------------
# Chat Input
# -------------------------------
typed_input = st.chat_input("Ask something about the repository...")

# Prioritize typed input over button input
if typed_input:
    user_input = typed_input

# -------------------------------
# Handle Query
# -------------------------------
if user_input:

    if not st.session_state.repo_processed:
        st.warning("⚠️ Please process a repository first!")
    else:
        # Save user message
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })

        with st.chat_message("user"):
            st.markdown(user_input)

        # Assistant Response
        with st.chat_message("assistant"):
            with st.spinner("🤖 Thinking... analyzing code..."):
                try:
                    embedding_model = get_embedding_model()
                    db = load_vectorstore(embedding_model)

                    retriever = get_retriever(db)
                    llm = get_llm()

                    # ⏱ Measure response time
                    start = time.time()
                    answer = run_rag(user_input, retriever, llm)
                    end = time.time()

                    # Answer
                    st.markdown(f"💡 **Answer:**\n\n{answer}")

                    st.caption(f"⏱ Response time: {round(end - start, 2)}s")

                    # 🔍 Sources & Context (ENHANCED)
                    with st.expander("📎 Sources & Retrieved Context"):
                        docs = retriever.invoke(user_input)

                        for i, doc in enumerate(docs):
                            st.markdown(f"**📄 Source {i+1}**")
                            st.code(doc.page_content[:300], language="python")
                            st.divider()

                    # Save response
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer
                    })

                except Exception as e:
                    st.error(str(e))
