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
from discord.ext import commands
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option, create_choice

from commands.maps import Maps
from commands.admin import Admin


DATABASE_URL = os.environ['DATABASE_URL']  # connect to postgres if online
connection = psycopg2.connect(DATABASE_URL, sslmode='require')
# connection = sqlite3.connect("splat.db")
cursor = connection.cursor()

maps = {}


# bot description
command_prefix = '!'
description = "Discord bot to help with Splatoon things"
bot = commands.Bot(command_prefix=command_prefix, description=description,
                   case_insensitive=True)
# Declares slash commands through the client.
slash = SlashCommand(bot, sync_commands=True)

# COGS
bot.add_cog(Maps(bot))
bot.add_cog(Admin(bot))

# start up


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

    game = discord.Game("stinky is cute !")
    await bot.change_presence(activity=game)

    with open("maps") as infile:
        for line in infile:
            data = line.split("=")
            maps[data[0]] = data[1]

# bot testing id, splat server
guild_ids = [670469511572488223, 771226056346042410]


@slash.slash(name="ping", guild_ids=guild_ids)
async def _ping(ctx):  # Defines a new "context" (ctx) command called "ping."
    await ctx.send(f"Pong! ({bot.latency*1000}ms)")


@slash.slash(name="callouts",
             description="Pulls pictures of callouts or rainmaker paths",
             options=[
                 create_option(
                     name="map",
                     description="Name or short code of the map",
                     option_type=3,
                     required=True
                 ),
                 create_option(
                     name="rm",
                     description="True = displays rm path for the map",
                     option_type=5,
                     required=False
                 )
             ],
             guild_ids=guild_ids)
async def _callouts(ctx, map: str, rm: bool = False):
    if len(map) == 2:
        map = maps[map].lower().rstrip()
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

@slash.slash(name="help", guild_ids=guild_ids)
async def _help(ctx):
    embed = discord.Embed(title="Lil Judd's Commands", description="Lil Judd is a slash command bot ! This means that all of these commands are accessed by typing '/' at the beginning of a Discord message instead of using usual prefixes.", color=0x00b3ff)
    embed.add_field(name="/maplist add", value="Adds a new maplist to Lil Judd's database. The mapstr is a code built up of short codes for map mode combos visible in the command /maplist codes. Codes separated by commas will be interpreted to be in separate rounds. For example: szgacbkd,tcmmrmpp corresponds to Round 1 having Splat Zones Goby Arena and Clam Blitz Kelp Dome and Round 2 having Tower Control Manta Marina and Rainmaker Piranha Pit", inline=False)
    embed.add_field(name="/maplist codes", value="Displays a list of short codes mentioned above", inline=False)
    embed.add_field(name="/maplist get", value="Displays a maplist for the given tournament name", inline=False)
    embed.add_field(name="/maplist maps", value="Displays the current maplists stored in Lil Judd's database", inline=False)
    embed.add_field(name="/callouts", value="Sends the image with annotated callouts corresponding to the given map. If the optional argument rm is set to True, the rainmaker path for the given map will be sent instead", inline=False)
    embed.set_footer(text="Ask Cake if you have any questions ! <3")
    await ctx.send(embed=embed)

bot.run(os.environ.get('TOKEN'))

# bot_token = ""
# with open("secrets.txt",'r') as fl:
#     for line in fl:
#         if "TOKEN" in line:
#             bot_token = line.split("=")[1]
# bot.run(bot_token)
