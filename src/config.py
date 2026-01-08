from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

# API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
HF_API_KEY = os.getenv("HF_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is not set")
if not HF_API_KEY:
    raise ValueError("HF_API_KEY is not set")

# Models
GROQ_MODEL = "llama-3.1-8b-instant"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data"
VECTOR_INDEX_PATH = BASE_DIR / "vector_index"
EMBEDDING_CACHE_PATH = BASE_DIR / "embedding_model"
LOGS_PATH = BASE_DIR / "logs"