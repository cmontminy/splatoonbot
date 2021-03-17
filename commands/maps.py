import json
import discord
import asyncio
from discord.ext import commands

import sqlite3 # connect, commit

connection = sqlite3.connect("splat.db")
cursor     = connection.cursor()

bot = commands.Bot(command_prefix='!')

class Maps(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

   
    @commands.command()
    async def maptest(self, ctx):
        await ctx.send('Hello from map file!')

    
    @commands.command()
    async def maplist_fetch(self, ctx, tournament):
        await ctx.send(f'searching for {tournament}...')

        cursor.execute("SELECT name, date, type, maps FROM maplists WHERE name=?", (tournament,))
        data = cursor.fetchone()

        if data is None:
            return await ctx.send(f"{tournament} doesn't exist tt")

        name, date, type, maps = data
        maps = json.loads(maps.replace("\'", "\""))
        
        embed = discord.Embed(title=tournament, description=f"{type} - {date}")
        
        index = 1
        for round in maps['rounds']:
            value_str = ""
            for match in round:
                value_str += f"{match['mode']} - {match['map']}\n"
            embed.add_field(name=f"Round {index}", value=value_str, inline=False)
            index += 1

        await ctx.send(embed=embed)
    
    
    @commands.command()
    async def maplist_list(self, ctx):
        cursor.execute("SELECT name, date FROM maplists")
        data = cursor.fetchall()

        embed = discord.Embed(title="Stored Maplists")
        
        value_str = ""
        for tournament in data:
            value_str += f"{tournament[0]} - {tournament[1]}\n"
        embed.add_field(name="haha", value=value_str, inline=False)
        
        await ctx.send(embed=embed)