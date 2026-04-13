def run_rag(query, query_engine, llm):

    # LlamaIndex retrieval
    response = query_engine.query(query)

    context = str(response)

    prompt = f"""
You are a helpful AI assistant.

Use the following context to answer the question.

Context:
{context}

Question:
{query}

Answer:
"""

    final_response = llm.invoke(prompt)

    return final_response.content
