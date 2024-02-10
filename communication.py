import slack_sdk
import os

def generate_msg(msg, channel):
    slack_client = slack_sdk.WebClient(token=os.getenv("SLACK_BOT"))

    slack_client.chat_postMessage(channel=channel, text=f"{msg}", mrkdwn=True)
