from langchain_openai import ChatOpenAI

def get_llm():
    return ChatOpenAI(temperature=0)

def run_rag(query, retriever, llm):
    # NEW API
    docs = retriever.invoke(query)

    context = "\n\n".join([doc.page_content for doc in docs])

    prompt = f"""
You are a helpful AI assistant.

Use the following context to answer the question.

Context:
{context}

Question:
{query}

Answer:
"""

    response = llm.invoke(prompt)

    return response.content
