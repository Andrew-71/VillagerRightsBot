import nextcord


def make_error_embed(description: str) -> nextcord.Embed:
    return nextcord.Embed(
        title="ERROR",
        description=description,
        colour=nextcord.Colour.red()
    )


def make_success_embed(description: str) -> nextcord.Embed:
    return nextcord.Embed(
        title="SUCCESS",
        description=description,
        colour=nextcord.Colour.green()
    )
