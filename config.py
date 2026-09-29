import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./fitbuddy.db")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "").strip()

# Keep these configurable because Gemini model names available to an API key can change.
WORKOUT_MODEL = os.getenv("GEMINI_WORKOUT_MODEL", "gemini-2.5-flash")
TIP_MODEL = os.getenv("GEMINI_TIP_MODEL", "gemini-2.5-flash")

ADMIN_KEY = os.getenv("ADMIN_KEY", "").strip()
