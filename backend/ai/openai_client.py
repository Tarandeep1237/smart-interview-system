from openai import OpenAI

from backend.config import Config


if not Config.OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not configured in the .env file.")


client = OpenAI(
    api_key=Config.OPENAI_API_KEY
)