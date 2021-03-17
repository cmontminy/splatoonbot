import discord
from discord.ext import commands
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

from commands.maps  import Maps
from commands.admin import Admin


DATABASE_URL = os.environ['DATABASE_URL'] # connect to postgres if online
connection = psycopg2.connect(DATABASE_URL, sslmode='require')
cursor = connection.cursor()

# # SQLITE CONNECTION
# connection = sqlite3.connect("splat.db")
# cursor     = connection.cursor()


# bot description
command_prefix = '!'
description = "Discord bot to help with Splatoon things"
bot = commands.Bot(command_prefix=command_prefix, description=description,
                   case_insensitive=True)

# COGS
bot.add_cog(Maps(bot))
bot.add_cog(Admin(bot))

# start up
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

    game = discord.Game("stinky is cute !")
    await bot.change_presence(activity = game)


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
        data = (tournament, date, type, str(maplist))
        cursor.execute("INSERT OR IGNORE INTO maplists VALUES (?, ?, ?, ?)", data)
        connection.commit()
        await ctx.send(f'Successfully added {tournament} to the map list')
    
    else:
        await ctx.send('you fucked up')


# test command
@bot.command()
async def test(ctx):
    await ctx.send("hi !")


bot.run(os.environ.get('TOKEN'))