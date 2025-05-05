# config.py
from dotenv import load_dotenv
import os

# Load .env
load_dotenv()

class Config:
    # Database (to be added later)
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///data.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Tokens & endpoints
    OPENAI_API_KEY         = os.getenv("OPENAI_API_KEY", "")
    HUGGINGFACE_API_TOKEN  = os.getenv("HUGGINGFACE_API_TOKEN", "")
    HF_API_URL             = os.getenv(
        "HF_API_URL",
        "https://api-inference.huggingface.co/models/google/flan-t5-small"
    )

    # Processing limits
    MAX_ROWS_ERROR   = int(os.getenv("MAX_ROWS_ERROR", 5000))
    MAX_ROWS_SAMPLE  = int(os.getenv("MAX_ROWS_SAMPLE", 500))
    MAX_CAT_UNIQUE   = int(os.getenv("MAX_CAT_UNIQUE", 100))
