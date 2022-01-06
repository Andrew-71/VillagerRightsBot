import nextcord
from nextcord.ext import commands
from pathlib import Path
from toml import load
from typing import Optional
from utils.slash_commands import has_permissions

CONFIG = load(Path("configs/config.toml"))


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
        self.activist_role: Optional[nextcord.Role] = None
        self.java_role: Optional[nextcord.Role] = None

    @commands.Cog.listener()
    async def on_ready(self):
        guild = self.bot.get_guild(CONFIG["IDS"]["GUILD"])
        self.activist_role = guild.get_role(CONFIG["IDS"]["ACTIVIST_ROLE"])
        self.java_role = guild.get_role(CONFIG["IDS"]["JAVA_ROLE"])

    @nextcord.slash_command(
        name="declaration",
        description="Declaration on the Rights of the Villager",
        guild_ids=[CONFIG["IDS"]["GUILD"]]
    )
    async def declaration(self, interaction: nextcord.Interaction):
        await interaction.response.send_message(
            content="_ _",
            view=DeclarationURL()
        )

    @nextcord.slash_command(
        name="add_activist_role",
        description="Add the activist role for all allowed users",
        guild_ids=[CONFIG["IDS"]["GUILD"]]
    )
    @has_permissions(manage_guild=True)
    async def add_activist_role(self, interaction: nextcord.Interaction):
        for member in interaction.guild.members:
            if not member.bot:
                await member.add_roles(self.activist_role)

        await interaction.response.send_message("success", ephemeral=True)

    @nextcord.slash_command(
        name="remove_java_role",
        description="Remove java server role from all players",
        guild_ids=[CONFIG["IDS"]["GUILD"]]
    )
    @has_permissions(manage_guild=True)
    async def remove_java_role(self, interaction: nextcord.Interaction):
        for member in interaction.guild.members:
            if not member.bot and self.java_role in member.roles:
                await member.remove_roles(self.java_role)

        await interaction.response.send_message("success", ephemeral=True)
