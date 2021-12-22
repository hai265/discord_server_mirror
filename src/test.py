import json 
config = {'guild_to_monitor' : 510460368900849664, 'channel_to_post_in' : 717830745338675281}
users = {'1' : "hello", '2' : 'nopp'}
list = []
list.append(config)
list.append(users)
with open('config','w') as outfile:
    json.dump(list,outfile)