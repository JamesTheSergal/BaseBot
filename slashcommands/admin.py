import asyncio
from typing import Mapping
from typing_extensions import Required
import hikari
from hikari import snowflakes
from hikari import guilds
from hikari.channels import GuildChannel
import lightbulb
import collections
from lightbulb.errors import LightbulbError
from matplotlib import colors # This is for the color picker

# Import redb from main.py
from __main__ import redb
from __main__ import authed_guilds

from lightbulb import commands
from lightbulb.context.slash import SlashContext

# add this for importing this plugin
plugin = lightbulb.Plugin("admin")

# Action reporter
async def reportaction(context: SlashContext, act_title: str, action: str, sucessful: bool, had_permission: bool):
    if redb.exists(f'workreportchannel-{context.guild_id}'):
        channelid = redb.get(f'workreportchannel-{context.guild_id}')
        try:
            workchannel = await plugin.bot.rest.fetch_channel(channelid)
            embed = (
                hikari.Embed(
                    title=act_title,
                    description=f'Action by: {context.author.mention}\nWhere:{context.get_channel().mention}'
                )
                .set_thumbnail(context.author.avatar_url)
            )
            if sucessful:
                embed.add_field("Action state:", value="Executed Successfully", inline=True)
            else:
                embed.add_field("Action state:", value="Failed", inline=True)
                
            if had_permission:
                embed.add_field("Had Permission:", value="Yes", inline=True)
            else:
                embed.add_field("Had Permission:", value="No", inline=True)
            
            embed.add_field("Action:", value=action, inline=False)
            
            
            await workchannel.send(embed=embed)
        except:
            await context.get_guild().fetch_owner().send("Please reset your work channel, or remove it from the bot's config.")
            pass

# Authorization helper
async def isauthorized(context):
    
    membergot: hikari.Member = await plugin.app.rest.fetch_member(context.guild_id, context.user.id)
    memberallroles = membergot.role_ids
    
    # Check to see if user calling this command is the owner of the server.
    if context.author.id == context.get_guild().owner_id:
        return True
    for id in memberallroles:
        if redb.exists(f'admins-{context.guild_id}-{id}'):
            return True
    if redb.exists(f'adminuser-{context.guild_id}-{membergot.id}'):
            return True
    return False

# This is the main slash command group.
@plugin.command
@lightbulb.command("admin", "Group of commands for admins.")
@lightbulb.implements(commands.SlashCommandGroup)
async def admin(context):
    pass

# This slash command sets a level up channel for the server.
@admin.child
@lightbulb.option("channel", "The channel to set as level up channel.", hikari.GuildChannel, required=True)
@lightbulb.command("setlevelupchannel", "Sets the level up channel for the server.", guilds=authed_guilds)
@lightbulb.implements(commands.SlashSubCommand)
async def setlevelupchannel(context: SlashContext):
    # Check to see if user calling this command is the owner of the server.
    if not await isauthorized(context):
        await context.respond("You are not authorized to use this command.")
        await reportaction(context,f'Missing User Permissions', f'User attempted to set the level up channel to "{context.options.channel.name}" ID: {context.options.channel.id}', False, False)
        await asyncio.sleep(5)
        await context.delete_last_response()
        return
    
    # Now we set the level up channel.
    redb.set(f"levelchannel-{context.get_guild().id}", context.options.channel.id)
    await context.respond("Level up channel set.")
    await reportaction(context,f'Changed Level Up Channel", "Admin set the level up channel to "{context.options.channel.name}" ID: {context.options.channel.id}', True, True)
    await asyncio.sleep(5)
    await context.delete_last_response()

# This slash command sets a level up channel for the server.
@admin.child
@lightbulb.option("channel", "The channel to set as the welcome channel.", hikari.GuildChannel, required=True)
@lightbulb.command("setwelcomechannel", "Sets the welcome channel for the server.", guilds=authed_guilds)
@lightbulb.implements(commands.SlashSubCommand)
async def setwelcomechannel(context: SlashContext):
     # Check to see if user calling this command is the owner of the server.
    if not await isauthorized(context):
        await context.respond("You are not authorized to use this command.")
        await reportaction(context,f'Missing User Permissions', f'User attempted to set the welcome channel to "{context.options.channel.name}" ID: {context.options.channel.id}', False, False)
        await asyncio.sleep(5)
        await context.delete_last_response()
        return
    
    # Now we set the level up channel.
    redb.set(f"welcomechannel-{context.get_guild().id}", context.options.channel.id)
    await context.respond("Welcome channel set.")
    await reportaction(context,f'Welcome Channel Set', f'Admin set the level up channel to "{context.options.channel.name}" ID: {context.options.channel.id}', True, True)
    await asyncio.sleep(5)
    await context.delete_last_response()
    
# This slash command sets a level up channel for the server.
@admin.child
@lightbulb.command("removelevelupchannel", "Removes levelup channel.", guilds=authed_guilds)
@lightbulb.implements(commands.SlashSubCommand)
async def removelevelupchannel(context: SlashContext):
    # Check to see if user calling this command is the owner of the server.
    if not await isauthorized(context):
        await context.respond("You are not authorized to use this command.")
        await reportaction(context,f'Missing User Permissions', "User attempted to remove the level up channel.", False, False)
        await asyncio.sleep(5)
        await context.delete_last_response()
        return
    
    # Now we set the level up channel.
    redb.delete(f"levelchannel-{context.get_guild().id}")
    await context.respond("Level up channel removed.")
    await reportaction(context,f'Removed Welcome Channel', "Admin removed the level up channel.", True, True)
    await asyncio.sleep(5)
    await context.delete_last_response()

# This slash command sets a level up channel for the server.
@admin.child
@lightbulb.command("removewelcomechannel", "Removes levelup channel.", guilds=authed_guilds)
@lightbulb.implements(commands.SlashSubCommand)
async def removewelcomechannel(context: SlashContext):
    # Check to see if user calling this command is the owner of the server.
    if not await isauthorized(context):
        await context.respond("You are not authorized to use this command.")
        await reportaction(context,f'Missing User Permissions', "User attempted to remove the welcome channel.", False, False)
        await asyncio.sleep(5)
        await context.delete_last_response()
        return
    
    # Now we set the level up channel.
    redb.delete(f"welcomechannel-{context.get_guild().id}")
    await context.respond("Welcome channel removed.")
    await reportaction(context,f'Removed The Welcome Channel', "Admin removed the welcome channel.", False, False)
    await asyncio.sleep(5)
    await context.delete_last_response()
    
@admin.child
@lightbulb.option("user", "User to count messages from.", hikari.Member, required=True)
@lightbulb.command("countmessages", "counts the messages from a user.", guilds=authed_guilds)
@lightbulb.implements(commands.SlashSubCommand)
async def countmessages(context: SlashContext):
    # Check to see if user calling this command is the owner of the server.
    if not await isauthorized(context):
        await context.respond("You are not authorized to use this command.")
        await reportaction(context,f'Missing User Permissions', f'User asked to collect user data from {context.options.user.mention} (message count of a user) in a channel.', False, False)
        await asyncio.sleep(5)
        await context.delete_last_response()
        return
    
    count = 0
    
    await context.respond("Collecting information...")
    await reportaction(context,f'Message Gathering Started...', f'The bot is beginning to collect information in {context.get_channel().mention} about {context.options.user.mention}', True, True)
    returnchannel = context.bot.cache.get_guild_channel(context.get_channel())
    
    # Now we get the user ID
    user: hikari.Member = context.options.user
    currentchannel = context.get_channel()
    async for msg in plugin.bot.rest.fetch_messages(currentchannel):
        if msg.author.id == user.id:
            count = count + 1
    
    await returnchannel.send(f'The user "{user.username}" has {count} messages in this channel!')
    await reportaction(context,f'Message Gathering Complete.', "See results in the channel.", True, True)
    await context.delete_last_response()
    
# This slash command creates a role for the server.
@admin.child
@lightbulb.option("putabove", "The role to put the new role above. (If not specified, role is at the bottom)", hikari.Role, required=False)
@lightbulb.option("hoist", "Should the role be shown apart?", bool, required=True)
@lightbulb.option("mentionable", "Should you be able to mention this role?", bool, required=True)
@lightbulb.option("color", "Can be almost any color you can name.", hikari.Color, required=True)
@lightbulb.option("name", "The role to create.", str, required=True)
@lightbulb.command("createrole", "Creates a role for the server.", guilds=authed_guilds)
@lightbulb.implements(commands.SlashSubCommand)
async def createrole(context: SlashContext):
    
    
    # Check to see if user calling this command is the owner of the server.
    if not await isauthorized(context):
        await context.respond("You are not authorized to use this command.")
        await reportaction(context,f'Missing User Permissions', f'User attempted to make a role with the name "{context.options.name}"', False, False)
        await asyncio.sleep(5)
        await context.delete_last_response()
        return
    
    # Convert color to hex
    colorhex = colors.to_hex(context.options.color)
    # Now turn this RGB into hikari.Color
    finalcolor = hikari.Color.from_hex_code(colorhex)
    
    # check if the putabove role is not none
    if context.options.putabove is not None:
        # If the role is not none, then we need to get the role ID
        aboverole: hikari.Role = context.options.putabove
        aboverole.position
    
    
    #Now we set the role.
    
    guildid = context.get_guild().id
    
    createdrole = await context.bot.rest.create_role(
        guild=guildid,
        name=context.options.name,
        color=finalcolor,
        hoist=context.options.hoist,
        mentionable=context.options.mentionable
    )
    
    desiredposition = (context.options.putabove.position + 1) if context.options.putabove is not None else 0
    
    # Sorry for shitty code.
    if context.options.putabove is not None:
        allroles = {}
        preview = []
        # Get all of the other roles and put them into a dict
        for roleobj in await context.bot.rest.fetch_roles(guildid):
            if roleobj.id != createdrole.id:
                allroles[roleobj.position] = roleobj.id
            else:
                allroles[desiredposition] = roleobj.id

        
    if context.options.putabove is not None:
        try:
            await context.bot.rest.reposition_roles(guildid,positions=allroles)
            await context.respond("Role created.")
            await reportaction(context,f'Role Created', f'Role: "{context.options.name}" created.', True, True)
            await asyncio.sleep(5)
            await context.delete_last_response()
        except hikari.BadRequestError:
            await context.respond("Role was created, but I can't move the role above the role you requested.")
            await reportaction(context,f'Role Creation Partially Finished', f'Role: "{context.options.name}" created however it was not able to be placed above the role requested.', False, True)
            await asyncio.sleep(10)
            await context.delete_last_response()
    else:        
        await context.respond("Role created.")
        await reportaction(context,f'Role Created', f'Role: "{context.options.name}" created.', True, True)
        await asyncio.sleep(5)
        await context.delete_last_response()
    

# Slash command to delete a role.
@admin.child
@lightbulb.option("role", "The role to delete.", hikari.Role, required=True)
@lightbulb.command("deleterole", "Deletes a role from the server.", guilds=authed_guilds)
@lightbulb.implements(commands.SlashSubCommand)
async def deleterole(context: SlashContext):
    
    # Check to see if user calling this command is the owner of the server.
    if not await isauthorized(context):
        await context.respond("You are not authorized to use this command.")
        await reportaction(context,f'Missing User Permissions', f'User attempted to delete "{context.options.role.name}" role.', False, False)
        await asyncio.sleep(5)
        await context.delete_last_response()
        return
    
    # Don't allow an admin to delete a role through the bot that is an admin role.
    if redb.exists(f'admins-{context.guild_id}-{context.options.role.id}'):
        await context.respond("You cannot remove an administrator role. You must do it manually.")
        await reportaction(context,f'Critical Missing Permission', f'User attempted to delete "{context.options.role.name}" role which is marked as administrator.', False, False)
        await asyncio.sleep(5)
        await context.delete_last_response()
        return
    
    # Delete the role
    try:
        await context.bot.rest.delete_role(context.get_guild().id, context.options.role.id)
    except hikari.ForbiddenError:
        await context.respond("Bot could not complete the request because it does not have permission to delete this role.")
        await reportaction(context, f'Bot Error', f'Admin attempted to delete a role: "{context.options.role.name}" but the bot does not have the permissions to do so.', False, True)
    
    await context.respond("Role deleted.")
    await reportaction(context,f'Role Deleted', f'Admin deleted "{context.options.role.name}" role.', True, True)
    await asyncio.sleep(5)
    await context.delete_last_response()

# This bot purges the channel or ammount of messages specified.
@admin.child
@lightbulb.option("amount", "Amount of messages to remove.", int, required=False)
@lightbulb.command("purge", "Purges the ammount of messages specified. (Max 100)", guilds=authed_guilds)
@lightbulb.implements(commands.SlashSubCommand)
async def purge(context: SlashContext):
    
    # Check to see if user calling this command is the owner of the server.
    if not await isauthorized(context):
        await context.respond("You do not have the power.")
        await reportaction(context,f'Missing User Permissions', f'User attempted to purge {context.get_channel().mention}', False, False)
        await asyncio.sleep(5)
        await context.delete_last_response()
        return
    await context.respond("Purging...")
    await reportaction(context,f'Purge Started...', f'An admin started a purge of {context.get_channel().mention}. This action cannot be stopped, and is processing.', True, True)
    returnchannel = context.bot.cache.get_guild_channel(context.get_channel())
    currentchannel = context.get_channel()
    count = -1
    print(type(context.options.amount))
    print(context.options.amount)
    # If the ammount is not specified, then we delete all messages.
    if context.options.amount is None or context.options.amount == 0:
        await context.bot.rest.delete_messages(context.get_channel(), await plugin.bot.rest.fetch_messages(currentchannel))
        count = count + 1
    else:
        async for msg in plugin.bot.rest.fetch_messages(currentchannel):
            count = count + 1
            await context.bot.rest.delete_message(currentchannel, msg)
            if count == context.options.amount:
                break
        
    await returnchannel.send(f'Deleted {count} messages.')
    await reportaction(context,f'Purge Finished', f'Purge of {context.get_channel().mention} has finished.', True, True)

# Command that sets roles that users can get a certain levels.
@admin.child
@lightbulb.option("level", "The level to set the role for. (Level must be at least 2 for protection.)", int, required=True)
@lightbulb.option("role", "The role to set.", hikari.Role, required=True)
@lightbulb.command("setlevelrole", "Sets a role for a certain level.", guilds=authed_guilds)
@lightbulb.implements(commands.SlashSubCommand)
async def setlevelrole(context: SlashContext):
    # Check to see if user calling this command is the owner of the server.
    if not await isauthorized(context):
        await context.respond("You are not authorized to use this command.")
        await reportaction(context,f'Missing User Permissions', f'User attempted to set a level role.', False, False)
        await asyncio.sleep(5)
        await context.delete_last_response()
        return
    
    # Check to see if user entered a level that at least 2.
    if context.options.level < 2:
        await context.respond("You must enter a level that is at least 2.")
        await asyncio.sleep(5)
        await context.delete_last_response()
        return
    
    # Check if the role is already set for the level.
    if redb.exists(f'levelrole-{context.get_guild().id}-{context.options.level}'):
        await context.respond("This level is already set.")
        return
    else:
        # Run an extended test...
        for key in redb.keys(f'levelrole-{context.get_guild().id}-*'):
            if str(redb.get(key)) == str(context.options.role.id):
                await context.respond("The role selected is already used for another level.")
                return
            
        # Set the role for the level.
        redb.set(f'levelrole-{context.get_guild().id}-{context.options.level}', context.options.role.id)
    
    # Send the message that we set the role. Now look for users that are at that level.
    await context.respond("Level role set. Applying to users that have the level in the background...")
    await reportaction(context,f'Applying Level Role Update...', f'Admin made role: {context.options.role.name} avalible to users at level {context.options.level}. This action is being applied to users in the background.', True, True)
    
    # Look for users.
    async for gotmember in context.bot.rest.fetch_members(context.guild_id):
        
        # If they have a level, we will go through with getting their level, and setting the role for them.
        if redb.exists(f'level:{gotmember.id}:server_id:{context.guild_id}'):
            memberlevel = redb.get(f'level:{gotmember.id}:server_id:{context.guild_id}')
            if int(memberlevel) >= context.options.level:
                # Now we need to check if they have another level role and remove it.
                # Get their ids
                hasids = []
                for hasroles in gotmember.get_roles():
                    hasids.append(hasroles.id)
                
                userlevelhigher = False
                # Key search Redis to see if there are any other previous roles.
                otherroles = redb.keys(f'levelrole-{context.guild_id}-*')
                for rolekey in otherroles:
                    testroleid = int(redb.get(rolekey))
                    if testroleid in hasids:
                        level = int(rolekey.split('-')[2])
                        # If the user's current role is at a higher level. Don't remove.
                        if level > context.options.level:
                            # User's level is higher than that.
                            userlevelhigher = True
                        else:
                            await gotmember.remove_role(testroleid)
                
                # Then apply the new level if the users current role level is higher.
                if not userlevelhigher:
                    await gotmember.add_role(context.options.role)
                else:
                    pass
            else:
                # User level does not meet check.
                pass
        else:
            # User has no level set in DB.
            pass
    
    await reportaction(context,f'Role Change Complete', f'Server Role update complete.', True, True)
    await asyncio.sleep(15)
    await context.delete_last_response()
    
# Command that removes a level role.
@admin.child
@lightbulb.option("role", "The role to set.", hikari.Role, required=True)
@lightbulb.command("removelevelrole", "Sets a role for a certain level.", guilds=authed_guilds)
@lightbulb.implements(commands.SlashSubCommand)
async def removelevelrole(context: SlashContext):
    # Check to see if user calling this command is the owner of the server.
    if not await isauthorized(context):
        await context.respond("You must be the owner of the server to use this command.")
        await reportaction(context,f'Missing User Permissions', f'User attempted to remove a level role.', False, False)
        await asyncio.sleep(5)
        await context.delete_last_response()
        return
    
    dbroles = []
    # Go in Redis and find the role id
    for key in redb.keys(f'levelrole-{context.guild_id}-*'):
        dbroles.append(int(redb.get(key)))
    
    # Check if the role ID is in the dbroles list.
    if context.options.role.id not in dbroles:
        await context.respond("That role wasn't found in the list of levelup roles.")
        await asyncio.sleep(8)
        await context.delete_last_response()
        return
    
    # We found it if we are past this point. So, we will remove the role from the DB now.
    for key in redb.keys(f'levelrole-{context.guild_id}-*'):
        if int(redb.get(key)) == context.options.role.id:
            redb.delete(key)
            break
    
    # Send the message that we set the role. Now look for users that are at that level.
    await context.respond("Level role removed. Applying to users that have the level in the background...")
    await reportaction(context,f'Applying Level Role Update...', f'Admin removed role: {context.options.role.name} from level roles. This action is being applied to users in the background.', True, True)
    
    # Look for users.
    async for gotmember in context.bot.rest.fetch_members(context.guild_id):
        if redb.get(f'level:{gotmember.id}:server_id:{context.guild_id}') is not None:
            memberlevel = int(redb.get(f'level:{gotmember.id}:server_id:{context.guild_id}'))
            # Now we need to check if they have the level role and remove it.
            # Get their ids
            hasids = []
            for hasroles in gotmember.get_roles():
                hasids.append(hasroles.id)
            
            if context.options.role.id in hasids:
                await gotmember.remove_role(context.options.role)
            
            # Check if there was a lower levelup role we can give them.
            levels = []
            for key in redb.keys(f'levelrole-{context.guild_id}-*'):
                levels.append(int(key.split("-")[2]))
            levels.sort(reverse=True)
            
            # Remove levels that are greater than the user's current level
            for index in range(len(levels)):
                if levels[index] > memberlevel:
                    levels.pop(index)
            
            if len(levels) < 1:
                pass
            else:
                # Finally, get the first item in levels.
                roleid = redb.get(f'levelrole-{context.guild_id}-{levels[0]}')
                await gotmember.add_role(roleid)

    await reportaction(context,f'Role Change Complete', f'Server Role update complete.', True, True)
    await asyncio.sleep(15)
    await context.delete_last_response()

# Slash command to allow a role to be recognized as an admin.
@admin.child
@lightbulb.option("role", "Role to allow the using of admin commands.", hikari.Role, required=True)
@lightbulb.command("allowroleforadmin", "Allows a specific role to access admin commands.", guilds=authed_guilds)
@lightbulb.implements(commands.SlashSubCommand)
async def allowroleforadmin(context: SlashContext):
    
    # Check to see if user calling this command is the owner of the server.
    if context.get_guild().owner_id == context.author.id:
        redb.set(f'admins-{context.guild_id}-{context.options.role.id}', f'{context.options.role.id}')
        if context.options.role.is_mentionable:
            await context.respond(f'Set {context.options.role.mention} as authorized admin role.')
            await reportaction(context,f'Set Admin Role', f'The server owner made {context.options.role.mention} an admin role.', True, True)
        else:
            await context.respond(f'Set {context.options.role.name} as authorized admin role.')
            await reportaction(context,f'Set Admin Role', f'The server owner made {context.options.role.name} an admin role.', True, True)
        
    else:
        await reportaction(context,f'Critical Missing Permission', f'A user attempted to set a role as admin.', False, False)
        
    
    await asyncio.sleep(15)
    await context.delete_last_response()
    
# Slash command to allow a role to be recognized as an admin.
@admin.child
@lightbulb.option("role", "Role to allow the using of admin commands.", hikari.Role, required=True)
@lightbulb.command("removeroleforadmin", "Allows a specific role to access admin commands.", guilds=authed_guilds)
@lightbulb.implements(commands.SlashSubCommand)
async def removeroleforadmin(context: SlashContext):
    
    # Check to see if user calling this command is the owner of the server.
    if context.get_guild().owner_id == context.author.id:
        if redb.exists(f'admins-{context.guild_id}-{context.options.role.id}'):
            redb.delete(f'admins-{context.guild_id}-{context.options.role.id}')
            await context.respond("Role has been removed from admin.")
            await reportaction(context,f'Removed Admin Role', f'The server owner removed {context.options.role.name} as an admin role.', True, True)
        else:
            await context.respond("That role was not found to be an admin role.")
        
    else:
        await context.respond("You cannot remove an admin role.")
        await reportaction(context,f'Critical Missing Permission', f'A user attempted to set a role as admin.', False, False)
    
    await asyncio.sleep(15)
    await context.delete_last_response()
    
# Slash command to allow a member to be recognized as an admin.
@admin.child
@lightbulb.option("member", "User to allow the using of admin commands.", hikari.Member, required=True)
@lightbulb.command("adduserforadmin", "Allows a specific role to access admin commands.", guilds=authed_guilds)
@lightbulb.implements(commands.SlashSubCommand)
async def allowuserforadmin(context: SlashContext):
    
    # Check to see if user calling this command is the owner of the server.
    if context.get_guild().owner_id == context.author.id:
        redb.set(f'adminuser-{context.guild_id}-{context.options.member.id}', f'{context.options.member.id}')
        if context.options.role.is_mentionable:
            await context.respond(f'Set {context.options.member.mention} as authorized admin member.')
            await reportaction(context,f'Set User As Admin', f'The server owner made {context.options.member.mention} an admin.', True, True)
    else:
        await context.respond("You don't have the power.")
        await reportaction(context,f'Critical Missing Permission', f'A user attempted to set a role as admin.', False, False)
    
    await asyncio.sleep(15)
    await context.delete_last_response()
        
@admin.child
@lightbulb.option("channel", "Channel to make the work report section.", hikari.GuildChannel, required=True)
@lightbulb.command("setworkchannel", "Sets the bot's work channel for reports.", guilds=authed_guilds)
@lightbulb.implements(commands.SlashSubCommand)
async def setworkchannel(context: SlashContext):
    
    #Check if the user is authorized to use this command.
    if await isauthorized(context):
        redb.set(f'workreportchannel-{context.guild_id}', context.options.channel.id)
        await context.respond("The work channel has been set.")
        await reportaction(context,"Work Channel Set", "Admin set the current work channel", True, True)
    else:
        await context.respond("You are not authroized to use this command.")
        await reportaction(context,"Missing User Permissions", "User attempted to set the current work channel", False, False)
    
    
    await asyncio.sleep(15)
    await context.delete_last_response()

@admin.child
@lightbulb.command("removeworkchannel", "removes the bot's work channel for reports.", guilds=authed_guilds)
@lightbulb.implements(commands.SlashSubCommand)
async def removeworkchannel(context: SlashContext):
    
    #Check if the user is authorized to use this command.
    if await isauthorized(context):
        if redb.exists(f'workreportchannel-{context.guild_id}'):
            redb.delete(f'workreportchannel-{context.guild_id}')
            await context.respond("The work channel has been removed.")
        else:
            await context.respond("A work channel was not set.")
    else:
        await context.respond("You are not authroized to use this command.")
        
    await asyncio.sleep(15)
    await context.delete_last_response()
        