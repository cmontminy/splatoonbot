import discord
import os
import random
import pathlib
import sys
import io
import traceback
import sqlite3 # connect, commit
import asyncio
import json
# import psycopg2
from discord.ext   import commands
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option, create_choice

from commands.maps  import Maps
from commands.admin import Admin


# DATABASE_URL = os.environ['DATABASE_URL'] # connect to postgres if online
# connection = psycopg2.connect(DATABASE_URL, sslmode='require')
# cursor = connection.cursor()

connection = sqlite3.connect("splat.db")
cursor     = connection.cursor()


# bot description
command_prefix = '!'
description = "Discord bot to help with Splatoon things"
bot = commands.Bot(command_prefix=command_prefix, description=description,
                   case_insensitive=True)
slash = SlashCommand(bot, sync_commands=True) # Declares slash commands through the client.

# COGS
bot.add_cog(Maps(bot))
bot.add_cog(Admin(bot))

# start up
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

    game = discord.Game("stinky is cute !")
    await bot.change_presence(activity = game)

guild_ids = [670469511572488223, 771226056346042410] # bot testing id, splat server

@slash.slash(name="ping", guild_ids=guild_ids)
async def _ping(ctx): # Defines a new "context" (ctx) command called "ping."
    await ctx.send(f"Pong! ({bot.latency*1000}ms)")

# @slash.slash(name="maplist",
#              description="Commands for maplists from tournaments",
#              options=[
#                create_option(
#                  name="option",
#                  description="Maplist options",
#                  option_type=3,
#                  required=False,
#                  choices=[
#                   create_choice(
#                     name="add",
#                     value="DOGE!"
#                   ),
#                   create_choice(
#                     name="ChoiceTwo",
#                     value="NO DOGE"
#                   )
#                 ]
#                )
#              ], guild_ids=guild_ids)
# async def test(ctx, optone: str):
#     await ctx.respond()
#     await ctx.send(content=f"Wow, you actually chose {optone}? :(")

@bot.command()
async def maplist_add(ctx, tournament, date):
    await ctx.send('maplist time')

    def check(m):
        return ctx.author == m.author
    
    try:
        msg = await bot.wait_for('message', timeout=10.0, check=check)
    except asyncio.TimeoutError:
        return await ctx.send('you took too long sadge')
    else:
        await ctx.send('received list')

    maplist = json.loads(msg.content)
    type = maplist['type']
    # maps = maplist['rounds']
    
    if type == "rounds" or type == "pool":
        data = (tournament.lower(), date, type, str(maplist))
        cursor.execute("INSERT INTO maplists VALUES (?, ?, ?, ?)", data)
        connection.commit()
        await ctx.send(f'Successfully added {tournament} to the map list')
    
    else:
        await ctx.send('you fucked up')


# # test command
# @bot.command()
# async def test(ctx):
#     await ctx.send("hi !")


# bot.run(os.environ.get('TOKEN'))

bot_token = ""
with open("secrets.txt",'r') as fl:
    for line in fl:
        if "TOKEN" in line:
            bot_token = line.split("=")[1]
bot.run(bot_token)   