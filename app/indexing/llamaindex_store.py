from llama_index.core import VectorStoreIndex, Document as LlamaDocument
from llama_index.core.settings import Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding


def create_index(documents):

    # Convert LangChain Documents → LlamaIndex Documents
    llama_docs = []

    for doc in documents:
        llama_docs.append(
            LlamaDocument(
                text=doc.page_content,
                metadata=doc.metadata
            )
        )

    # Embedding model
    embed_model = HuggingFaceEmbedding(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    Settings.embed_model = embed_model

    # Create index
    index = VectorStoreIndex.from_documents(llama_docs)

    return index


def get_query_engine(index):

    query_engine = index.as_query_engine(
        similarity_top_k=3
    )

    return query_engine
