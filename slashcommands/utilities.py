import hikari
from hikari import guilds
import lightbulb
from lightbulb import commands
from lightbulb.context.slash import SlashContext
import asyncio

from __main__ import authed_guilds

plugin = lightbulb.Plugin("util")


@plugin.command
@lightbulb.command("util", "Group of commands to help admin and users.", guilds=authed_guilds)
@lightbulb.implements(commands.SlashCommandGroup)
async def util(context: SlashContext):
    await context.resolved()
    pass

@util.child
@lightbulb.command(name='ping',description='Pings the bot.')
@lightbulb.implements(commands.SlashSubCommand)
async def ping(context: SlashContext):
    await context.respond("pong!")      
    
# Command to remind the user after a certain amount of time.
@util.child
@lightbulb.option(name='time',description='The time in s, m, h or d to remind the user.', type=str)
@lightbulb.option(name='message',description='The message to send to the user.', type=str)
@lightbulb.command(name='remind',description='Reminds you in this channel after a certain amount of time.', guilds=authed_guilds)
@lightbulb.implements(commands.SlashSubCommand)
async def remind(context: SlashContext):
    
    # Get channel from context.
    
    channel = context.bot.cache.get_guild_channel(context.get_channel())
    
    # Convert the string of time to seconds.
    timestring = ""
    for letter in context.options.time:
        if letter.isdigit():
            timestring = timestring + letter
        else:
            if letter == 's':
                time = int(timestring)
                break
            elif letter == 'm':
                time = int(timestring) * 60
                break
            elif letter == 'h':
                time = int(timestring) * 60 * 60
                break
            elif letter == 'd':
                time = int(timestring) * 60 * 60 * 24
                break
    # if we didn't get a time, or a letter, then we can't do anything.
    if time is None:
        await context.respond("Invalid time. We expect a format of ()s, ()m, ()h or ()d.")
        return
    # if we didn't get a message, then we can't do anything.
    if context.options.message is None:
        await context.respond("Invalid message. Please provide a message to remind you of.")
        return
    # if we dodn't get the type of time, then we can't do anything.
    if letter is None:
        await context.respond("Invalid time. We expect a format of ()s, ()m, ()h or ()d.")
        return
    
    # Send the message to the user.
    await context.respond("Okay! I will remind you in " + str(time) + " seconds.")
    await asyncio.sleep(5)
    await context.delete_last_response()
    # Now we sleep for time
    await asyncio.sleep(time)
    # Now we send the message to the user
    await channel.send(f'Hey {context.user.mention}! You asked me to remind you: \"{context.options.message}\"')

@util.child
@lightbulb.option(name='time',description='The time in s, m, h or d to remind the user.', type=str)
@lightbulb.option(name='message',description='The message to send to the user.', type=str)
@lightbulb.command(name='privateremind',description='Reminds you in your DMs after a certain amount of time.', guilds=authed_guilds)
@lightbulb.implements(commands.SlashSubCommand)
async def privateremind(context: SlashContext):
    
    # Get channel from context.
    
    channel = context.bot.cache.get_guild_channel(context.get_channel())
    
    
    # Convert the string of time to seconds.
    timestring = ""
    for letter in context.options.time:
        if letter.isdigit():
            timestring = timestring + letter
        else:
            if letter == 's':
                time = int(timestring)
                break
            elif letter == 'm':
                time = int(timestring) * 60
                break
            elif letter == 'h':
                time = int(timestring) * 60 * 60
                break
            elif letter == 'd':
                time = int(timestring) * 60 * 60 * 24
                break
    # if we didn't get a time, or a letter, then we can't do anything.
    if time is None:
        await context.respond("Invalid time. We expect a format of ()s, ()m, ()h or ()d.")
        return
    # if we didn't get a message, then we can't do anything.
    if context.options.message is None:
        await context.respond("Invalid message. Please provide a message to remind you of.")
        return
    # if we dodn't get the type of time, then we can't do anything.
    if letter is None:
        await context.respond("Invalid time. We expect a format of ()s, ()m, ()h or ()d.")
        return
    
    # Send the message to the user.
    await context.respond("Okay! I will remind you in " + str(time) + " seconds.")
    await asyncio.sleep(5)
    await context.delete_last_response()
    # Now we sleep for time
    await asyncio.sleep(time)
    # Now we send the message to the user
    try:
        await context.author.send(f'Hey {context.user.mention}! You asked me to remind you: \"{context.options.message}\"')
    except hikari.UnauthorizedError:
        await channel.send(f'Hey {context.user.mention}! You asked me to remind you: \"{context.options.message}\"\n(I cant reach you at your DMs. You might not accept messages from outsiders!)')
        
@util.child
@lightbulb.option(name='user', description='The user to remind.', type=hikari.Member)
@lightbulb.option(name='time',description='The time in s, m, h or d to remind the user.', type=str)
@lightbulb.option(name='message',description='The message to send to the user.', type=str)
@lightbulb.command(name='remindsomeone',description='Reminds a user in this channel after a certain amount of time.', guilds=authed_guilds)
@lightbulb.implements(commands.SlashSubCommand)
async def remindsomeone(context: SlashContext):
    
    # Get channel from context.
    
    channel = context.bot.cache.get_guild_channel(context.get_channel())
    
    # Convert the string of time to seconds.
    timestring = ""
    for letter in context.options.time:
        if letter.isdigit():
            timestring = timestring + letter
        else:
            if letter == 's':
                time = int(timestring)
                break
            elif letter == 'm':
                time = int(timestring) * 60
                break
            elif letter == 'h':
                time = int(timestring) * 60 * 60
                break
            elif letter == 'd':
                time = int(timestring) * 60 * 60 * 24
                break
    # if we didn't get a time, or a letter, then we can't do anything.
    if time is None:
        await context.respond("Invalid time. We expect a format of ()s, ()m, ()h or ()d.")
        return
    # if we didn't get a message, then we can't do anything.
    if context.options.message is None:
        await context.respond("Invalid message. Please provide a message to remind you of.")
        return
    # if we dodn't get the type of time, then we can't do anything.
    if letter is None:
        await context.respond("Invalid time. We expect a format of ()s, ()m, ()h or ()d.")
        return
    
    # Send the message to the user.
    await context.respond("Okay! I will remind you in " + str(time) + " seconds.")
    await asyncio.sleep(5)
    await context.delete_last_response()
    # Now we sleep for time
    await asyncio.sleep(time)
    # Now we send the message to the user
    await channel.send(f'Hey {context.options.user.mention}! {context.author.username} asked me to remind you: \"{context.options.message}\"')
    
@util.child
@lightbulb.option(name='user', description='The user to remind.', type=hikari.Member)
@lightbulb.option(name='time',description='The time in s, m, h or d to remind the user.', type=str)
@lightbulb.option(name='message',description='The message to send to the user.', type=str)
@lightbulb.command(name='personalremind',description='Reminds you after a certain amount of time.', guilds=authed_guilds)
@lightbulb.implements(commands.SlashSubCommand)
async def personalremind(context: SlashContext):
    
    # Get channel from context.
    
    channel = context.bot.cache.get_guild_channel(context.get_channel())
    
    
    # Convert the string of time to seconds.
    timestring = ""
    for letter in context.options.time:
        if letter.isdigit():
            timestring = timestring + letter
        else:
            if letter == 's':
                time = int(timestring)
                break
            elif letter == 'm':
                time = int(timestring) * 60
                break
            elif letter == 'h':
                time = int(timestring) * 60 * 60
                break
            elif letter == 'd':
                time = int(timestring) * 60 * 60 * 24
                break
    # if we didn't get a time, or a letter, then we can't do anything.
    if time is None:
        await context.respond("Invalid time. We expect a format of ()s, ()m, ()h or ()d.")
        return
    # if we didn't get a message, then we can't do anything.
    if context.options.message is None:
        await context.respond("Invalid message. Please provide a message to remind you of.")
        return
    # if we dodn't get the type of time, then we can't do anything.
    if letter is None:
        await context.respond("Invalid time. We expect a format of ()s, ()m, ()h or ()d.")
        return
    
    # Send the message to the user.
    await context.respond("Okay! I will remind you in " + str(time) + " seconds.")
    await asyncio.sleep(5)
    await context.delete_last_response()
    # Now we sleep for time
    await asyncio.sleep(time)
    # Now we send the message to the user
    try:
        await context.options.user.send(f'Hey {context.options.user.mention}! {context.author.username} asked me to remind you: \"{context.options.message}\"')
    except hikari.UnauthorizedError:
        await channel.send(f'Hey {context.user.username}, Unfortunately, I was unable to remind {context.options.user.username} of your message. They dont accept DMs from me, or people not in their friends list.\nHeres a copy of your message: \"{context.options.message}\"')