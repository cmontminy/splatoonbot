import json
import discord
import asyncio
import os
import psycopg2
# import sqlite3

from discord.ext   import commands
from discord_slash import cog_ext, SlashContext, SlashCommand
from discord_slash.utils.manage_commands import create_option, create_choice

DATABASE_URL = os.environ['DATABASE_URL'] # connect to postgres if online
connection = psycopg2.connect(DATABASE_URL, sslmode='require')
# connection = sqlite3.connect("splat.db")
cursor     = connection.cursor()

guild_ids = [670469511572488223, 771226056346042410] # bot testing id, splat server

class Maps(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # slash = SlashCommand(self.bot, sync_commands=True)

   
    @commands.command()
    async def maptest(self, ctx):
        await ctx.send('Hello from map file!')

    @cog_ext.cog_slash(name="mapping", guild_ids=guild_ids)
    async def _mapping(self, ctx): # Defines a new "context" (ctx) command called "ping."
        await ctx.send(f"map Pong! ({self.bot.latency*1000}ms)")


    @cog_ext.cog_subcommand(base="maplist", name="get", guild_ids=guild_ids)
    async def maplist_get(self, ctx, tournament: str):
        def get_mapstr(code):
            cursor.execute("SELECT string FROM mapmodes WHERE code=?", (code,))
            data = cursor.fetchone()
            return data[0]
        
        tournament = tournament.lower()
        cursor.execute("SELECT name, date, num_rounds, mapstr FROM maplists WHERE name=?", (tournament,))
        data = cursor.fetchone()

        if data is None:
            return await ctx.send(f"{tournament} doesn't exist !")

        name, date, num_rounds, mapstr = data

        embed = discord.Embed(title=tournament, description=f"{date}")
        index = 1
        for round in mapstr.split(","):
            value_str = ""
            for char in range(0, len(round), 4):
                code = mapstr[char:char+4]
                string = get_mapstr(code)
                value_str += f"{string}\n"
            embed.add_field(name=f"Round {index}", value=value_str, inline=False)
            index += 1

        await ctx.send(embed=embed)


    @cog_ext.cog_subcommand(base="maplist", name="maps", guild_ids=guild_ids)
    async def maplist_maps(self, ctx):
        cursor.execute("SELECT name, date FROM maplists")
        data = cursor.fetchall()

        embed = discord.Embed(title="Stored Maplists")
        
        value_str = ""
        for tournament in data:
            value_str += f"{tournament[0]} - {tournament[1]}\n"
        embed.add_field(name="Page 1", value=value_str, inline=False)
        
        await ctx.send(embed=embed)


    @cog_ext.cog_subcommand(base="maplist", name="add",
             description="Command to add maplists from tournaments",
             options=[
               create_option(
                 name="name",
                 description="Tournament name",
                 option_type=3,
                 required=True
               ),
               create_option(
                 name="date",
                 description="Tournament date [YYYY-MM-DD]",
                 option_type=3,
                 required=True
               ),
               create_option(
                 name="num_rounds",
                 description="Number of rounds in tournament [1 if pool]",
                 option_type=4,
                 required=True,
               ),
               create_option(
                 name="mapstr",
                 description="String to input maps. Use commas to separate rounds. (ex: szagtcmmcbpp,szag...",
                 option_type=3,
                 required=True
               ),
             ], guild_ids=guild_ids)
    async def maplist_add(self, ctx, name: str, date: str, num_rounds: int, mapstr: str):
        data = (name.lower(), date, num_rounds, mapstr)
        cursor.execute("INSERT INTO maplists VALUES (?, ?, ?, ?)", data)
        connection.commit()
        await ctx.send(f'Successfully added {name} to the map list')
    

    @cog_ext.cog_subcommand(base="maplist", name="codes", guild_ids=guild_ids)
    async def maplist_codes(self, ctx):
        embed = discord.Embed(title="Maplist Codes")
        embed.add_field(name="Modes", value="SZ = Splat Zones\nTC = Tower Control\nRM = Rainmaker\nCB = Clam Blitz\nTW = Turf War", inline=False)
        value_str = "ag = Ancho-V Games\nam = Arowana Mall\nbs = Blackbelly Skatepark\nct = Camp Triggerfish\nga = Goby Arena\nhp = Humpback Pump Track\nia = Inkblot Art Academy\nkd = Kelp Dome\nmk = MakoMart\nmm = Manta Maria\nmt = Moray Towers\nmf = Musselforge Fitness\nah = New Albacore Hotel\npp = Piranha Pit\npm = Port Mackerel\nsi = Shellendorf Institute\nsp = Skipper Pavilion\nsc = Snapper Canal\nsm = Starfish Mainstage\nss = Sturgeon Shipyard\ntr = The Reef\nwh = Wahoo World\nww = Walleye Warehouse\n"
        embed.add_field(name="Maps", value=value_str, inline=False)
        await ctx.send(embed=embed)

    # @commands.command()
    # async def maplist_list(self, ctx):
    #     cursor.execute("SELECT name, date FROM maplists")
    #     data = cursor.fetchall()

    #     embed = discord.Embed(title="Stored Maplists")
        
    #     value_str = ""
    #     for tournament in data:
    #         value_str += f"{tournament[0]} - {tournament[1]}\n"
    #     embed.add_field(name="Page 1", value=value_str, inline=False)
        
    #     await ctx.send(embed=embed)