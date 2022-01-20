import asyncio
import hikari
from hikari import guilds
from hikari.impl import bot
import lightbulb
from lightbulb import commands
from lightbulb.app import BotApp
from lightbulb.context.slash import SlashContext

# Import redb from main.py
from __main__ import redb

# add this for importing this plugin
plugin = lightbulb.Plugin("basebotadmin", "Admin commands for the bot.")
#gotguilds = plugin.app.rest.fetch_my_guilds()
#for id in gotguilds:
#    print(id)


@plugin.command
@lightbulb.add_checks(lightbulb.owner_only)
@lightbulb.command("basebotadmin", "Group of commands for the bot owner", guilds=[916545175818473482])
@lightbulb.implements(commands.SlashCommandGroup)
async def basebotadmin(context: SlashContext):
    pass

@basebotadmin.child
@lightbulb.add_checks(lightbulb.owner_only)
@lightbulb.option("user", "The user to clean up in this server.", hikari.User)
@lightbulb.command("clearuser", "Cleans a user from the database", guilds=[916545175818473482])
@lightbulb.implements(commands.SlashSubCommand)
async def clearuser(context: SlashContext):
    """
    Cleans a user from the database.
    """
    
    print("Cleaning up user...")
    
    user: hikari.Member = context.options.user
    user_id = user.id
    server_id = context.get_guild().id
    
    # Check redis to see if the user has a level, or xp.
    if redb.get(f'xp:{user_id}:server_id:{server_id}') is None:
        print("User does not have xp.")
        await context.respond("User does not have xp.")
    else:
        redb.delete(f'xp:{user_id}:server_id:{server_id}')
        redb.delete(f'level:{user_id}:server_id:{server_id}')
        await context.respond("User has been cleaned up.")
    await asyncio.sleep(5)
    await context.delete_last_response()

@basebotadmin.child
@lightbulb.add_checks(lightbulb.owner_only)
@lightbulb.option("user", "The user to clean up in an external server (USER ID).", int)
@lightbulb.option("guild", "Guild ID.", int)
@lightbulb.command("remoteclear", "Cleans a user from the database outside of this server", guilds=[916545175818473482])
@lightbulb.implements(commands.SlashSubCommand)
async def remoteclear(context: SlashContext):
    """
    Cleans a user from the database.
    """
    
    print("Cleaning up user...")
    
    user_id = context.options.user
    server_id = context.options.guild
    
    # Check redis to see if the user has a level, or xp.
    if redb.get(f'xp:{user_id}:server_id:{server_id}') is None:
        print("User does not have xp or does not exist.")
        await context.respond("User does not have xp or does not exist.")
    else:
        redb.delete(f'xp:{user_id}:server_id:{server_id}')
        redb.delete(f'level:{user_id}:server_id:{server_id}')
        await context.respond("User has been cleaned up.")
    await asyncio.sleep(5)
    await context.delete_last_response()
        

    