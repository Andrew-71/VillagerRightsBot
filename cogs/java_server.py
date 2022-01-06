import cogs.whitelisting as w
from datetime import timedelta, datetime
from mcstatus import MinecraftServer
import nextcord
from nextcord.ext import tasks, commands
from pathlib import Path
from toml import load
from typing import Union
from utils.common_embeds import make_error_embed
from utils.java_stats_utils import make_status_embed, update_stats, update_whitelist
from utils.json_handling import write_to_json


CONFIG: dict = load(Path('configs/config.toml'))
JAVA_SERVER: MinecraftServer = MinecraftServer.lookup(f"{CONFIG['HOSTNAME']}:{CONFIG['QUERY_PORT']}")


@tasks.loop(seconds=15.0)
async def check_java(status_channel: nextcord.TextChannel):

    try:
        query_response = JAVA_SERVER.query()
        player_names = query_response.players.names
    except ConnectionResetError:
        status_embed = nextcord.Embed(
            title="Server is Offline",
            colour=nextcord.Colour.red()
        )
    else:
        status_embed = make_status_embed(players=player_names)
        await update_whitelist(players=player_names)
        update_stats(players=player_names)
        write_to_json(w.WHITELIST_DICT, "data/stats.json")
        status_embed.colour = nextcord.Colour.blue()

    # Since we often edit the message, this helps players know the relevance of info
    status_embed.timestamp = datetime.now()

    # Try to edit old message. If there isn't one, send new message.
    history = await status_channel.history().flatten()
    if history:
        await history[0].edit(embed=status_embed)
    else:
        await status_channel.send(embed=status_embed)


class JavaServerStats(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @nextcord.user_command(
        name="Java Server Stats",
        guild_ids=[CONFIG["IDS"]["GUILD"]]
    )
    async def java_user_stats(self, interaction: nextcord.Interaction, user: nextcord.User):
        await self.get_java_stats(interaction, user)

    @nextcord.slash_command(
        name="stats",
        description="Gets a user's stats for the Java Server",
        guild_ids=[CONFIG["IDS"]["GUILD"]]
    )
    async def java_slash_stats(self, interaction: nextcord.Interaction, member: nextcord.Member):
        await self.get_java_stats(interaction, member)

    async def get_java_stats(self, interaction: nextcord.Interaction, user: Union[nextcord.User, nextcord.Member]):
        if (user_id := str(user.id)) not in w.WHITELIST_DICT:
            await interaction.response.send_message(
                embed=make_error_embed("This player is not whitelisted on the Java Server!"),
                ephemeral=True
            )
            return
        user_dict = w.WHITELIST_DICT[user_id]
        player_stats_embed = nextcord.Embed(
                title=f"{user_dict['username']}'s Stats",
                colour=nextcord.Colour.gold(),
            ).set_footer(text="Note: the bot only tracks stats since the server has been whitelisted"
                         ).add_field(name="Time played", value=str(timedelta(seconds=user_dict['time_played']))
                                     ).add_field(name="Joined on", value=f"<t:{user_dict['since']}>")
        # Shows player skin's head.
        player_stats_embed.set_thumbnail(url=f"https://crafatar.com/avatars/{user_dict['uuid']}")

        await interaction.response.send_message(
            embed=player_stats_embed,
            ephemeral=True
        )

    @commands.Cog.listener()
    async def on_ready(self):
        status_channel = self.bot.get_channel(CONFIG["IDS"]["STATUS_CHANNEL"])
        check_java.start(status_channel)
