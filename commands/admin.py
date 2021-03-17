import discord
from discord.ext import commands

import sqlite3 # connect, commit

connection = sqlite3.connect("splat.db")
cursor     = connection.cursor()

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    @commands.command()
    async def createmaplistdb(self, ctx):
        # init database
        cursor.execute(''' CREATE TABLE maplists (
            name    text,
            date    text,
            type    text,
            maps    text
        )''')
        connection.commit()
        await ctx.send('created maplist db')