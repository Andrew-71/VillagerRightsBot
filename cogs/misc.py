import nextcord
from nextcord.ext import commands, tasks
from pathlib import Path
from random import randint
from toml import load
from typing import Optional

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
        self.colour_role: Optional[nextcord.Role] = None

    @commands.Cog.listener()
    async def on_ready(self):
        villager_rights: nextcord.Guild = self.bot.get_guild(CONFIG["IDS"]["GUILD"])
        self.colour_role = villager_rights.get_role(CONFIG["IDS"]["COLOUR_ROLE"])

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

    @tasks.loop(seconds=20)
    async def update_colour_role(self):
        rgb_tuple = (randint(0, 255) for _ in range(3))
        await self.colour_role.edit(colour=nextcord.Colour.from_rgb(*rgb_tuple))

    @update_colour_role.after_loop
    async def on_update_colour_role_cancel(self):
        self.update_colour_role.start()
