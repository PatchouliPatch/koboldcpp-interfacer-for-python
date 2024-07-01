import requests
import json

# Define the URL of the API
url = "http://127.0.0.1:5001/api/v1/generate"

# Define the payload with the parameters
payload = {
    "max_context_length": 8000,
    "max_length": 1000,
    "prompt": "Niko the kobold stalked carefully down the alley, his small scaly figure obscured by a dusky cloak that fluttered lightly in the cold winter breeze.",
    "quiet": False,
    "rep_pen": 1.1,
    "rep_pen_range": 256,
    "rep_pen_slope": 1,
    "temperature": 0.5,
    "tfs": 1,
    "top_a": 0,
    "top_k": 100,
    "top_p": 0.9,
    "typical": 1
}

# Set the headers
headers = {
    "Content-Type": "application/json"
}

# Send the POST request
response = requests.post(url, data=json.dumps(payload), headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    result = response.json()
    print("Generated Text:", result['results'][0]['text'])
else:
    print("Error:", response.status_code, response.text)

