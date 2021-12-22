import discum    
import json
import http
from discum.discum import Client 
from discum.utils.embed import Embedder
import requests

from requests.api import request


# From a User id, grab the avatar picture
def get_avatar_picture_url(user_id, bot : Client):
    profile = bot.getProfile(user_id).json()
    url = "https://cdn.discordapp.com/avatars/{}/{}.webp?size=40".format(user_id,profile['user']['avatar'])
    return url

bot = discum.Client(token='mfa.21O17pDpBaqib9C1nctBvYkQFDkC-Yd4SX5b390NW7TmBKv6OgLP2U24yZrTafWuXQ-uaERMklmctHAPovdG', log=False)


# Guild ID to monitor messages in
guild_to_monitor = 510460368900849664
# Channel to post things in
channel_to_post_in = 717830745338675281
@bot.gateway.command
def helloworld(resp):
    if resp.event.message:
        m = resp.parsed.auto()
        guildID = m['guild_id'] if 'guild_id' in m else None #because DMs are technically channels too
        channelID = m['channel_id']
        if int(guildID) == int(guild_to_monitor) and int(channelID) != int(channel_to_post_in):
            username = m['author']['username']
            discriminator = m['author']['discriminator']
            content = m['content']
            # bot.sendMessage(str(channel_to_post_in),"> guild {} channel {} | {}#{}: {}".format(guildID, channelID, username, discriminator, content))
            avatar_url = get_avatar_picture_url(m['author']['id'],bot)
            bot.sendFile(str(channel_to_post_in),avatar_url,True)
            bot.sendMessage(str(channel_to_post_in),"**{}**\n{}".format(username, content))
            # Send a message to the mirror server

bot.gateway.run(auto_reconnect=True)