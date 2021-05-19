import discord
from discord.ext import commands
import os
import psycopg2
# import sqlite3

DATABASE_URL = os.environ['DATABASE_URL'] # connect to postgres if online
connection = psycopg2.connect(DATABASE_URL, sslmode='require')
# connection = sqlite3.connect("splat.db")
cursor     = connection.cursor()


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def createmaplistdb(self, ctx):
        # init database
        cursor.execute(''' CREATE TABLE maplists (
            name       text,
            date       text,
            num_rounds text,
            mapstr     text
        )''')
        connection.commit()
        await ctx.send('created maplist db')


    @commands.command()
    async def createmapdb(self, ctx):
        cursor.execute("DROP TABLE IF EXISTS mapmodes")
        cursor.execute(''' CREATE TABLE mapmodes (
            code     text,
            string   text
        )''')
        connection.commit()
        await ctx.send('created mapmodes db')

        with open("mapmodes") as in_file:
            for line in in_file:
                arr  = line.split("=")
                data = (arr[0], str(arr[1]).rstrip("\n"))
                cursor.execute("INSERT INTO mapmodes VALUES (%s, %s)", data)
        connection.commit()
                