import nextcord
from nextcord.ext import commands


class DeclarationURL(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(nextcord.ui.Button(
            label="Declaration!",
            url="https://www.reddit.com/r/villagerrights/comments/ipvejn/the_official_declaration_on_the_rights_of_the/"
                                         )
                      )


class Miscellaneous(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(description="Declaration on the Rights of the Villager")
    async def declaration(self, interaction: nextcord.Interaction):
        await interaction.response.send_message(
            content="_ _",
            view=DeclarationURL()
        )
