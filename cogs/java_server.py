import cogs.whitelisting as w
from datetime import timedelta, datetime
from itertools import islice
from mcstatus import MinecraftServer
import nextcord
from nextcord.ext import tasks, commands
from pathlib import Path
from toml import load
from typing import Union, MutableMapping, Any
from utils.common_embeds import make_error_embed
from utils.java_stats_utils import make_status_embed, update_stats, update_whitelist
from utils.json_handling import write_to_json


CONFIG: MutableMapping[str, Any] = load(Path('configs/config.toml'))
JAVA_SERVER: MinecraftServer = MinecraftServer.lookup(f"{CONFIG['HOSTNAME']}:{CONFIG['QUERY_PORT']}")


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

    @nextcord.slash_command(
        name="leaderboard",
        description="Top 10 java players by time online",
        guild_ids=[CONFIG["IDS"]["GUILD"]]
    )
    async def java_leaderboard(self, interaction: nextcord.Interaction):
        leaderboard_embed = nextcord.Embed(title='Leaderboard', description='Ranked by time played',
                                           colour=nextcord.Colour.dark_blue())

        # Create dictionary of players and their time played on the server.
        player_times = {
            player_dict['username']: player_dict['time_played']
            for player_dict in w.WHITELIST_DICT.values()
        }

        sorted_player_times = dict(sorted(player_times.items(), key=lambda item: item[1], reverse=True))
        # We only display top 10 to not make the embed overly long.
        for i, user in enumerate(islice(sorted_player_times.items(), 10)):
            leaderboard_embed.add_field(name=f'{i + 1}. {user[0]}',
                                        value=str(timedelta(seconds=user[1])))

        # If user is a player and is outside the top 10 we add them at the bottom with their rank.
        member_id = str(interaction.user.id)
        try:
            user_dict = w.WHITELIST_DICT[member_id]
            rank = list(sorted_player_times).index(user_dict["username"])
            if rank > 9:
                leaderboard_embed.add_field(
                    name=f'...\n{rank + 1}. {user_dict["username"]}',
                    value=str(timedelta(seconds=user_dict['time_played'])),
                )

        except KeyError:
            pass

        await interaction.response.send_message(embed=leaderboard_embed, ephemeral=True)  # Send the leaderboard

    @tasks.loop(seconds=15.0)
    async def check_java(self, status_channel: nextcord.TextChannel):

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
        try:
            # Try to edit old message. If there isn't one, send new message.
            history = await status_channel.history().flatten()
            if history:
                await history[0].edit(embed=status_embed)
            else:
                await status_channel.send(embed=status_embed)
        except nextcord.DiscordException:
            pass

    @check_java.after_loop
    async def on_check_java_cancel(self):
        status_channel = self.bot.get_channel(CONFIG["IDS"]["STATUS_CHANNEL"])
        self.check_java.start(status_channel)

    @commands.Cog.listener()
    async def on_ready(self):
        status_channel = self.bot.get_channel(CONFIG["IDS"]["STATUS_CHANNEL"])
        self.check_java.start(status_channel)
