# 🧠 RepoMind AI  
### GitHub Repository Assistant with RAG (Retrieval-Augmented Generation)

RepoMind AI is an intelligent system that allows users to upload or connect a GitHub repository and ask natural language questions about the codebase. It retrieves relevant code snippets and documentation and provides contextual explanations using **LangChain**, **FAISS**, and **LLMs**.

It helps developers and teams:
- 🎯 Understand the repository quickly  
- 🧠 Get AI-based code explanations  
- 📄 Navigate documentation efficiently  
- 🚀 Improve code comprehension  

---

## 🚀 Features

✅ GitHub Repository Connection (via API or URL)  
✅ Local Repository Processing  
✅ Code & Documentation Parsing  
✅ Text Chunking and Embeddings (Sentence Transformers)  
✅ FAISS Vector Search  
✅ LLM-Based Contextual Explanations  
✅ Streamlit-Based Interactive UI  
✅ View Source of Retrieved Context  

---

## 🏗️ Project Architecture

User Repository → Load & Parse Code & Docs  
-> Split Text into Chunks  
-> Generate Embeddings  
-> Store in FAISS Vector Database  
-> User Query → Retrieve Relevant Chunks → LLM Explanation  
-> Output Contextual Answer + Source References  

---

## 🛠️ Tech Stack

- **Python**  
- **Streamlit**  
- **LangChain**  
- **Sentence Transformers**  
- **FAISS**  
- **GitHub API**  
- **NumPy**  
- **dotenv**  

---

## 📂 Project Structure
```

RepoMind-AI/
│
├── app/ # Main application logic
│ ├── main.py # Streamlit UI entry point
│ ├── config.py # Configs (API keys, paths)
│ │
│ ├── ingestion/ # Data ingestion pipeline
│ │ ├── github_loader.py # Load repo using GitHub API
│ │ ├── file_loader.py # Load local repo files
│ │ └── splitter.py # Text chunking logic
│ │
│ ├── embeddings/
│ │ └── embedding_model.py # Sentence transformer setup
│ │
│ ├── vectorstore/
│ │ └── faiss_store.py # FAISS DB creation & loading
│ │
│ ├── retrieval/
│ │ └── retriever.py # Retrieval logic
│ │
│ ├── chains/
│ │ └── rag_chain.py # LangChain RAG pipeline
│ │
│ ├── utils/
│ │ ├── helpers.py
│ │ └── logger.py
│
├── data/ # Temporary repo storage
├── experiments/ # Testing different configs/models
│ └── test_rag.ipynb
├── .env # API keys
├── requirements.txt
├── README.md

```
---

## 🎯 How It Works

1️⃣ **User uploads or links a GitHub repository**  

2️⃣ **System Processing:**  
- Loads repository files & documentation  
- Splits large files into chunks  
- Generates sentence embeddings  
- Stores embeddings in FAISS  

3️⃣ **User Queries Repository:**  
- Retrieves relevant code & documentation chunks  
- LLM generates contextual explanation  
- Shows source of retrieved content  

4️⃣ **System Displays:**  
- 🎯 Contextual answer to your query  
- 📌 Code snippets & references where content was retrieved  

---

## 📊 Example Usage

- **Ask:** “What functions handle user authentication?”  
- **Output:**  
  - 🎯 Answer with explanation  
  - 📄 Retrieved code snippets from relevant files  
  - 🔗 Source reference (file name / line numbers)  

---

## 💡 Future Improvements

- Multi-Repository Support  
- Collaborative Code Exploration  
- Advanced Syntax Highlighting in UI  
- Deployment to Cloud (AWS / GCP / Azure)  
- User Preferences & Saved Queries  

---

### 🧑‍💻 Author
**Saad Saddique**  
AI Engineer | Machine Learning | Generative AI

### 📜 License
This project is developed for educational and portfolio purposes.
