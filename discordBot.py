# bot.py
import os
import numpy
import pandas as pd
import discord
import io
import aiohttp
from dotenv import load_dotenv
from yfina import StockGraph , getCurrentStockData
from datetime import datetime
today = datetime.today().strftime('%Y-%m-%d')


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
client = discord.Client()

@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds,name=GUILD)
    print(f'{client.user} is connected to the following servers:\n')
    print(f'{guild.name}(id: {guild.id})')

# Implement Function Calls on Triggers
@client.event
async def on_message(message):
  # Prevent Bot from looping into itself
    if message.author == client.user:
        return
  # Trigger when bot reads ! message
    if message.content[0] == '!':
        Stock_ticker = message.content[1:len(message.content)]
        #Output chart to graph folder
        StockGraph(Stock_ticker)
        Stock_response = getCurrentStockData(Stock_ticker)
        image_path = 'Graphs\{}.png'.format(Stock_ticker)
        await message.channel.send(f'{Stock_response}',file=discord.File(image_path))
    elif message.content == 'raise-exception':
        raise discord.DiscordException

client.run(TOKEN)
