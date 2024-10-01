import discord

class Publish(discord.ui.View):
    @discord.ui.button(label='Publish', style=discord.ButtonStyle.gray)
    async def publish_click_interaction(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.clear_items()  # Remove all elements from the View
        await interaction.response.edit_message(embeds=interaction.message.embeds, content=interaction.message.content, view=self)  # Update the triggering message
        embeds = interaction.message.embeds
        if embeds:
            embeds[0].add_field(name="From", value=interaction.user.mention)
        await interaction.followup.send(embeds=embeds, content=interaction.message.content)  # Send new message