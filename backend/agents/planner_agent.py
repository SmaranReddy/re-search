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

class PlannerAgent:
    def plan(self, user_input):
        """
        Extracts key concepts and keywords from the user query
        to improve retrieval precision and minimize hallucinations.
        """
        prompt = (
            f"Extract the most relevant keywords and key phrases from the following research query.\n"
            f"Return only concise search terms (comma-separated) that best represent the topic.\n\n"
            f"Query: {user_input}"
        )

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100
        )

        keywords = response.choices[0].message.content.strip()
        print(f"🧩 Extracted Keywords: {keywords}")
        return keywords
