import os

from dotenv import load_dotenv

load_dotenv()

BASE_URL: str = os.getenv("BASE_URL", "https://automationexercise.com")
DEFAULT_TIMEOUT: int = int(os.getenv("DEFAULT_TIMEOUT", "10"))
HEADLESS: bool = os.getenv("HEADLESS", "false").lower() == "true"
