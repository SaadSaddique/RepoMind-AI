# RepoMind AI - GitHub Repository Assistant

**RepoMind AI** is a Retrieval-Augmented Generation (RAG) system built with LangChain that allows you to upload or connect any GitHub repository and ask natural language questions about the codebase. The system retrieves relevant code snippets and documentation, then provides contextual explanations.

---

## 🚀 Features

- Process GitHub repositories directly from URL
- Breaks repo files into smaller chunks and stores embeddings in FAISS
- Ask questions about the codebase using natural language
- Chatbot-style interactive UI
- View retrieved context and sources for every answer
- Streamlit front-end with cool, modern UI

---

## 🛠 Tech Stack

- **Framework:** LangChain  
- **Vector Database:** FAISS  
- **Embedding Model:** Sentence Transformers  
- **LLM:** OpenAI or HuggingFace  
- **Backend:** Python  
- **Frontend:** Streamlit  

---

## ⚡ Quick Start

1. **Clone the repository**

```bash
git clone https://github.com/<your-username>/RepoMind-AI.git
cd RepoMind-AI
