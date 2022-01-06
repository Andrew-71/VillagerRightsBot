from aiomojang import Player, ApiException, BadRequestException
import asyncio
from utils.common_embeds import make_error_embed
from functools import wraps
import json
from nextcord import Interaction
from pathlib import Path
from toml import load


CONFIG = load(Path('configs/config.toml'))
SERVER_ADDRESS = (CONFIG["HOSTNAME"], CONFIG["TCP_PORT"])


class UUIDException(Exception):
    pass


class ConnectionException(Exception):

    @staticmethod
    async def run(interaction: Interaction):
        await interaction.response.send_message(
            embed=make_error_embed("There was an error sending the data to the server. "
                                   "Maybe the Java server is offline?"),
            ephemeral=True
        )


def can_specify_member(func):

    @wraps(func)
    async def wrapper(*args, **kwargs):
        if kwargs["member"] and not args[1].user.guild_permissions.manage_roles:
            await args[1].response.send_message(
                embed=make_error_embed("You do not have permissions to manage other members"),
                ephemeral=True
            )
            return
        await func(*args, **kwargs)

    return wrapper


async def read_and_write(json_payload: dict) -> None:
    try:
        reader, writer = await asyncio.open_connection(*SERVER_ADDRESS)
        writer.write(str.encode(json.dumps(json_payload)))
    except Exception:
        # Thanks asyncio for not listing the possible exceptions, so I'll use this instead :)
        raise ConnectionException
    await writer.drain()
    writer.close()


async def get_uuid(user: Player, interaction: Interaction) -> str:
    try:
        user_id = await user.uuid
        if not user_id:
            raise ApiException
        return user_id
    except BadRequestException:
        await interaction.response.send_message(
            embed=make_error_embed("Username not found!"),
            ephemeral=True
        )
        raise UUIDException
    except ApiException:
        await asyncio.sleep(1)
        await interaction.response.send_message(
            embed=make_error_embed("There was an error with the request, please try again"),
            ephemeral=True
        )
        raise UUIDException
