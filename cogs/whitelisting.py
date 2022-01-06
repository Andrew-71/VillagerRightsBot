from aiomojang import Player
import nextcord
from nextcord.ext import commands
from pathlib import Path
from time import time
from toml import load
from typing import Optional
from utils.common_embeds import make_error_embed, make_success_embed
from utils.json_handling import read_from_json, write_to_json
from utils.whitelist_utils import can_specify_member, read_and_write, get_uuid, UUIDException, ConnectionException

CONFIG = load(Path('configs/config.toml'))
WHITELIST_DICT: dict[str, dict] = read_from_json("data/stats.json")


class Whitelisting(commands.Cog):

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
        name="whitelist",
        description="Whitelist commands for the Java Server",
        guild_ids=[CONFIG["IDS"]["GUILD"]]
    )
    async def whitelist(self):
        pass

    @whitelist.subcommand(
        name="add",
        description="Add yourself to the Java whitelist with your current username"
    )
    @can_specify_member
    async def whitelist_add(self, interaction: nextcord.Interaction, username: str, member: nextcord.Member = nextcord.SlashOption(
        name="member",
        required=False,
        default=None
    )):
        if str(interaction.user.id if not member else member.id) in WHITELIST_DICT.keys():
            await interaction.response.send_message(
                embed=make_error_embed("You are already whitelisted on the server!"),
                ephemeral=True
            )
            return
        try:
            user_id = await get_uuid(user=Player(username), interaction=interaction)
        except UUIDException:
            return
        except ConnectionException:
            await ConnectionException.run(interaction=interaction)
            return

        WHITELIST_DICT[str(interaction.user.id if not member else member.id)] = {
            "uuid": user_id,
            "username": username,
            "since": int(time()),
            "time_played": 0
        }
        write_to_json(WHITELIST_DICT, "data/stats.json")
        await interaction.user.add_roles(self.java_role)
        await interaction.response.send_message(
            embed=make_success_embed("Whitelist add was successful, welcome!"
                                     ).insert_field_at(0, name="UUID", value=user_id
                                                       ).insert_field_at(0, name="Username", value=username),
            ephemeral=True
        )

    @whitelist.subcommand(
        name="remove",
        description="Remove your account from the whitelist"
    )
    @can_specify_member
    async def whitelist_remove(self, interaction: nextcord.Interaction, member: nextcord.Member = nextcord.SlashOption(
        name="member",
        required=False,
        default=None
    )):
        member_id = str(interaction.user.id if not member else member.id)
        try:
            user_dict = WHITELIST_DICT[member_id]
            await read_and_write({"method": 1, "uuid": user_dict['uuid'], "name": user_dict['username']})
        except KeyError:
            await interaction.response.send_message(
                embed=make_error_embed("You are not whitelisted"),
                ephemeral=True
            )
            return
        except ConnectionException:
            await ConnectionException.run(interaction=interaction)
            return

        del WHITELIST_DICT[member_id]
        write_to_json(WHITELIST_DICT, "data/stats.json")
        await interaction.user.remove_roles(self.java_role)
        await interaction.response.send_message(
            embed=make_success_embed("Whitelist removal was successful"),
            ephemeral=True
        )

    @whitelist.subcommand(
        name="edit",
        description="Remove old whitelist and add a new one"
    )
    @can_specify_member
    async def whitelist_edit(self, interaction: nextcord.Interaction, username: str, member: nextcord.Member = nextcord.SlashOption(
        name="member",
        required=False,
        default=None
    )):
        member_id = str(interaction.user.id if not member else member.id)
        try:
            user_dict = WHITELIST_DICT[member_id]
            user_id = await get_uuid(user=Player(username), interaction=interaction)
            await read_and_write({"method": 2,
                                  "uuid": user_dict['uuid'], "name": user_dict['username'],
                                  "new_uuid": user_id, "new_name": username
                                  })
        except KeyError:
            await interaction.response.send_message(
                embed=make_error_embed("You are not whitelisted"),
                ephemeral=True
            )
            return
        except UUIDException:
            return
        except ConnectionException:
            await ConnectionException.run(interaction=interaction)
            return

        WHITELIST_DICT[member_id] = {
            "uuid": user_id,
            "username": username,
            "since": WHITELIST_DICT[member_id]["since"],
            "time_played": WHITELIST_DICT[member_id]["time_played"]
        }
        write_to_json(WHITELIST_DICT, "data/stats.json")
        await interaction.response.send_message(
            embed=make_success_embed("Whitelist edit was successful"
                                     ).insert_field_at(0, name="UUID", value=user_id
                                                       ).insert_field_at(0, name="Username", value=username),
            ephemeral=True
        )
