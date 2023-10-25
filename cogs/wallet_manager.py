import discord
from discord.ext import commands


intents = discord.Intents.default()
intents.message_content = True


bot = commands.Bot(command_prefix='/', intents=intents)


@bot.tree.command(name="flip")
async def flip(interaction: discord.Interaction):
    embedVar = discord.Embed(
            title="Title", description="Desc", color=0x336EFF
        )
    embedVar.add_field(name="Field1", value="hi", inline=False)
    await message.channel.send(embed=embedVar)
