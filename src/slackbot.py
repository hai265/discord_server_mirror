# import the random library to help us generate the random numbers
import random
from slack import WebClient
import os
import logging
# Create the CoinBot Class
class SlackBot:
    # Create a constant that contains the default text for the message
    MESSAGE_BLOCK = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": (
                "Sure! Flipping a coin....\n\n"
            ),
        },
    }
    # The constructor for the class. It takes the channel name as the a
    # parameter and then sets it as an instance variable
    def __init__(self, channel : str):
        logging.info("Slack bot initialized")
        self.client = WebClient(token=os.environ.get("SLACK_TOKEN"))
        # Send a message to the slack #bot-status channel
        self.postMessage("Slack bot initialized.","bot-status")

    # Generate a random number to simulate flipping a coin. Then return the
    # crafted slack payload with the coin flip message.
    def generate_slack_message(self, text : str):
        return {"type": "section", "text": {"type": "mrkdwn", "text": text}},

    # Craft and return the entire message payload as a dictionary.
    def get_message_payload(self, text : str, channelName : str):
        return {
            "channel": channelName,
            "blocks": [
                *self.generate_slack_message(text),
            ],
        }
    def postMessage(self,msg : str, channel_name : str,uName = '',iconUrl = ''):
        # self.client.conversations_join(channel = self.channel_name_to_id(channel_name))
        message = self.get_message_payload(msg,channel_name)
        # Post the onboarding message in Slack
        self.client.chat_postMessage(**message,username = uName, icon_url = iconUrl)
    def create_channel(self,channel_name : str):
        response = self.client.conversations_list()
        conversations = response["channels"]
        for conversation in conversations:
            # Channel already exists - do not create the channel
            if conversation["name"] == channel_name:
                print("Channel name already exists")
                logging.info("Tried to create channel {} but already exists".format(channel_name))
                return
        # Create a new channel with the name
        response = self.client.conversations_create(
        token=os.environ.get("SLACK_TOKEN"),
        name=channel_name,
        is_private = False
        )
        logging.info("Channel {} created".format(channel_name))
    # Returns a channel id give na channel name
    def channel_name_to_id(self,channel_name : str):
        response = self.client.conversations_list()
        conversations = response["channels"]
        for conversation in conversations:
            # Channel already exists - do not create the channel
            if conversation["name"] == channel_name:
                return conversation["id"]

