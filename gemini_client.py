from google import genai

from .config import GOOGLE_API_KEY


def get_client():
    if not GOOGLE_API_KEY:
        raise RuntimeError(
            "GOOGLE_API_KEY is not configured. Add it to the .env file before generating a plan."
        )
    return genai.Client(api_key=GOOGLE_API_KEY)
