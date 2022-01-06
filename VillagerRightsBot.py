from cogs.java_server import JavaServerStats
from cogs.misc import Miscellaneous
from cogs.moderation import Moderation
from cogs.verification import VerificationView, Verification
from cogs.whitelisting import Whitelisting
import nextcord
from pathlib import Path
from toml import load


class VillagerRightsBot(nextcord.Client):

    def __init__(self, config: dict):
        self.config = config
        super().__init__(intents=nextcord.Intents.all())
        self.current_players: list[tuple[str, int]] = []

    def load_ids(self):
        global villager_rights
        global verification_channel
        villager_rights = self.get_guild(self.config["IDS"]["GUILD"])
        verification_channel = villager_rights.get_channel(self.config["IDS"]["VERIFICATION_CHANNEL"])

    async def check_verification_channel(self):

        history = await verification_channel.history().flatten()
        embed = nextcord.Embed(
                        title="Welcome!",
                        description="Welcome to the official Villager Rights Discord server!\n"
                                    "Please verify yourself by **clicking the button below** and answering the"
                                    " random captcha using **/answer {solution}**\n"
                                    "*This helps with preventing illegitimate accounts from joining our server*"
                    ).set_footer(text="Hint: There are no zeroes in the images")
        view = VerificationView(bot=self)
        for message in history:
            if message.author == self.user:
                await message.edit(embed=embed, view=view)
                break
        else:
            await verification_channel.send(embed=embed, view=view)

    async def on_ready(self):
        print(nextcord.__version__)
        print("ready")
        self.load_ids()
        await self.check_verification_channel()

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
