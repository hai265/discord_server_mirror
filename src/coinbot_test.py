from slack import WebClient
from starterbot import CoinBot
import os

slack_web_client = WebClient(token=os.environ.get("SLACK_TOKEN"))

coin_bot = CoinBot("#random")

message = coin_bot.get_message_payload()

# Post the onboarding message in Slack
slack_web_client.chat_postMessage(**message)
slack_web_client.chat_postMessage(**message,icon_url="https://cdn.discordapp.com/avatars/113756127707136002/2fcccde9b88abab6087b65ff68c10bd6.png?size=40", username="diffname")
# 