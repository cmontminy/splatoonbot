import discord
from discord.ext import commands
import os
import psycopg2


DATABASE_URL = os.environ['DATABASE_URL'] # connect to postgres if online
connection = psycopg2.connect(DATABASE_URL, sslmode='require')
cursor = connection.cursor()


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