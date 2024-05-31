from nextcord import Embed, Forbidden, Color


red = Color.from_rgb(255, 0, 0)
green = Color.from_rgb(0, 255, 0)
blue = Color.from_rgb(0, 0, 255)
yellow = Color.from_rgb(255, 255, 0)
transparent = Color.from_rgb(43, 45, 49)


async def embed_generate(title, description, emoji):
    embed_generate = Embed(color=green)
    embed_generate.set_author(name=f"{emoji} {title}")
    embed_generate.description = description
    return embed_generate


async def embed_success(title, description, id, bot, emoji="✅", content=None, guild=True):
    try:
        embed_data = await embed_generate(title, description, emoji)

        if guild:
            sending = await bot.fetch_channel(id)
        else:
            sending = await bot.fetch_user(id)

        await sending.send(content=content, embed=embed_data)

        return True
    
    except Forbidden:
        return False


async def embed_error(title, description, id, bot, emoji="❌", content=None, guild=True):
    try:
        embed_data = await embed_generate(title, description, emoji)

        if guild:
            sending = await bot.fetch_channel(id)
        else:
            sending = await bot.fetch_user(id)

        await sending.send(content=content, embed=embed_data)

        return True
    except Forbidden:
        return False
