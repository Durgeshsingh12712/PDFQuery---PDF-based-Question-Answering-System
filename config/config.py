import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    VECTOR_DB_PATH = 'vector_db'


    MAX_FILE_SIZE = 20 * 1024 * 1024
    ALLOWED_EXTENSIONS = {'pdf', 'txt'}

    SESSION_LIFETIME = 3600

    index_name = "pdfQuery"