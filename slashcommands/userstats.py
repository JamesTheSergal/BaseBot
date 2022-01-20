import hikari
from hikari import guilds
import lightbulb
from lightbulb import commands
from lightbulb.app import BotApp
from lightbulb.context.slash import SlashContext

# Import redb from main.py
from __main__ import redb
from __main__ import authed_guilds

# add this for importing this plugin
plugin = lightbulb.Plugin("userstats")

@plugin.command
@lightbulb.command("userstats", "Group of commands to help the user see their stats.", guilds=authed_guilds)
@lightbulb.implements(commands.SlashCommandGroup)
async def userstats(context: SlashContext):
    pass
    
# This plugin gets the users current level, users xp, and the users xp needed to level up.
@userstats.child
@lightbulb.command(name='levelinfo', description='Get your current level, your current XP, and the XP needed to level up.', guilds=authed_guilds)
@lightbulb.implements(commands.SlashSubCommand)
async def levelinfo(context: SlashContext):
    # get the user's ID, server ID, current XP, and level.
    user_id = context.author.id
    server_id = context.get_guild().id
    currxp = redb.get(f'xp:{user_id}:server_id:{server_id}')
    currlevel = redb.get(f'level:{user_id}:server_id:{server_id}')
    
    if currxp is None or currlevel is None:
        await context.respond("You have no XP or level yet! Sorry!")
        return
    
    # get member object
    context_member = context.get_guild().get_member(user_id)
    
    # Make hikari embed showing user stats
    embed = (
        hikari.Embed(
            title=f"Level {currlevel} User",
            color=hikari.Color.from_rgb(186, 21, 232),
        )
        .set_author(name=context.author.username)
        .set_thumbnail(context_member.avatar_url)
        .add_field(name="XP:", value=currxp, inline=True)
        .add_field(name="Messages:", value=redb.get(f'messagecount:{user_id}:server_id:{server_id}'), inline=True)
        .add_field(name="XP to Level:", value=int(currlevel) * int(120 * (1.1 ** int(currlevel)))-int(currxp), inline=True)
    )
    
    # Send the embed to the user.
    await context.respond(embed=embed)
    
@userstats.child
@lightbulb.option("user", "User to count messages from.", hikari.Member)
@lightbulb.command(name="getinfo", description="Gets information about the user.", guilds=authed_guilds)
@lightbulb.implements(commands.SlashSubCommand)
async def getinfo(context: SlashContext):
    checkuser: hikari.Member = context.options.user
    roles = (await checkuser.fetch_roles())[1:]
    
    embed = (
        hikari.Embed(
            title="User Information",
            description=f"{checkuser.username}'s information.",
            colour=hikari.Color.from_rgb(186, 21, 232),
        )
        .set_author(name="Information")
        .set_footer(
            text=f"{checkuser.username}'s ID is {checkuser.id}.\nRequested by {context.author.username}.",
            icon=context.member.avatar_url,
        )
        .set_thumbnail(checkuser.avatar_url)
        .add_field(
            name="Joined Server",
            value=checkuser.joined_at.strftime("%A, %B %d, %Y at %I:%M %p")
            )
        .add_field(
            name="Number of messages seen",
            value=redb.get(f'messagecount:{checkuser.id}:server_id:{context.get_guild().id}')
            )
        .add_field(
            name="User Score",
            value=redb.get(f'xp:{checkuser.id}:server_id:{context.get_guild().id}') if redb.get(f'xp:{checkuser.id}:server_id:{context.get_guild().id}') is not None else "No user score yet."
            )
        .add_field(
            name="No of roles",
            value=len(roles)
            )
        .add_field(
            name="Roles",
            value=", ".join([role.name for role in roles]) if len(roles) > 0 else "No roles"
            )
    )
    
    await context.respond(embed=embed)
