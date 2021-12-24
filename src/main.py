import discum    
import json
from discum.discum import Client 
from discum.utils.embed import Embedder
from datetime import datetime
import random
from requests.api import request
# From a User id, grab the avatar picture
def get_avatar_picture_url(user_id, bot : Client):
    profile = bot.getProfile(user_id).json()
    url = "https://cdn.discordapp.com/avatars/{}/{}.webp?size=40".format(user_id,profile['user']['avatar'])
    return url

# Initialize config
now = datetime.now()
f = open("config.json")
config = json.load(f)
guilds_to_monitor = config['guilds_to_monitor']
channels_to_mirror = config['channels_to_mirror']
bot = discum.Client(token=config['user_token'], log=False)
random.seed()
print("Time started: {} ".format(now))
bot.sendMessage(str(config['debug_channel']),"Time started:{} ".format(now))
@bot.gateway.command
def helloworld(resp):
    if resp.event.message:
        m = resp.parsed.auto()
        guildID = m['guild_id'] if 'guild_id' in m else None #because DMs are technically channels too
        channelID = m['channel_id']
        if guildID in guilds_to_monitor and channelID in channels_to_mirror:
            channel_to_post_in = channels_to_mirror[str(channelID)]
            username = m['author']['username']
            attachments = m['attachments']
            discriminator = m['author']['discriminator']
            content = m['content']
            avatar_url = get_avatar_picture_url(m['author']['id'],bot)
            embed = Embedder()
            # Send message in an embed
            embed.title(username)
            embed.thumbnail(avatar_url)
            if len(content) != 0:
                embed.description(content)
                bot.sendMessage(str(channel_to_post_in),"",embed=embed.read())
            # Send the attachments
            embed.description("")
            for attachment in attachments:
                time.sleep(random.randrange(1,3) + (random.randrange(0,100) / 100))
                embed.image(attachment['url'])
                bot.sendMessage(str(channel_to_post_in),"",embed=embed.read())
            print("> guild {} channel {} | {}#{}: {} with {} attachments".format(guildID, channelID, username, discriminator, content, len(attachments)))
            # Send a message to the mirror server

bot.gateway.run(auto_reconnect=True)