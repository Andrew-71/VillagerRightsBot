from aiomojang import Player, ApiException
import cogs.whitelisting as w
from dataclasses import dataclass
import nextcord
from time import time


@dataclass
class CurrentPlayer:
    username: str
    joined_at: int


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
