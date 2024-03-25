# Voiceflow Transcript Processor

## Overview
This project is designed to fetch transcripts from Voiceflow for a given project ID, create structured dialogues from these transcripts, and then send them to a Google Sheet via Zapier for easy analysis and review. It is particularly useful for conversational analysis, quality assurance, and data tracking of user interactions with a Voiceflow chatbot.

## Features
- Fetches transcripts from the Voiceflow API.
- Processes and structures dialogues into a conversational format.
- Identifies and separates dialogues using specific user and chatbot messages.
- Sends structured dialogue sequences to a Google Sheet via Zapier Webhooks.

## How it Works
The script performs the following steps:
1. Requests transcripts from Voiceflow using a project ID and a given time range.
2. Parses the returned JSON and extracts individual dialogue items.
3. Structures dialogues by distinguishing between chatbot and user messages.
4. Identifies the end of a dialogue sequence based on specific 'goodbye' messages from the chatbot.
5. Compiles all dialogues into a single payload.
6. Sends the payload to a Zapier Webhook, which then populates a Google Sheet.

## Requirements
- Python 3.x
- `requests` library (Install using `pip install requests`)
- Voiceflow account and project with API access
- Zapier account with a configured webhook linked to a Google Sheet

## Setup and Configuration
1. **Clone the Repository:**
- git clone [repository URL]
- cd [repository name]

2. **Install Dependencies:**
- pip install -r requirements.txt

3. **Set Environment Variables:**
- Create a `.env` file in the root of the project.
- Add your Voiceflow `PROJECT_ID` and `AUTHORIZATION_TOKEN`.
- Add your Zapier Webhook `URL`.

