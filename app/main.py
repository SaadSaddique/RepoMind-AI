import streamlit as st
import time

from ingestion.github_loader import load_github_repo
from config import GITHUB_TOKEN

from ingestion.langchain_splitter import split_documents
from indexing.llamaindex_store import create_index, get_query_engine
from llm.llm_model import get_llm
from chains.rag_chain import run_rag


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

if "index" not in st.session_state:
    st.session_state.index = None


# -------------------------------
# Sidebar
# -------------------------------
with st.sidebar:

    st.markdown("## ⚙️ Controls")

    repo_url = st.text_input("🔗 GitHub Repo URL")

    if "repo_name" in st.session_state:
        st.markdown(f"### 📂 {st.session_state.repo_name}")

    if st.session_state.repo_processed:
        st.success("✅ Repository Ready")
        st.info(f"📦 Chunks: {st.session_state.chunks}")

    # -------------------------------
    # Process Repository
    # -------------------------------

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

                        index = create_index(split_docs)

                        st.session_state.index = index
                        st.session_state.repo_processed = True
                        st.session_state.chunks = len(split_docs)
                        st.session_state.repo_name = repo_url.split("/")[-1]

                        st.success("Repository processed successfully!")

                except Exception as e:
                    st.error(str(e))


    # -------------------------------
    # Reset Repository
    # -------------------------------

    if st.button("🔄 Reset Repository"):

        st.session_state.repo_processed = False
        st.session_state.messages = []
        st.session_state.chunks = 0
        st.session_state.index = None

        if "repo_name" in st.session_state:
            del st.session_state.repo_name

        st.success("Reset complete")


    # -------------------------------
    # Clear Chat
    # -------------------------------

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

if typed_input:
    user_input = typed_input


# -------------------------------
# Handle Query
# -------------------------------

if user_input:

    if not st.session_state.repo_processed:

        st.warning("⚠️ Please process a repository first!")

    else:

        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })

        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):

            with st.spinner("🤖 Thinking... analyzing code..."):

                try:

                    query_engine = get_query_engine(st.session_state.index)

                    llm = get_llm()

                    start = time.time()

                    answer = run_rag(user_input, query_engine, llm)

                    end = time.time()

                    st.markdown(f"💡 **Answer:**\n\n{answer}")

                    st.caption(f"⏱ Response time: {round(end - start, 2)}s")


                    # -------------------------------
                    # Retrieved Sources
                    # -------------------------------

                    with st.expander("📎 Retrieved Context"):

                        response = query_engine.query(user_input)

                        st.markdown(str(response))


                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer
                    })

                except Exception as e:
                    st.error(str(e))
