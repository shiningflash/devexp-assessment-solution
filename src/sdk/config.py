import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    BASE_URL = os.getenv("BASE_URL", "http://localhost:3000")
    API_KEY = os.getenv("API_KEY")

    @staticmethod
    def validate():
        if not Config.API_KEY:
            raise ValueError("API_KEY is not set in the environment.")
