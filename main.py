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


cogs = ["cogs.wallet_manager.wallet_manager", "cogs.normal_trade.trade_entry_point"]


class MyBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def setup_hook(self):
        print("Bot is starting")
        for cog in cogs:
            print(cog)
            await bot.load_extension(cog)

    async def on_ready(self):
        print("Bot is ready")


bot = MyBot(command_prefix='/', intents=intents)

@bot.command(name='sync')
async def sync_tree(ctx):
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands: {synced = }")
    except Exception as e:
        print(e)


@bot.command(name='purge')
async def purge(ctx, *limit):
    limit = int(limit[0])
    await ctx.channel.send(limit)
    channel = ctx.channel
    await channel.purge(limit=limit)


bot.run(API)
