import time
import discum    
import json
from discum.discum import Client 
from discum.utils.embed import Embedder
from datetime import datetime
import random
from requests.api import request
from json_minify import json_minify
import schedule
import datetime
import threading
# From a User id, grab the avatar picture
def get_avatar_picture_url(user_id, bot : Client):
    profile = bot.getProfile(user_id).json()
    url = "https://cdn.discordapp.com/avatars/{}/{}.webp?size=96".format(user_id,profile['user']['avatar'])
    return url

def print_status(bot : Client, channel_to_post : str):
    current_time = datetime.datetime.now()
    print("Bot status: operational {} ".format(current_time))
    bot.sendMessage(str(channel_to_post),"Time started:{} ".format(current_time))    
def print_status_thread(bot : Client, channel_to_post : str, time_to_send_status : str):
    print_status(bot, config["status channel"])
    schedule.every().day.at(time_to_send_status).do(print_status,bot = bot, channel_to_post = config["status channel"])
    # schedule.every(10).seconds.do(print_status,bot = bot, channel_to_post = config["debug channel"])
    while True:
        schedule.run_pending()
        time.sleep(60)
        

# Initialize config
f = open("config.json")
json_string = f.read().replace("// *","")
config = json.loads(json_minify(json_string))
guilds_to_monitor = config['guilds_to_monitor']
channels_to_mirror = config['channels_to_mirror']
random.seed()
bot = discum.Client(token=config['user token'], log=False)
# Start the status thread
status_thread = threading.Thread(target=print_status_thread,args=(bot,config["status channel"],config["time to send status"]))
status_thread.start()
@bot.gateway.command
def monitor_channels(resp):
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