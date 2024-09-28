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

class Publish(discord.ui.View):
    @discord.ui.button(label='Publish', style=discord.ButtonStyle.gray)
    async def publish_click_interaction(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.clear_items()  # Remove all elements from the View
        await interaction.response.edit_message(embeds=interaction.message.embeds, content=interaction.message.content, view=self)  # Update the triggering message
        embeds = interaction.message.embeds
        if embeds:
            embeds[0].add_field(name="From", value=interaction.user.mention)
        await interaction.followup.send(embeds=embeds, content=interaction.message.content)  # Send new message

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
async def cmd_info(ctx :commands.Context, mod_id :str, keyword :str, version_filter :str = '%', target_user :discord.Member = None, preview: bool = False):
    msg :str = target_user.mention if target_user is not None else None
    for response in Database.get_info_formatted(modID=mod_id, keyword=keyword, filter=version_filter):
        if not response.description:
            #Catches "This keyword has no associated documentation" messages
            await ctx.send(embed=response, ephemeral=True)
            return
        if preview:
            view = Publish()  # Make a new view (that contains a Publish button)
            await ctx.send(content=msg, embed=response, ephemeral=True, view=view)
        else:
            await ctx.send(content=msg, embed=response)
        msg = None

@client.hybrid_command(name="compat")
async def cmd_compat(ctx :commands.Context, mod_a :str, mod_b :str, version_filter :str = '%', target_user :discord.Member = None, preview: bool = False):
    msg :str = target_user.mention if target_user is not None else None
    for response in Database.get_compat_formatted(mod_a=mod_a,mod_b=mod_b,filter=version_filter):
        if preview:
            view = Publish()  # Make a new view (that contains a Publish button)
            await ctx.send(content=msg, embed=response, ephemeral=True, view=view)
        else:
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

client.run(token)
