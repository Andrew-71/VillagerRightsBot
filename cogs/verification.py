from asyncio import sleep
from claptcha import Claptcha
from dataclasses import dataclass
import nextcord
from nextcord.ext import commands
from pathlib import Path
from random import randint
from toml import load
from utils.common_embeds import make_error_embed, make_success_embed
from utils.slash_commands import has_permissions


CONFIG = load(Path('configs/config.toml'))
GUILD_ID = CONFIG["IDS"]["GUILD"]
ACTIVIST_ROLE_ID = CONFIG["IDS"]["ACTIVIST_ROLE"]
MOD_LOG_ID = CONFIG["IDS"]["MOD_LOG"]


def generate_image():

    image_string = ""
    chars = "abcdefghijklmnopqrstuvwxyz123456789"
    for _ in range(6):
        index = randint(0, 34)
        image_string += chars[index]

    c = Claptcha(image_string, "FreeMono.ttf")

    text, file = c.write('verification_image.png')

    return text, file


@dataclass
class VerificationConversation:
    partner: nextcord.Member
    solution: str


conversations: list[VerificationConversation] = []


class VerificationView(nextcord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    @nextcord.ui.button(label="Verify here!", style=nextcord.ButtonStyle.green, custom_id="villagerrightsbot:verify")
    async def verify(self, _, interaction: nextcord.Interaction):
        async with interaction.channel.typing():
            solution, file = generate_image()
            with open(file, "rb") as image:
                fp = nextcord.File(image)  # type: ignore
                ch: nextcord.TextChannel = self.bot.get_channel(MOD_LOG_ID)
                msg = await ch.send(content=f"{interaction.user.mention} "
                                            f"received the captcha below with solution: {solution}",
                                    file=fp
                                    )
                await sleep(1)
                await interaction.response.send_message(embed=nextcord.Embed().set_image(url=msg.attachments[0].url),
                                                        ephemeral=True)

        conversation = VerificationConversation(interaction.user, solution)
        conversations.append(conversation)


class Verification(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="answer", description="Enter your solution for the last captcha", guild_ids=[GUILD_ID])
    async def answer(self, interaction: nextcord.Interaction, solution: str = nextcord.SlashOption(
        description="Solution for the captcha",
        required=True
    )):
        for conversation in conversations:
            if conversation.partner == interaction.user:
                if solution == conversation.solution:
                    embed = make_success_embed(
                        "You should now have access to the whole server!\nWelcome and have fun!"
                    )
                    await interaction.user.add_roles(interaction.guild.get_role(ACTIVIST_ROLE_ID))
                else:
                    embed = nextcord.Embed(
                        title="Wrong",
                        description="You did not pass the captcha, please dismiss this message"
                                    " then hit the button again",
                        colour=nextcord.Colour.red()
                    )
                conversations.remove(conversation)
                break
        else:
            embed = make_error_embed(
                "Did you already click the button?\n"
                "If you did, then there was an error with the bot, "
                "please dismiss this message then hit the button again."
            ).set_footer(text="Sorry about that, if this keeps occurring please DM the owner")

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @nextcord.slash_command(
        name="verication_message",
        description="Temporary command for owner only",
        guild_ids=[GUILD_ID]
    )
    @has_permissions(manage_guild=True)
    async def verification_message(self, interaction: nextcord.Interaction):
        await interaction.response.send_message(
            embed=nextcord.Embed(
                title="Welcome!",
                description="Welcome to the official Villager Rights Discord server!\n"
                            "Please verify yourself by **clicking the button below** "
                            "and answering the random captcha using **/answer {solution}**"
                            "*This helps with preventing illegitimate accounts from joining our server*"
            ).set_footer(text="Hint: There are no zeroes in the images"),
            view=VerificationView(bot=self.bot)
        )

