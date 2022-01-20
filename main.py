import os
import hikari
import lightbulb
from lightbulb import Plugin
from pathlib import Path
from importlib import import_module
import redis

# Create a lightbulb bot

# NOTES
# New post when image - New video when video

authed_guilds = [916545175818473482]

def create_lightbulbBot():
    bot = lightbulb.BotApp(
        token="", 
        intents=hikari.Intents.ALL, 
        ignore_bots=True, 
        owner_ids=[299742661290622977],
        default_enabled_guilds=[916545175818473482],
        logs="DEBUG")
    
    # Use import_module to import the plugin object from each plugin file
    print("Loading slash commands and groups...")
    slashcoms = Path("slashcommands").glob("*.py")
    for c in slashcoms:
        mod = import_module(f"slashcommands.{c.stem}")
        bot.add_plugin(mod.plugin)
    
    print("Loading plugins...")
    plugins = Path("plugins").glob("*.py")
    for c in plugins:
        mod = import_module(f"plugins.{c.stem}")
        bot.add_plugin(mod.plugin)
        print("plugins.{c.stem}")
    

    
        
    return bot  # Return the lightbulb bot

# check OS to see if we need to import uvloop

if os.name != "nt":
    import uvloop
    uvloop.install()
    
# Start the bot

if __name__ == "__main__":
    
    # Before starting the bot, make a connection to a redis database
    print("Connecting to Redis...")
    redb = redis.Redis(host="5.161.60.66", port=6379, decode_responses=True, password="", db=1) # DB 1 for this bot
    # test redis connection
    print(f"Redis time: {redb.time()}")
    
    # Now create and start the bot
    bot = create_lightbulbBot()
    bot.run(activity=hikari.Activity(
        name="Testing.",
        type=hikari.ActivityType.PLAYING
    ))
    
    print("bot is non-blocking")
    