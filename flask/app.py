import requests
import json

# Replace this with your actual ngrok URL
ngrok_url = "https://29c9-104-199-9-119.ngrok-free.app"

# The endpoint you want to call
url = f"{ngrok_url}/generate"

# The prompt data to send to the Flask app
data = {
    "prompt": "Tell me about financial planning"  # Modify your prompt as needed
}

try:
    # Sending the POST request
    response = requests.post(url, json=data)
    
    # Check if the request was successful
    if response.status_code == 200:
        result = response.json()
        print("Generated advice:", result.get("advice"))
    else:
        print(f"Error: {response.status_code}, {response.text}")
except Exception as e:
    print(f"An error occurred: {e}")
