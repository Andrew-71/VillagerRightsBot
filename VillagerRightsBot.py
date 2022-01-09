from cogs.java_server import JavaServerStats
from cogs.misc import Miscellaneous
from cogs.moderation import Moderation
from cogs.verification import VerificationView, Verification
from cogs.whitelisting import Whitelisting
import nextcord
from nextcord.ext import commands
from pathlib import Path
from toml import load


class VillagerRightsBot(commands.Bot):

    def __init__(self, config: dict):
        self.config = config
        super().__init__(command_prefix="!", intents=nextcord.Intents.all())
        self.current_players: list[tuple[str, int]] = []
        self.persistent_views_added: bool = False

    def load_ids(self):
        global villager_rights
        global verification_channel
        villager_rights = self.get_guild(self.config["IDS"]["GUILD"])
        verification_channel = villager_rights.get_channel(self.config["IDS"]["VERIFICATION_CHANNEL"])

    async def on_ready(self):
        print(nextcord.__version__)
        print("ready")
        self.load_ids()
        if not self.persistent_views_added:
            self.add_view(VerificationView(bot=self))
            self.persistent_views_added = True
        await self.change_presence(
            activity=nextcord.Game(name="Use /whitelist add  to join the Java Server!"),
            status=nextcord.Status.online
        )

    async def on_message(self, message: nextcord.Message):
        if message.author == self.user or message.flags.ephemeral:
            return
        if message.channel == verification_channel:
            await message.delete()

    async def on_member_join(self, member: nextcord.Member):
        if not member.bot:
            await verification_channel.send(content=member.mention, delete_after=0.1)


def main():
    config: dict = load(Path('configs/config.toml'))
    vr_bot = VillagerRightsBot(config=config)
    cogs = [JavaServerStats, Miscellaneous, Moderation, Verification, Whitelisting]
    for cog in cogs:
        vr_bot.add_cog(cog(vr_bot))
    vr_bot.run(config["TOKEN"])


if __name__ == "__main__":
    main()
