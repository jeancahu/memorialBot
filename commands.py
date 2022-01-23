async def ping(ctx):
    """
    Ping command to verify bot is online
    """
    await ctx.send("pong")

async def name(ctx):
    """
    Reply a mention to the command message author
    """
    await ctx.send("{} hello uwu".format(ctx.author.mention))
