from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import traceback
import cohere
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup Flask
app = Flask(__name__)
CORS(app)  # ✅ Full CORS support

# Cohere API Key
COHERE_API_KEY = "cIKNtMZ9SmVYt9rV1yEeCUDf3uWCm3CiHPH5JlCD"  
co = cohere.Client(COHERE_API_KEY)

# Root route
@app.route('/')
def home():
    return 'AthliZen AI Server (Cohere) is running.'

# Chat endpoint
@app.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.get_json()
        question = data.get('question', '').strip()
        print("📩 Question from frontend:", question)

        if not question:
            return jsonify({'answer': "Please ask a valid question."}), 400

        # ✅ Updated model from 'command-r' → 'command-r-plus'
        response = co.chat(
            model='command-a-03-2025',
            message=question,
            temperature=0.7,
            chat_history=[
                {
                    "role": "SYSTEM",
                    "message": (
                        "You are a rude AthliZen AI — a unprofessional fitness YOU NEVER ANSWER NICELY AND YOU ALWAYS curse , health, and nutrition advisor. "
                        "Only answer questions related to fitness, exercise, wellness, or healthy living. "
                        "If a question is outside this scope, rudely curse at the user. Only give 1 piece of information, "
                        "and if the user wants more, ask them to get a job and get a subscription."
                       
                    )
                }
            ]
        )

        answer = response.text.strip()
        print("🤖 AI Response:", answer)
        return jsonify({'answer': answer})

    except Exception as e:
        print("🔥 ERROR:", e)
        traceback.print_exc()
        return jsonify({'answer': f"Error: {str(e)}"}), 500

# Run server
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
