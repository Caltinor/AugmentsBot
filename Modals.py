import discord.ui
import Database
import traceback
import GitHub

class CompatModal(discord.ui.Modal, title='Compat Information Entry Form'):
    mod_a = discord.ui.TextInput(
        label="Mod ID for the base mod",
        style=discord.TextStyle.short,
        placeholder='forge',
        required=True
    )

    mod_b = discord.ui.TextInput(
        label="Mod ID for the (in)compatible mod",
        style=discord.TextStyle.short,
        placeholder='jei',
        required=True
    )

    version = discord.ui.TextInput(
        label="Version of base mod",
        style=discord.TextStyle.short,
        placeholder='1.19',
        required=True
    )

    feedback = discord.ui.TextInput(
        label='Describe the incompatibility.',
        style=discord.TextStyle.long,
        placeholder='Type here...',
        required=True,
        max_length=2000
    )

    async def on_submit(self, interaction: discord.Interaction, /) -> None:
        Database.set_compat(self.mod_a.value, self.mod_b.value, self.version.value, self.feedback.value)
        await interaction.response.send_message('Compat Information Submitted')

    async def on_error(self, interaction: discord.Interaction, error: Exception, /) -> None:
        await interaction.response.send_message('Error with Compat Modal.', ephemeral=True)
        traceback.print_tb(error.__traceback__)

class InfoModal(discord.ui.Modal, title='Info Entry Form'):
    mod_id = discord.ui.TextInput(
        label="Mod ID for this keyword",
        style=discord.TextStyle.short,
        placeholder='forge',
        required=True
    )

    keyword = discord.ui.TextInput(
        label="keyword associated with the info",
        style=discord.TextStyle.short,
        placeholder='forge',
        required=True
    )

    version = discord.ui.TextInput(
        label="mod version this applies to",
        style=discord.TextStyle.short,
        placeholder='forge',
        required=True
    )

    feedback = discord.ui.TextInput(
        label='Message to display',
        style=discord.TextStyle.long,
        placeholder='Type here...',
        required=True,
        max_length=2000
    )

    img = discord.ui.TextInput(
        label="image to embed",
        style=discord.TextStyle.short,
        required=False
    )

    async def on_submit(self, interaction :discord.Interaction, /) -> None:
        Database.set_info(self.mod_id.value, self.keyword.value, self.version.value, self.feedback.value, self.img.value)
        await interaction.response.send_message('Information Added/Updated')
    
    async def on_error(self, interaction: discord.Interaction, error: Exception, /) -> None:
        await interaction.response.send_message('Error with Info Modal.', ephemeral=True)
        traceback.print_tb(error.__traceback__)

class IssueModal(discord.ui.Modal, title='Issue Submission'):
    issueLine = discord.ui.TextInput(
        label="Issue Title",
        style=discord.TextStyle.short,
        placeholder='I Found a Bug',
        required=True
    )

    observation = discord.ui.TextInput(
        label='What is actually happening?',
        style=discord.TextStyle.long,
        placeholder='Type here...',
        required=True,
        max_length=2000
    )

    expectation = discord.ui.TextInput(
        label='What do you expect to happen?',
        style=discord.TextStyle.long,
        placeholder='Type here...',
        required=True,
        max_length=2000
    )

    versions = discord.ui.TextInput(
        label='Forge and Mod version used',
        style=discord.TextStyle.short,
        placeholder='Forge:43.1.0, pmmo:1.19-2.1.1',
        required=True,
        max_length=2000
    )

    other = discord.ui.TextInput(
        label='Other Relevant Information',
        style=discord.TextStyle.long,
        placeholder='Type here...',
        required=False,
        max_length=2000
    )

    def __init__(self, *, projectID :str) -> None:
        super().__init__()
        self.projectID = projectID

    async def on_submit(self, interaction :discord.Interaction, /) -> None:
        bodyFinal = "**Observed Behavior:** \n" + self.observation.value + \
            "\n\n**Expected Behavior:**\n" + self.expectation.value + \
            "\n\nVersions: "+ self.versions.value + \
            "\n\n**Other Information:**\n"+ self.other.value + \
            "\n\n Submitted by: " + interaction.user.name + "#" + interaction.user.discriminator
        GitHub.createIssue(self.projectID, self.issueLine.value, bodyFinal)
        await interaction.response.send_message('Issue Submitted.', ephemeral=True)
    
    async def on_error(self, interaction: discord.Interaction, error: Exception, /) -> None:
        await interaction.response.send_message('Error with Issue Modal.', ephemeral=True)
        traceback.print_tb(error.__traceback__)