from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

# Load from environment if running on Render, Railway, etc.
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
CORS(app)  # Allow access from any frontend

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data.get('question', '').strip()

    if not question:
        return jsonify({'answer': "Please ask a valid question."}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a fitness and health assistant. Only answer questions related to fitness, exercise, health, or nutrition. If the user asks about anything else, politely refuse."},
                {"role": "user", "content": question}
            ],
            temperature=0.7,
            max_tokens=200
        )
        answer = response['choices'][0]['message']['content'].strip()
        return jsonify({'answer': answer})
    except Exception as e:
        print("ERROR:", e)
        return jsonify({'answer': "Sorry, I am unable to respond right now."}), 500

# Required by Render / Railway to bind to all interfaces
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Render sets PORT env var
    app.run(debug=False, host='0.0.0.0', port=port)
