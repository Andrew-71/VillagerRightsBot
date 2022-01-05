from functools import wraps
from nextcord import Interaction, Permissions, TextChannel, Embed, Colour
from nextcord.ext import commands


def has_permissions(**perms):

    invalid = set(perms) - set(Permissions.VALID_FLAGS)
    if invalid:
        raise TypeError(f"Invalid permission(s): {', '.join(invalid)}")

    def decorator(func):

        @wraps(func)
        async def wrapper(*args, **kwargs):

            interaction: Interaction = args[int(isinstance(args[0], commands.Cog))]
            ch: TextChannel = interaction.channel  # type: ignore
            permissions = ch.permissions_for(interaction.user)
            missing = [perm for perm, value in perms.items() if getattr(permissions, perm) != value]

            if missing:
                nl = '\n'
                await interaction.response.send_message(
                    embed=Embed(
                        title="Missing Permissions!",
                        description=f"You are missing the following permissions:\n{nl.join(missing)}",
                        colour=Colour.red()
                    ),
                    ephemeral=True
                )
                raise commands.errors.MissingPermissions(missing)

            result = await func(*args, **kwargs)
            return result

        return wrapper

    return decorator
