import time
import discum    
import json
from discum.discum import Client 
from discum.utils.embed import Embedder
from datetime import datetime
import random
from requests.api import request

import schedule
import datetime
import threading
import os
from slackbot import SlackBot
import re
# From a User id, grab the avatar picture
def get_avatar_picture_url(user_id, bot : Client):
    profile = bot.getProfile(user_id).json()
    # Return default discord pfp if lookup failed
    if 'user' not in profile:
        return 'https://discord.com/assets/1f0bfc0865d324c2587920a7d80c609b.png'
    # Check for "unknown user and code 10013"
    url = "https://cdn.discordapp.com/avatars/{}/{}.png?size=96".format(user_id,profile['user']['avatar'])
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
# Converts messages containing <user_id> to @mentions, m is the whole message w/ metadata
def process_message(m):
    # If the message is a reply of another message, process the original message and append it to beginning of message
    if m['type'] == 'reply':
        referenced_message ='*{0}*: {1}\n *Reply:* '.format(m['referenced_message']['author']['username'],process_message(m['referenced_message']))
        # referenced_message = m['referenced_message']['author']['username'] +':' + process_message(m['referenced_message']) +'\n*Reply: *'
    else:
        referenced_message = ''
    # Split message according to space
    msg_split = m['content'].split(" ")
    mentions = m['mentions']
    # Go thru the message and iterate through it
    mentioned_user = 0
    for i in range(0,len(msg_split)):
        if re.search("<@?!\d+>",msg_split[i]):
            msg_split[i] = '@' + mentions[mentioned_user]['username']
            mentioned_user += 1
    return referenced_message  + ' '.join(msg_split)




        


# Old config to send to discord
random.seed()
discord_bot = discum.Client(token=os.environ.get("DISCORD_TOKEN"), log=False)
# Initialize slack bot
slack_bot = SlackBot()
slack_bot.load_config("config/config.json")
# From the config file, create channels that do not exist already
# for channel in channels_to_mirror.values():
#     slack_bot.create_channel(channel)
# Start the status thread
# status_thread = threading.Thread(target=print_status_thread,args=(discord_bot,config["status channel"],config["time to send status"]))
# status_thread.start()
@discord_bot.gateway.command
def monitor_channels(resp):
    loaded = False
    # Initialize config
    # TODO: Load configs once
    # if not loaded:
    #     f = open("old_config.json")
    #     json_string = f.read().replace("// *","")
    #     config = json.loads(json_minify(json_string))
    #     guilds_to_monitor = config['guilds_to_monitor']
    #     channels_to_mirror = config['channels_to_mirror']
    #     f.close()
    #     loaded = True
    if resp.event.message:
        m = resp.parsed.auto()
        guildID = m['guild_id'] if 'guild_id' in m else None #because DMs are technically channels too
        channelID = m['channel_id']
        # Send the message to discord
        # if guildID in guilds_to_monitor and channelID in channels_to_mirror:
        #     channel_to_post_in = channels_to_mirror[str(channelID)]
        #     username = m['author']['username']
        #     attachments = m['attachments']
        #     discriminator = m['author']['discriminator']
        #     content = m['content']
        #     print("> guild {} channel {} | {}#{}: {} with {} attachments".format(guildID, channelID, username, discriminator, content, len(attachments)))
        #     avatar_url = get_avatar_picture_url(m['author']['id'],discord_bot)
        #     embed = Embedder()
        #     # Send message in an embed
        #     embed.title(username)
        #     embed.thumbnail(avatar_url)
        #     if len(content) != 0:
        #         embed.description(content)
        #         discord_bot.sendMessage(str(channel_to_post_in),"",embed=embed.read())
        #     # Send the attachments
        #     embed.description("")
        #     for attachment in attachments:
        #         time.sleep(random.randrange(1,3) + (random.randrange(0,100) / 100))
        #         embed.image(attachment['url'])
        #         discord_bot.sendMessage(str(channel_to_post_in),"",embed=embed.read())
        # Send the message to slack
        # if not loaded1:
        #     f = open("config.json")
        #     json_string = f.read().replace("// *","")
        #     config = json.loads(json_minify(json_string))
        #     guilds_to_monitor = config['guilds_to_monitor']
        #     channels_to_mirror = config['channels_to_mirror']
        #     loaded1=True

        if guildID in slack_bot.guilds_to_monitor and channelID in slack_bot.channels_to_mirror:
            username = m['author']['username']
            attachments = m['attachments']
            discriminator = m['author']['discriminator']
            content = process_message(m)
            print("> guild {} channel {} | {}#{}: {} with {} attachments".format(guildID, channelID, username, discriminator, content, len(attachments)))
            avatar_url = get_avatar_picture_url(m['author']['id'],discord_bot)
            # Send a message to the mirror server
            # Send the message in the appropriate slack channel
            user_name = m["author"]["username"]
            # Add attachment links in content as links
            for attachment in attachments:
                content += "\n" + str(attachment["url"])
            slack_bot.postMessage(
                content, slack_bot.channels_to_mirror[str(channelID)], user_name, avatar_url)

discord_bot.gateway.run(auto_reconnect=True)