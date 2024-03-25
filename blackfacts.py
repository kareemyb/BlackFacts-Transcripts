import requests
import json

project_id = "65a1efe377a05bcdc339cb14"
authorization_token = "VF.DM.65f1dc9e31cdf17d1e7493a3.5myyvjDQ7zYbFdA1"

# API endpoint for fetching the transcripts
url = f"https://api.voiceflow.com/v2/transcripts/{project_id}?range=Last%207%20Days"

headers = {
    "accept": "application/json",
    "Authorization": f"{authorization_token}"
}

response = requests.get(url, headers=headers)

# Parse the JSON response to a Python list
output = json.loads(response.text)

# Extract transcript IDs into a list
transcript_ids = [transcript["_id"] for transcript in output]


# Initialize a list to store all dialogue sequences
all_dialogues = []

# Loop through each transcript ID
for transcript_id in transcript_ids:
    url = f"https://api.voiceflow.com/v2/transcripts/{project_id}/{transcript_id}"

    # Initialize a list to store the current dialogue sequence
    dialogue_sequence = []

    # Make the GET request
    response = requests.get(url, headers=headers)

    # Load the transcript data
    transcript_data = json.loads(response.text)

    # Iterate through each item in the transcript data
    for item in transcript_data:
        # Extract chatbot messages
        if item['type'] == 'text' and 'message' in item['payload']['payload']:
            chatbot_message = item['payload']['payload']['message']
            if chatbot_message:  # Ensure the message is not empty
                dialogue_sequence.append({'Speaker': 'Chatbot', 'Message': chatbot_message})
                # Check if the message is a goodbye message
                if "feel free to open this chat again" in chatbot_message or "Don't hesitate to restart this chat" in chatbot_message:
                    all_dialogues.append(dialogue_sequence)
                    dialogue_sequence = []

        # Extract user messages (button selections and message selections)
        if item['type'] == 'request':
            user_message = ""
            if item['payload']['type'] == 'intent' and 'query' in item['payload']['payload']:
                user_message = item['payload']['payload']['query']
            elif item['payload']['type'].startswith('path-') and 'label' in item['payload']['payload']:
                user_message = item['payload']['payload']['label']

            if user_message:  # Ensure the message is not empty
                dialogue_sequence.append({'Speaker': 'User', 'Message': user_message})

    # Add the last dialogue sequence if it's not empty and not already added
    if dialogue_sequence and dialogue_sequence != all_dialogues[-1]:
        all_dialogues.append(dialogue_sequence)

# Prepare all dialogues as one payload
all_dialogues_text = ["\n".join([f"{entry['Speaker']} : {entry['Message']}" for entry in dialogue]) for dialogue in all_dialogues]
all_dialogues_payload = "\n--- New Dialogue ---\n".join(all_dialogues_text)

# Send the payload to Zapier
def send_data_to_zapier(all_dialogues_payload):
    webhook_url = "https://hooks.zapier.com/hooks/catch/16736801/30t24js/"
    headers = {"Content-Type": "application/json"}
    data = {"dialogues": all_dialogues_payload}
    response = requests.post(webhook_url, json=data, headers=headers)
    if response.status_code == 200:
        print("Data sent successfully")
    else:
        print("Failed to send data")

send_data_to_zapier(all_dialogues_payload)

