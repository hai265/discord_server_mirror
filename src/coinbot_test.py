from slack import WebClient
from slackbot import SlackBot
import os


slackBot = SlackBot("#random")
slackBot.create_channel("random")
message = slackBot.get_message_payload("hi","random")

# Post the onboarding message in Slack
slackBot.postMessage("Hi","random")
# client.chat_postMessage(**message,icon_url="https://cdn.discordapp.com/avatars/113756127707136002/2fcccde9b88abab6087b65ff68c10bd6.png?size=40", username="diffname")
# 
