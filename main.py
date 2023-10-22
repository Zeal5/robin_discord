# This example requires the 'message_content'
import random
import discord
from discord.ext import commands
# from discord import app_commands
from dotenv import load_dotenv
import os

load_dotenv()
API = os.environ.get("TOKEN")

intents = discord.Intents.default()
intents.message_content = True


bot = commands.Bot(command_prefix='/', intents=intents)


@bot.event
async def on_ready():
    print("Bot is ready")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands: {synced = }")
    except Exception as e:
        print(e)


@bot.tree.command(name="flip")
async def hello(interaction: discord.Interaction):
    res = random.randint(0, 6)
    embedVar = discord.Embed(
            title="Dice Bot", description="Rolls a dice ", color=0x336EFF
        )
    embedVar.add_field(name="Dice Roller", value=f"{interaction.user}", inline=False)
    embedVar.add_field(name="Odds", value="1 / 6", inline=False)
    embedVar.add_field(name="Result", value=f"{res}")
    await interaction.response.send_message(embed=embedVar)


bot.run(API)
