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
async def test1(ctx, arg1, arg2):
    await ctx.send('You passed {} and {}'.format(arg1, arg2))

@bot.command()
async def clear(ctx , limit:int = 5):
    await ctx.channel.purge(limit=limit)
    # await ctx.send(f'{limit} messages have been deleted')


@bot.command()
async def helpme(ctx):
    await ctx.send(f"To get mayor stats type ```.mayor stateno districtname municipality```\nTo get political-party stats  type ```.partystats ```")
    # await ctx.send(f'{limit} messages have been deleted')

@bot.command() #command to kick a user from server
@commands.has_permissions(kick_members=True) 
async def kick(ctx, member:discord.Member ,*,reason=None):

    await member.kick(reason=reason)
    await ctx.send(f'{member} has been kicked by {ctx.author}\n Reason:{reason}')


#command to ban a user from server
@bot.command()
@commands.has_permissions(ban_members=True) 
async def ban(ctx, member:discord.Member ,*,reason=None):

    await member.ban(reason=reason)
    await ctx.send(f'{member} has been banned by {ctx.author}\n Reason:{reason}')



@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.event
async def on_member_join(member:discord.Member):
    channel= bot.get_channel(977665855590629376)
    # print(f'{member} joined the server')
    await channel.send(f'{member} joined the server')

@bot.event
async def on_member_remove(member:discord.Member):
    channel= bot.get_channel(977665855590629376)
    # print(f'{member} joined the server')
    await channel.send(f'{member} left the server')

@bot.command()
async def mayor(ctx,state,district,muni):
    data = get_muni_data(state,district,muni)
    print(state,district,muni)
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