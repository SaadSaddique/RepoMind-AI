import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
HF_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # <--- ADD THIS LINE

DATA_PATH = "data/"
FAISS_PATH = "faiss_index/"
