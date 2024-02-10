import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk.errors import SlackApiError
import urllib.parse
import pprint
import slack_sdk
from communication import generate_msg
from transcript_verifier import script_verifier

from dotenv import load_dotenv

load_dotenv()

# Initializes your app with your bot token and socket mode handler
app = App(token=os.environ["SLACK_APP"])
slack_client = slack_sdk.WebClient(token=os.getenv("SLACK_BOT"))

def get_user_first_name(user_id):
    try:
        result = slack_client.users_info(user=user_id)
        if result['ok']:
            # Retrieve the user's first name from the result
            first_name = result['user']['profile']['first_name']
            first_name=first_name.split('.')[0]
            return first_name
        else:
            print("Could not retrieve user info: " + result['error'])
    except SlackApiError as e:
        print(f"Error fetching user info: {e.response['error']}")

@app.event("app_mention")
def handle_mention(body, logger):
    event = body["event"]
    channel_id = event["channel"]
    first_name=get_user_first_name(event.get("user")).capitalize()
    elements = event["blocks"][0]["elements"][0]["elements"]
    user_prompt = ""

    for element in elements:
        if element["type"] == "text":
            user_prompt += element["text"]  # Add text to the prompt
        elif element["type"] == "link":
            user_prompt += element["url"]  # Add URL to the prompt
    
    print("handle_mention", user_prompt)

    generate_msg("Hey " + first_name + ". I am verifying this Loom video!", channel_id)

    ai_response = script_verifier(user_prompt)

    generate_msg(ai_response, channel_id)

    # sequences, url = workflow(user_prompt)

    # generate_msg(url, channel_id)


# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP"]).start()