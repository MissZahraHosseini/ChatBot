import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ANTHROPIC_API_KEY_AVL")

BASE_URL = "https://api.avalai.ir"
EMBEDDING_BASE_URL = "https://api.avalai.ir/v1"

MODEL = "claude-sonnet-4-5"
MAX_TOKENS = 10000
TEMPERATURE = 0.7