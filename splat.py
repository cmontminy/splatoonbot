import discord
import os
import random
import pathlib
import sys
import io
import traceback
# import sqlite3 # connect, commit
import asyncio
import json
import psycopg2
from discord.ext   import commands
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option, create_choice

from commands.maps  import Maps
from commands.admin import Admin


DATABASE_URL = os.environ['DATABASE_URL'] # connect to postgres if online
connection = psycopg2.connect(DATABASE_URL, sslmode='require')
# connection = sqlite3.connect("splat.db")
cursor     = connection.cursor()

maps = {}


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

    with open("maps") as infile:
        for line in infile:
            data = line.split("=")
            maps[data[0]] = data[1]

guild_ids = [670469511572488223, 771226056346042410] # bot testing id, splat server

@slash.slash(name="ping", guild_ids=guild_ids)
async def _ping(ctx): # Defines a new "context" (ctx) command called "ping."
    await ctx.send(f"Pong! ({bot.latency*1000}ms)")

@slash.slash(name="callouts", 
             description="Pulls pictures of callouts or rainmaker paths",
             options=[
               create_option(
                 name="rm",
                 description="Pulls rainmaker path instead of callout image",
                 option_type=5,
                 required=False
               )
             ],
             guild_ids=guild_ids)
async def _callouts(ctx, rm: bool, map: str):
    if len(map) == 2:
        map = maps[map].lower().rstrip()
        print(map)
        if map is None:
            return await ctx.send(f"I don't know the map code {map} !")
    if rm:
        path = f'rm/{map}.png'
    else:
        path = f'callouts/{map}.png'
    if os.path.exists(path):
        await ctx.send(file=discord.File(path))
    else:
        await ctx.send(f"I couldn't find the picture for {map} sadge")


bot.run(os.environ.get('TOKEN'))

# bot_token = ""
# with open("secrets.txt",'r') as fl:
#     for line in fl:
#         if "TOKEN" in line:
#             bot_token = line.split("=")[1]
# bot.run(bot_token)   