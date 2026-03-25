import os

def load_files(repo_path):
    documents = []

    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith((".py", ".md", ".txt", ".js")):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        documents.append(f.read())
                except:
                    continue

    return documents
