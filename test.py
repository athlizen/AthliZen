import cohere
import os
from dotenv import load_dotenv

load_dotenv()  # Load from .env

# Or paste the key directly if .env isn't working
COHERE_API_KEY = os.getenv("COHERE_API_KEY") or "9UdObC5ScVqsabnce7bUwYNyZXOTZuOi02sK6PyB"

if not COHERE_API_KEY:
    print("❌ API key not found.")
    exit()

co = cohere.Client(COHERE_API_KEY)

try:
    prompt = "What is the best workout routine to build chest muscles?"
    print("📤 Sending prompt:", prompt)

    response = co.generate(
        model="command-r-plus",  # advanced model, use "command" if you're on free tier
        prompt=prompt,
        max_tokens=150,
        temperature=0.7
    )

    print("✅ AI Response:")
    print(response.generations[0].text.strip())

except Exception as e:
    print("❌ Error talking to Cohere:", e)
