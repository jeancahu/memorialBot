# memorial Bot

from discord import Embed, Member, Intents, utils # Bot TODO
from discord.ext import commands # it's no needed for 1.7.3>

from sys import exit
from time import sleep, time
from random import sample, random
from asyncio import gather

from commands import ping, name

import requests
import pandas as pd

## indirect commands
df = pd.read_csv('textpixoubot.csv', delimiter=';')

## Users list
guild_id = 398770997559296011 # Enterprise
bot_id = 933187664037965834 # MANGER
manger_id = 336571520379781122 # MANGER ID
admin_ids = [
    650633031064879125, # homura
    383805313880424449, # thunder
]

## Decorators
def guild_only(guild_id):
    async def predicate(ctx):
        return ctx.guild and ctx.guild.id == guild_id
    return commands.check(predicate)

def only_for_user(user_id, user_name): # Functions who returns a decorator
    async def predicate(ctx):
        if not ctx.author.id == user_id:
            await ctx.send("Hey you are not {}!".format(user_name))
            return False
        return True
    return commands.check(predicate)

try:
    TOKEN = open("TOKEN").readline().replace('\n','')
except Exception as e:
    print(e)
    exit(1)

if not TOKEN:
    exit(2)

## Global variables
bot = commands.Bot(command_prefix="m>", case_insensitive=True)
bot.remove_command("help")

disable_bot = False

class MemberRoles(commands.MemberConverter):
    async def convert(self, ctx, argument):
        member = await super().convert(ctx, argument)
        return [role.name for role in member.roles[1:]] # Remove everyone role!

@bot.check
async def globally_block_dms(ctx):
    # Block DMs
    return ctx.guild is not None

async def on_ready():
    print("Bot is online")

@guild_only(guild_id) # Works for enterprise server only
async def on_message(message):
    global disable_bot
    if message.author.id == bot_id: # Bot itself
        return

    if disable_bot: # bot is disable
        return

    ## Auto update
    if message.author.id in admin_ids:
        if message.attachments:
            if message.attachments[0].filename == "textpixoubot.csv":
                r = requests.get(message.attachments[0].url)

                ## Add data headers/column names
                file_content = "command;response;\n" + r.content.decode("iso-8859-1")
                open("textpixoubot.csv", 'wb').write(file_content.encode("utf-8"))

                # Update the database
                global df
                df = pd.read_csv('textpixoubot.csv', delimiter=';')

                await message.reply("Done, database is update")
                return

    # sleeps between 2 and 6 seconds
    # TODO Disable responses
    sleep(random()*2 + 1)
    # Enable responses

    responses = df.loc[df['command'] == message.content.lower()]
    if not responses.empty:
        await message.reply(responses["response"].sample(n=1).to_string(index=False))

async def on_reaction_add(reaction, user):
    if user.id == 863062654699438110: # Bot itself
        return
    #print(user.name)
    pass

@bot.command(name="enable", aliases=["en","e"])
async def enable(ctx):
    """
    Enable the bot
    """
    global disable_bot
    if ctx.author.id in admin_ids:
            disable_bot = False
            await ctx.reply("ò_ó ok")

@bot.command(name="disable", aliases=["ds", "d"])
async def disable(ctx):
    """
    Disable de bot
    """
    global disable_bot
    if ctx.author.id in admin_ids:
        disable_bot = True
        await ctx.message.add_reaction("👋")

@bot.command()
async def roles(ctx, *, member: MemberRoles = None):
    """
    Tells you a member's roles.
    * means next arguments will be named args
    """
    if member:
        await ctx.send('I see the following roles: **{}**'.format('**, **'.join(member)))
        return
    await ctx.send('I see the following roles: **{}**'.format('**, **'.join([str(i) for i in ctx.author.roles[1:]]))) # [1:] removes everyone role

@bot.command(name="avatar", aliases=["pp", "pfp"])
async def avatar(ctx, *, member: Member = None):
    """
    Tells you a member's roles.
    * means next arguments will be named args
    """
    if member:
        await ctx.message.reply('{}'.format(member.avatar.url))
        return

    await ctx.message.reply('{}'.format(ctx.author.avatar.url))


@bot.command(name="randreact", aliases=["rreact", "rr"])
async def randreact(ctx):
    """
    React with random guild emojis
    """

    message = await ctx.channel.history(limit=2).flatten()
    message = message[1]
    available_emojis = [i for i in ctx.guild.emojis if i.available]
    random_emojis = sample(available_emojis, 9)

    await gather(*[
            message.add_reaction(emoji) for emoji in random_emojis
        ])
    await ctx.message.delete()

# Command hi
bot.command(name="hi")(name)

# Command Ping
bot.command()(ping)

@bot.command()
async def whoissus(ctx):
    await ctx.send("<@330030494534336512>, he is sus af")

@bot.command()
async def sus(ctx):
    await ctx.send("<@330030494534336512>, he is sus af 🦃")

## Run
bot.add_listener(on_ready)
bot.add_listener(on_message, "on_message")
bot.add_listener(on_reaction_add, "on_reaction_add")
bot.run(TOKEN)
