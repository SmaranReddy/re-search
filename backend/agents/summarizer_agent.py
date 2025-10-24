from groq import Groq
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the API key from environment variables
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY not found in .env file")

client = Groq(api_key=api_key)

class SummarizerAgent:
    def summarize(self, abstract):
        prompt = (
            f"Summarize this research abstract into four sections:\n"
            f"Problem, Method, Results, and Limitations.\n\nAbstract:\n{abstract}"
        )
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1024  # Prevents runaway generation
        )
        return response.choices[0].message.content

