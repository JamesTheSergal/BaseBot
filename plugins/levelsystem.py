import random
import hikari
from hikari import guilds
import lightbulb

# Import redb from main.py
from __main__ import redb

#Import lightbulb commands
from lightbulb import commands
from lightbulb.context.slash import SlashContext

# add this for importing this plugin
plugin = lightbulb.Plugin("levelsystem")

# These are for the greetings
greetFront = ["Hello! ", "Nice to meet you! ", "It's a pleasure to meet you! ", "Look! Its- ", "G'day! ", "Howdy! ",
              "Gosh! You scared me! ", "Well hey there! ", "Woah, look! Its- "]
greetEnd = [" we are so happy to meet you! ", " welcome to the server! ", " it's wonderful to see you here! ",
            " good server we have here! "]
greetFinal = ["Have fun!", "Don't get in trouble!", "Have a wonderful time!", "<3", "Make some friends!"]

    
#Listen for a message and then update the user XP in the Redis database.
@plugin.listener(hikari.GuildMessageCreateEvent)
async def levelWhenMessage(context: hikari.GuildMessageCreateEvent):
    
    # check if message is from a DM channel or if the message is from a bot
    if isinstance(await context.message.fetch_channel(), hikari.DMChannel) or context.message.author.is_bot:
        # Return because we don't want to update XP in a DM channel.
        return
    
    if context.message.member.is_system:
        return
    
    # Get needed IDs
    user_id = context.author.id
    server_id = context.get_guild().id
    
    # Get the user's xp and level from the Redis database. If they don't exist, create them.
    currxp = redb.get(f'xp:{user_id}:server_id:{server_id}')
    redb.set(f'xp:{user_id}:server_id:{server_id}', 0) if currxp is None else None
    redb.set(f'level:{user_id}:server_id:{server_id}', 0) if redb.get(f'level:{user_id}:server_id:{server_id}') is None else None
    
    # Get the user's current level in this server.
    currlevel = redb.get(f'level:{user_id}:server_id:{server_id}')
    
    # return character count from message
    charcount = len(context.message.content)
    # For each character, add 0.72 to the user's XP.
    addxp = charcount * 0.72
    
    # Add the XP to the user's current XP and set it in the database.
    if currxp is None:
        currxp = 0
    if addxp is None:
        addxp = 0
    addxp = int(currxp) + int(addxp)
    redb.set(f'xp:{user_id}:server_id:{server_id}', addxp)
    
    # Calculate if the user has leveled up.
    if addxp >= int(currlevel) * int(250 * (1.1 ** int(currlevel))):
        # If they have, add 1 to their level.
        redb.set(f'level:{user_id}:server_id:{server_id}', int(currlevel) + 1)
        # Check to see if there is a preference of channel to use for leveling
        if redb.get(f"levelchannel-{context.get_guild().id}") is not None:
            # If there is, get the channel ID from the Redis database.
            levelchannel = redb.get(f"levelchannel-{context.get_guild().id}")
            channeltarget: hikari.GuildChannel = plugin.bot.cache.get_guild_channel(levelchannel)
            if channeltarget is not None:
                
                # We have a leveling channel. Lets send a nice embed.
                embed = ( 
                    hikari.Embed(
                        title="Levelup!",
                        description='Great Job for leveling up! Keep up the great work!',
                        color=hikari.Color.from_rgb(186, 21, 232),
                    )
                    .set_thumbnail(context.author.avatar_url)
                    .add_field("Level: ", value=int(currlevel) + 1, inline=False)
                    .add_field("Messages: ", value=redb.get(f'messagecount:{user_id}:server_id:{server_id}') if redb.get(f'messagecount:{user_id}:server_id:{server_id}') is not None else 1, inline=True)
                    .add_field("XP to next level:", value=((int(currlevel)+1) * int(250 * (1.1 ** int(currlevel)+1))) - addxp, inline=True)
                )
                await channeltarget.send(context.author.mention, embed=embed)
                
            else:
                await context.get_channel().send(f"{context.author.mention} You've leveled up to level {int(currlevel) + 1}! (Also please tell your admin to set up the levelup channel again. Thanks <3)")     
        else:
            # Send a message to the user letting them know they've leveled up.
            await context.get_channel().send(f"{context.author.mention} You've leveled up to level {int(currlevel) + 1}!")
    
    # If they have leveled up, see if there is a role to give them.
    nowlevel = redb.get(f'level:{user_id}:server_id:{server_id}')
    if int(currlevel) < int(redb.get(f'level:{user_id}:server_id:{server_id}')):
        # If there is, get the role ID from the Redis database.
        if redb.exists(f'levelrole-{server_id}-{int(currlevel) + 1}'):
            roleid = redb.get(f'levelrole-{server_id}-{int(currlevel) + 1}')
            # If there is, get the role from the server.
            role = context.get_guild().get_role(roleid)
            # If there is, add the role to the user.
            if role is not None:
                
                # Now get the user's other roles. If there was a previous levelup role, we want to remove the old one.
                user = await plugin.bot.rest.fetch_member(server_id, user_id)
                
                # put their role IDs in an array so we can quickly search for them.
                hasids = []
                for hasroles in user.get_roles():
                    hasids.append(hasroles.id)
                
                # Now we will do a key search in the Redis database to see if there is a previous levelup role. If they have one, we will remove them.
                otherroles = redb.keys(f'levelrole-{server_id}-*')
                for rolekey in otherroles:
                    testroleid = int(redb.get(rolekey))
                    if testroleid in hasids:
                        await user.remove_role(testroleid)
                        
                # Add the role new using REST.
                await plugin.bot.rest.add_role_to_member(server_id, user_id, role, reason="Added levelup role.")
                
            else:
                # If the role was none, there was a problem. Don't do anything hasty, just let the user know.
                await context.get_channel().send(f"There was a problem adding the levelup role to {context.author.mention}. Please contact your administrator.")   
        else:
            # There was no role set by the admin. Just pass.
            pass
            
#Listen for a message and then incrament.
@plugin.listener(hikari.GuildMessageCreateEvent)
async def recordmessage(context: hikari.GuildMessageCreateEvent):
    # check if message is from a DM channel or if the message is from a bot
    if isinstance(await context.message.fetch_channel(), hikari.DMChannel) or context.message.author.is_bot:
        # Return because we don't want to update XP in a DM channel.
        return
    
    # Get the user's ID.
    user_id = context.author.id
    # Get the server's ID.
    server_id = context.get_guild().id
    
    # add 1 to the user's message count in this server
    redb.set(f'messagecount:{user_id}:server_id:{server_id}', int(redb.get(f'messagecount:{user_id}:server_id:{server_id}')) + 1 if redb.get(f'messagecount:{user_id}:server_id:{server_id}') is not None else 1) # This line of code is fucking crazy.

# Listen for user join and then add them to the Redis database.
@plugin.listener(hikari.MemberCreateEvent)
async def adduser(context: hikari.MemberCreateEvent):
    
    # Get user id and add them to the Redis database.
    user_id = context.user_id
    server_id = context.guild_id

    # Check to see if the user already exists in the Redis database.
    # check user xp
    if redb.exists(f'xp:{user_id}:server_id:{server_id}'):
        pass
    else:
        #Then set the user's XP to 0.
        redb.set(f'xp:{user_id}:server_id:{server_id}', 0)
    # check user level
    if redb.exists(f'level:{user_id}:server_id:{server_id}'):
        pass
    else:
        redb.set(f'level:{user_id}:server_id:{server_id}', 0)
        
    # Check if there is a welcome channel in this server.
    if redb.exists(f"welcomechannel-{context.get_guild().id}"):
        welcomechannel = redb.get(f"welcomechannel-{context.get_guild().id}")
        channeltarget: hikari.GuildChannel = plugin.bot.cache.get_guild_channel(welcomechannel)
        if channeltarget is not None:
            front = random.randrange(0, len(greetFront) - 1)
            end = random.randrange(0, len(greetEnd) - 1)
            final = random.randrange(0, len(greetFinal) - 1)
            
            embed = (
                hikari.Embed(
                    title=greetFront[front],
                    description=context.member.mention + greetEnd[end] + greetFinal[final],
                    color=hikari.Color.from_rgb(random.randrange(1, 255), random.randrange(1, 255),
                                               random.randrange(1, 255))
                )
                .set_image(context.member.avatar_url)
            )
            await channeltarget.send(embed=embed)