# Discord Server Mirror 
## A program to mirror discord channels and post them to slack

# Build Instructions
Install docker, and then run `docker build discord_mirror .`
# Run Instructions
Run `docker run -e DISCORD_TOKEN=YOURTOKENHERE -e SLACK_TOKEN=YOURTOKENHERE discord_mirror` 