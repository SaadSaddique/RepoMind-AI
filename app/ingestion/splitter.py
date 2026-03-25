def split_documents(documents, chunk_size=500, overlap=50):
    chunks = []

    for doc in documents:
        start = 0
        length = len(doc)

        while start < length:
            end = start + chunk_size
            chunk = doc[start:end]
            chunks.append(chunk)

            start += chunk_size - overlap

    return chunks
