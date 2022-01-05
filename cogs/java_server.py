from aiomojang import Player, ApiException
import cogs.whitelisting as w
from dataclasses import dataclass
from datetime import timedelta
from mcstatus import MinecraftServer
import nextcord
from nextcord.ext import tasks, commands
from pathlib import Path
from time import time
from toml import load
from utils.common_embeds import make_error_embed
from utils.json_handling import write_to_json
# This is a FAT module, probably should refactor somehow


@dataclass
class CurrentPlayer:
    username: str
    joined_at: int


CONFIG: dict = load(Path('configs/config.toml'))
JAVA_SERVER: MinecraftServer = MinecraftServer.lookup(f"{CONFIG['HOSTNAME']}:{CONFIG['QUERY_PORT']}")
CURRENT_PLAYERS: list[CurrentPlayer] = []


def make_status_embed(players: list[str]) -> nextcord.Embed:
    if players:  # is not empty
        status_embed = nextcord.Embed(
            title="Server is Online",
            description="Here is a list of online players",
        )
        for player in players:
            for current_player_ in CURRENT_PLAYERS:
                if current_player_.username == player:
                    x = current_player_.joined_at
                    break
            else:
                x = int(time())
                CURRENT_PLAYERS.append(CurrentPlayer(player, x))
            status_embed.add_field(name=player, value=f"since <t:{x}>")

    else:
        status_embed = nextcord.Embed(
            title="Server is Online",
            description="There are no online players",
        )
    return status_embed


# Check if usernames are up to date
async def update_whitelist(players: list[str]):
    for player in players:
        if player in [
            value["username"] for value in w.WHITELIST_DICT.values()
        ]:
            continue
        try:
            user_id = await Player(player).uuid
        except ApiException:
            continue
        for key in w.WHITELIST_DICT:
            if w.WHITELIST_DICT[key]["uuid"] == user_id:
                w.WHITELIST_DICT[key]["username"] = player


def update_stats(players: list[str]):
    for key in w.WHITELIST_DICT:
        if w.WHITELIST_DICT[key]["username"] in players:
            w.WHITELIST_DICT[key]["time_played"] += 15


@tasks.loop(seconds=15.0)
async def check_java(status_channel: nextcord.TextChannel):

    try:
        a = JAVA_SERVER.query()
        b = a.players.names
    except ConnectionResetError:
        status_embed = nextcord.Embed(
            title="Server is Offline",
            colour=nextcord.Colour.red()
        )
    else:
        status_embed = make_status_embed(players=b)
        await update_whitelist(players=b)
        update_stats(players=b)
        write_to_json(w.WHITELIST_DICT, "data/stats.json")
        status_embed.colour = nextcord.Colour.blue()

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
    async def get_java_stats(self, interaction: nextcord.Interaction, user: nextcord.User):
        if (user_id := str(user.id)) not in w.WHITELIST_DICT:
            await interaction.response.send_message(
                embed=make_error_embed("This player is not whitelisted on the Java Server!"),
                ephemeral=True
            )
            return
        user_dict = w.WHITELIST_DICT[user_id]
        await interaction.response.send_message(
            embed=nextcord.Embed(
                title=f"{user_dict['username']}'s Stats",
                colour=nextcord.Colour.gold(),
            ).set_footer(text="Note: the bot only tracks stats since the server has been whitelisted"
                         ).add_field(name="Time played", value=str(timedelta(seconds=user_dict['time_played']))
                                     ).add_field(name="Joined on", value=f"<t:{user_dict['since']}>"),
            ephemeral=True
        )

    @commands.Cog.listener()
    async def on_ready(self):
        status_channel = self.bot.get_channel(CONFIG["IDS"]["STATUS_CHANNEL"])
        check_java.start(status_channel)
