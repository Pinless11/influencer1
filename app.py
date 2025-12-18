
import os
from flask import Flask, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv

# 1. Configuration & Setup
load_dotenv()  # Load environment variables from a .env file
app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Store conversation history (Simple in-memory storage)
messages = [
    {"role": "system", "content": "You are a helpful and efficient Python-based assistant."}
]

# 2. Core Assistant Logic
def get_assistant_response(user_input):
    """Sends user input to OpenAI and returns the model's response."""
    global messages
    messages.append({"role": "user", "content": user_input})
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",  # Use latest 2025 standard models
            messages=messages
        )
        assistant_reply = response.choices[0].message.content
        messages.append({"role": "assistant", "content": assistant_reply})
        return assistant_reply
    except Exception as e:
        return f"Error connecting to AI: {str(e)}"

# 3. API Endpoints (For Web/App Integration)
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_query = data.get("query")
    if not user_query:
        return jsonify({"error": "No query provided"}), 400
    
    reply = get_assistant_response(user_query)
    return jsonify({"response": reply})

# 4. Terminal Interface (For Local Testing)
if __name__ == "__main__":
    print("--- AI Assistant Local Session (Type 'exit' to quit) ---")
    # Uncomment the line below to run as a web server instead
    # app.run(debug=True, port=5000)
    
    while True:
        user_in = input("You: ")
        if user_in.lower() in ["exit", "quit"]:
            break
        print(f"Assistant: {get_assistant_response(user_in)}")
