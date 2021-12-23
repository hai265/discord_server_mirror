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
    url = "https://cdn.discordapp.com/avatars/{}/{}.webp".format(user_id,profile['user']['avatar'])
    return url

# Initialize config
f = open("config.json")
config = json.load(f)
guild_to_monitor = config['guild_to_monitor']
channels_to_mirror = config['channels_to_mirror']
bot = discum.Client(token=config['user_token'], log=False)


@bot.gateway.command
def helloworld(resp):
    if resp.event.message:
        m = resp.parsed.auto()
        guildID = m['guild_id'] if 'guild_id' in m else None #because DMs are technically channels too
        channelID = m['channel_id']
        if int(guildID) == int(guild_to_monitor) and channelID in channels_to_mirror:
            channel_to_post_in = channels_to_mirror[str(channelID)]
            username = m['author']['username']
            attachments = m['attachments']
            discriminator = m['author']['discriminator']
            content = m['content']
            avatar_url = get_avatar_picture_url(m['author']['id'],bot)
            # bot.sendFile(str(channel_to_post_in),avatar_url,True)
            # bot.sendMessage(str(channel_to_post_in),"__**{}**__\n{}".format(username, content))
            embed = Embedder()
            embed.title(username)
            embed.thumbnail(avatar_url)
            embed.description(content)
            bot.sendMessage(str(channel_to_post_in),"",embed=embed.read())
            # Send a message to the mirror server

bot.gateway.run(auto_reconnect=True)