from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import traceback

# For example, using Cohere
import cohere
from dotenv import load_dotenv

load_dotenv()

# Setup Cohere or any other AI provider
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
if not COHERE_API_KEY:
    raise ValueError("COHERE_API_KEY not set in .env")
co = cohere.Client(COHERE_API_KEY)

app = Flask(__name__)
CORS(app)  # Allow CORS for all domains

@app.route('/')
def home():
    return 'AthliZen AI Server (Cohere) is running.'

@app.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.get_json()
        question = data.get('question', '').strip()
        print("📩 Question from frontend:", question)

        if not question:
            return jsonify({'answer': "Please ask a valid question."}), 400

        # Call to Cohere (example)
        response = co.generate(
            model='command-r',
            prompt=(
                f"You are a helpful assistant that only answers fitness, health, "
                f"exercise, or nutrition-related questions. If the user asks something "
                f"outside of those topics, politely refuse.\n\nUser: {question}\nAI:"
            ),
            max_tokens=200,
            temperature=0.7
        )

        answer = response.generations[0].text.strip()
        print("🤖 AI Response:", answer)
        return jsonify({'answer': answer})

    except Exception as e:
        print("🔥 ERROR:", e)
        traceback.print_exc()
        return jsonify({'answer': f"Error: {str(e)}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
