import nextcord
from nextcord.ext import commands
from pathlib import Path
from utils.slash_commands import has_permissions
from toml import load
from typing import Optional

CONFIG = load(Path('configs/config.toml'))
GUILD_ID = CONFIG["IDS"]["GUILD"]


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = CONFIG

    @nextcord.slash_command(description="Moderation commands", guild_ids=[GUILD_ID])
    async def moderation(self):
        pass

    @moderation.subcommand(name="ban_list", description="Lists all banned users")
    @has_permissions(ban_members=True)
    async def banned_users(self, interaction: nextcord.Interaction, hidden: bool = nextcord.SlashOption(
        description="Whether the message should only be visible to you",
        required=False,
        default=True
    )):
        ban_list: list[tuple[Optional[str], nextcord.Member]] = await interaction.guild.bans()
        if not ban_list:
            banned_user_embed = nextcord.Embed(
                title='Banned Users:',
                description='There are no banned users!',
                colour=nextcord.Colour.blue()
            )

        else:

            banned_user_embed = nextcord.Embed(
                title='Banned Users:',
                description='Here is a list of banned users',
                colour=nextcord.Colour.blue()
            )
            for banned_user in ban_list:
                banned_user_embed.add_field(
                    name=f'{banned_user[1].name}#{banned_user[1].discriminator}',
                    value=f'Reason: {banned_user[0]}'
                )

            banned_user_embed.set_footer(
                text='use /unban <name#discriminator> to unban a user'
            )

        await interaction.response.send_message(embed=banned_user_embed, ephemeral=hidden)

    @moderation.subcommand(name="ban", description="Send user to the shadow realm")
    @has_permissions(ban_members=True)
    async def ban(self, interaction: nextcord.Interaction, member: nextcord.Member, reason: str = nextcord.SlashOption(
        description="Give a detailed reason for banning",
        required=False,
        default=None
    )):
        await member.ban(reason=reason)
        await interaction.response.send_message(
            f"Banned {member.mention}"
            if not reason else
            f'Banned {member.mention}: {reason}',
            ephemeral=True
        )

    @moderation.subcommand(name="unban", description="Nobody ever uses this command :(")
    @has_permissions(ban_members=True)
    async def unban(self, interaction: nextcord.Interaction, member: nextcord.Member, reason: str = nextcord.SlashOption(
        description="Give a detailed reason for banning",
        required=False,
        default=None
    )):
        ban_list = await interaction.guild.bans()
        for banned_user in ban_list:
            if member == f"{banned_user[1].name}#{banned_user[1].discriminator}":
                await interaction.guild.unban(banned_user[1])
                await interaction.response.send_message(
                    f"Unbanned [{member.mention}] from your server with reason: {reason}",
                    ephemeral=True
                )
                break
        else:
            await interaction.response.send_message(
                f"No user {member} found in banned users list!",
                ephemeral=True
            )
