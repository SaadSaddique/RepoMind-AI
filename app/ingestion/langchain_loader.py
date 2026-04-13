from langchain_community.document_loaders import DirectoryLoader, TextLoader

def load_local_repo(repo_path):

    loader = DirectoryLoader(
        repo_path,
        glob="**/*",
        loader_cls=TextLoader,
        silent_errors=True
    )

    documents = loader.load()

    return documents
