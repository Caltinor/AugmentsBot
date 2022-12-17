import discord
from discord.ext import commands
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
async def cmd_info(ctx :commands.Context, mod_id :str, keyword :str, version_filter :str = '%'):
    for response in Database.get_info_formatted(modID=mod_id, keyword=keyword, filter=version_filter):
        await ctx.send(embed=response)

@client.hybrid_command(name="compat")
async def cmd_compat(ctx :commands.Context, mod_a :str, mod_b :str, version_filter :str = '%'):
    for response in Database.get_compat_formatted(mod_a=mod_a,mod_b=mod_b,filter=version_filter):
        await ctx.send(embed=response)

@client.hybrid_command(name='add_info')
@commands.has_guild_permissions(manage_messages=True)
async def cmd_add_info(ctx :commands.Context):
    await ctx.interaction.response.send_modal(Modals.InfoModal())

@client.hybrid_command(name="add_compat")
@commands.has_guild_permissions(manage_messages=True)
async def cmd_add_compat(ctx :commands.Context):
    await ctx.interaction.response.send_modal(Modals.CompatModal())

client.run(token)