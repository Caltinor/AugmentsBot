import discord
from discord.ext import commands
import os
import Database
import Modals

tokenFile = open("token.txt", 'r')
token = tokenFile.readline()
tokenFile.close()

intents = discord.Intents.default()
intents.message_content = True
intents.typing = True
intents.messages = True

client = commands.Bot(command_prefix='/', intents=intents)

@client.event
async def on_ready():
    await client.tree.sync()
    print(f'Logged on as {client.user}!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    #The eventual purpose of this listener will be to capture certain
    #key words and respond to them.  I will probably want a separate
    #table to handle this particular interaction.
    #print(f'Message from {message.author}: {message.content}')

@client.hybrid_command(name="info")
async def cmd_info(ctx :commands.Context, mod_id :str, keyword :str, version_filter :str = '%', target_user :discord.Member = None):
    msg :str = target_user.mention if target_user is not None else None
    for response in Database.get_info_formatted(modID=mod_id, keyword=keyword, filter=version_filter):
        if not response.description:
            #Catches "This keyword has no associated documentation" messages
            await ctx.send(embed=response, ephemeral=True)
            return
        await ctx.send(content=msg, embed=response)
        msg = None

@client.hybrid_command(name="compat")
async def cmd_compat(ctx :commands.Context, mod_a :str, mod_b :str, version_filter :str = '%', target_user :discord.Member = None):
    msg :str = target_user.mention if target_user is not None else None
    for response in Database.get_compat_formatted(mod_a=mod_a,mod_b=mod_b,filter=version_filter):
        await ctx.send(content=msg, embed=response)
        msg = None

@client.hybrid_command(name='add_info')
@commands.has_guild_permissions(manage_messages=True)
async def cmd_add_info(ctx :commands.Context):
    await ctx.interaction.response.send_modal(Modals.InfoModal())

@client.hybrid_command(name="add_compat")
@commands.has_guild_permissions(manage_messages=True)
async def cmd_add_compat(ctx :commands.Context):
    await ctx.interaction.response.send_modal(Modals.CompatModal())

@client.hybrid_command(name="bug_report")
async def cmd_issue(ctx :commands.Context, mod_id :str):
    if not os.path.exists("ghtoken.txt"):
        return await ctx.interaction.response.send_message("This mod is not configured for bug reporting", ephemeral=True)

    switch={
        "pmmo":"Project-MMO-2.0",
        "bot": "AugmentsBot"
    }
    projectID = switch.get(mod_id, None)

    await (ctx.interaction.response.send_modal(Modals.IssueModal(projectID=projectID)) \
        if projectID != None \
        else ctx.interaction.response.send_message("This mod is not configured for bug reporting", ephemeral=True))

@client.hybrid_command(name="info_keywords")
async def cmd_list(ctx :commands.Context, mod_id :str, filter :str = "%"):
    await ctx.interaction.response.send_message(Database.list_info(mod_id, filter), ephemeral=True)

@client.hybrid_command(name="compat_keywords")
async def cmd_list(ctx :commands.Context, mod_id :str, filter :str = "%"):
    await ctx.interaction.response.send_message(Database.list_compat(mod_id, filter), ephemeral=True)

@client.event
async def on_raw_reaction_add(msg) -> None:  # Using "raw" so that if the bot gets restarted, older messages can be removed.
    assert msg  # Aborts for days...
    assert msg.emoji.is_unicode_emoji()
    assert msg.emoji.name == "🚫"
    channel = await get_channel_from_id(msg.channel_id)
    member = await get_member_from_id(msg.user_id, channel.guild)
    assert member is not None 
    assert channel is not None
    message = await channel.fetch_message(msg.message_id)
    assert message is not None
    if not valid_message_deletion(message, member):
        return
    await message.delete()
    
async def get_member_from_id(user_id, guild: discord.Guild):  # Attempts to use cache, but will make an API call if that fails.
    member = guild.get_member(user_id)
    return member if member is not None else await guild.fetch_member(user_id)

async def get_channel_from_id(channel_id):  # Attempts to use cache, but will make an API call if that fails.
    channel = client.get_channel(channel_id)
    return channel if channel is not None else await client.fetch_channel(channel_id)

def valid_message_deletion(message: discord.Message, member: discord.Member):  # Validates if a member has permission to delete the message.
    if message.channel.permissions_for(member).manage_messages:  # Does the member have "manage messages" permission.
        return True
    if hasattr(message, "interaction_metadata") and message.interaction_metadata.user.id == member.id:  # Did the member trigger the command.
        return True
    return False

client.run(token)
