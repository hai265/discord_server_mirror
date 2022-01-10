# import the random library to help us generate the random numbers
import random
from slack import WebClient
from slack.errors import SlackApiError
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
    def __init__(self):
        logging.info("Slack bot initialized")
        self.client = WebClient(token=os.environ.get("SLACK_TOKEN"))
        # Get the channels in the workspace
        self.channels = self.client.conversations_list()["channels"]
        # Send a message to the slack #bot-status channel
        self.postMessage("Slack bot initialized.","bot-status")

    # Generate a random number to simulate flipping a coin. Then return the
    # crafted slack payload with the coin flip message.
    def generate_slack_message(self, text : str):
        return {"type": "section", "text": {"type": "mrkdwn", "text": text}}

    # Craft and return the entire message payload as a dictionary.
    def get_message_payload(self, text : str, channelName : str):
        # return {
        #     "channel": channelName,
        #     "text": [
        #         *self.generate_slack_message(text),
        #     ],
        # }
        return {
            "channel": channelName,
            "text": text
        }
    # Posts a message to the specified channel. Can add username and icon to post on behalf of that user
    def postMessage(self,msg : str, channel_name : str,uName = '',iconUrl = ''):
        # Create channel if it does not exist already
        if not self.channel_exists(channel_name):
            self.create_channel(channel_name)
        # self.client.conversations_join(channel = self.channel_name_to_id(channel_name))
        message = self.get_message_payload(msg,channel_name)
        # Post the onboarding message in Slack
        self.client.chat_postMessage(**message,username = uName, icon_url = iconUrl)
    def create_channel(self,channel_name : str):
        # Create a new channel with the name
        try:
            response = self.client.conversations_create(
            name=channel_name,
            is_private = False
            )
            # Update list of channels
            self.channels.append(response["channel"])
        except SlackApiError as e:
            logging.info(e.response["error"])
            return
        logging.info("Channel {} created".format(channel_name))
    # Returns true if a channel with the name exists in the workspace. False otherwise
    def channel_exists(self,channel_name : str):
        for channel in self.channels:
            # Channel already exists - do not create the channel
                if channel_name == channel["name"]:
                    return True
        return False
    # Returns a channel id give na channel name
    def channel_name_to_id(self,channel_name : str):
        response = self.client.conversations_list()
        conversations = response["channels"]
        for conversation in conversations:
            # Channel already exists - do not create the channel
            if conversation["name"] == channel_name:
                return conversation["id"]

