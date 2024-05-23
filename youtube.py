from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Load environment variables from a .env file if present
from dotenv import load_dotenv # type: ignore
load_dotenv()

BASE_URL = os.getenv("BASE_URL", "base_url")
CHANNEL_ID = "UCvrhS9flDBke2HxvARGvt5g"
CALLBACK_URL = f"{BASE_URL}/youtube/notifications"
HUB_URL = "https://pubsubhubbub.appspot.com/subscribe"

def subscribe_to_channel():
    data = {
        'hub.mode': 'subscribe',
        'hub.topic': f'https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}',
        'hub.callback': CALLBACK_URL,
        'hub.verify': 'async'
    }
    response = requests.post(HUB_URL, data=data)
    if response.status_code == 202:
        print("Subscription request accepted.")
    else:
        print("Failed to subscribe:", response.status_code, response.text)

@app.route('/youtube/notifications', methods=['GET', 'POST'])
def notifications():
    if request.method == 'GET':
        # Handle subscription verification
        hub_mode = request.args.get('hub.mode')
        hub_challenge = request.args.get('hub.challenge')
        hub_verify_token = request.args.get('hub.verify_token')
        
        if hub_mode == 'subscribe':
            return hub_challenge, 200
        return "Verification failed", 403
    
    if request.method == 'POST':
        # Handle notification
        print("New Video Notification Received")
        print(request.data)
        return "OK", 200

if __name__ == '__main__':
    # Subscribe to the channel on startup
    subscribe_to_channel()
    app.run(port=8001, debug=True)
