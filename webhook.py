from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Replace with your actual Gemini API Key
GEMINI_API_KEY = "AIzaSyDkKtG-kdTrjxQ7vzTHDdro70uQCBBwFzI"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json()

    # Extract Dialogflow's response and intent
    intent_name = req["queryResult"]["intent"]["displayName"]
    user_query = req["queryResult"]["queryText"]

    # If it's NOT a fallback intent, return Dialogflow's response
    if intent_name != "Default Fallback Intent":
        return jsonify({"fulfillmentText": req["queryResult"]["fulfillmentText"]})

    # If it's a fallback intent, call Gemini
    gemini_payload = {
        "contents": [{"parts": [{"text": user_query}]}]
    }
    
    response = requests.post(GEMINI_URL, json=gemini_payload)
    
    if response.status_code == 200:
        gemini_response = response.json()
        
        # Extract response properly
        bot_reply = gemini_response.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "I'm not sure how to respond.")
    else:
        bot_reply = "Sorry, I couldn't get a response from Gemini."

    return jsonify({"fulfillmentText": bot_reply})

if __name__ == '__main__':
    app.run(port=5000, debug=True)
