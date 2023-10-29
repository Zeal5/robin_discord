# This example requires the 'message_content'
import random
import discord
from discord.ext import commands

# from discord import app_commands
from dotenv import load_dotenv
import os
import aiohttp


load_dotenv()
API = os.environ.get("TOKEN")

intents = discord.Intents.default()
intents.message_content = True


bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    try:
        await bot.load_extension("cogs.wallet_manager.wallet_manager")
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands: {synced = }")
    except Exception as e:
        print(e)
    print("Bot is ready")


@bot.command(name='purge')
async def purge(ctx, *limit):
    limit = int(limit[0])
    await ctx.channel.send(limit)
    channel = ctx.channel
    await channel.purge(limit=limit)
    


bot.run(API)
