from langchain_openai import ChatOpenAI


def get_llm():

    llm = ChatOpenAI(
        temperature=0
    )

    return llm
