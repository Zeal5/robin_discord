# from discord.ext import commands
from discord import app_commands, Embed, colour
from discord.ext import commands
import discord
from discord.ui import Button, View
from typing import Optional, Dict, Any, Coroutine, List, Union
from discord import ui
from . import bot_settings
from .buy_with_eth_views import BuyModalView 
from .sell_with_eth_views import SellModalView 

class TradeBotView(View):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    @discord.ui.button(label="BUY", style=discord.ButtonStyle.success, row=1)
    async def buy_tokens(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.response.send_message(
            view= BuyModalView())


    @discord.ui.button(label="SELL", style=discord.ButtonStyle.danger, row=1)
    async def get_wallets(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.response.send_message(
            view= SellModalView())
        


class BuyTokensCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="trade")
    async def my_command(self, interaction: discord.Interaction) -> None:
        """Buy or Sell tokens with/into ETH"""

        embed = Embed(
            colour = colour.Color.green(),
            title="Trade Manager",
            description="Buy / Sell Tokens",
        )
        await interaction.response.send_message(
            embed=embed,
            view=TradeBotView(self.bot),
            ephemeral=True,
            delete_after=float(
                bot_settings.get("timeout", "original_message", fallback=240)
            ),
        )


async def setup(bot):
    await bot.add_cog(BuyTokensCommand(bot))
