import dis
import os
import discord
import random
from dotenv import load_dotenv
from prettytable import PrettyTable

from scraper import * 

from discord.ext import commands
load_dotenv()


intents = discord.Intents.default() #  what event to receive and what to not ..its confusing but heyyyy 
intents.members=True

bot = commands.Bot(command_prefix='.',intents=intents)

@bot.command()
async def helpme(ctx):
    await ctx.send(f"To get mayor stats type ```.mayor state-no districtname municipality```\nTo get political-party stats  type ```.partystats ```\n Special command for kathmanu (sanghiya rajdhani) ```.kathmandu ```")
    # await ctx.send(f'{limit} messages have been deleted')


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


@bot.command()
async def mayor(ctx,state,district,muni):
    data = get_muni_data(state,district,muni)
    print(state,district,muni)
    t = PrettyTable(['Name', 'Votes'])
    for (name,vote) in data:
        t.add_row([name,vote])
    await ctx.send(t)

@bot.command()  #special command for capital city
async def kathmandu(ctx): 
    data = get_muni_data('3','kathmandu','kathmandu')
    t = PrettyTable(['Name', 'Votes'])
    for (name,vote) in data:
        t.add_row([name,vote])
    await ctx.send(t)


@bot.command()
async def partystats(ctx):
    data = party_data()
    t = PrettyTable(['PartyName', 'Wins','Leads'])
    for (name,win,lead) in data:
        t.add_row([name,win,lead])

    await ctx.send(t)


bot.run(os.getenv('TOKEN'))