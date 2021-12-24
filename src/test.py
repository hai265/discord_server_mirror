import json 
config = {'guild_to_monitor' : [510460368900849664,321], "channels_to_post" : {"original_channel_1" : "mirror_channel 2","original_channel2" : "mirror_channel 2x"}}
with open('test.json','w') as outfile:
    json.dump(config,outfile, indent=2)
    json.loads