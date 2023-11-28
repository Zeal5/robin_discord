# from discord.ext import commands
from discord import app_commands, Embed, colour
from discord.ext import commands
import discord
from discord.ui import Button, View
from typing import Optional, Dict, Any, Coroutine, List, Union
from discord import ui
from . import bot_settings
from .buy_token import get_token_autopsy,TokenInfo

# class TradeBotView(View):
#     def __init__(self, bot):
#         super().__init__()
#         self.bot = bot
#
#     @discord.ui.button(label="BUY", style=discord.ButtonStyle.success, row=1)
#     async def buy_tokens(
#         self, interaction: discord.Interaction, button: discord.ui.Button
#     ):
#         await interaction.response.send_message("Enter token address",view=BuyModalView())
#         # await self.bot.wait_for('message',check = lambda m : m.author.id == interaction.user.id and interaction.channel == m.channel)
#         # await interaction.edit_original_response(content= "replied")
#
#
#     @discord.ui.button(label="SELL", style=discord.ButtonStyle.danger, row=1)
#     async def get_wallets(
#         self, interaction: discord.Interaction, button: discord.ui.Button
#     ):
#         await interaction.response.send_message(
#             view= SellModalView())



class BuyTokensCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="sell",description="Sell tokens into eth")
    async def sell_tokens(self, interactions: discord.Interaction, token_address: str) ->None:
        await interactions.response.send_message("sold")

    @app_commands.command(name="buy",description="Buy tokens with eth")
    async def my_command(self, interaction: discord.Interaction, token_address:str) -> None:
        print(token_address)
        token_data:TokenInfo = await get_token_autopsy(interaction.user.id, token_address)
        print(token_data.token_symbol)

        embed = Embed(title="Token Info",colour =colour.Color.green())
        embed.add_field(name=f"{token_data.token_name} ({token_data.token_symbol}) ({token_data.total_supply})",value=f'```{token_address}```')

        embed.add_field(name=f"buy tax {token_data.buy_tax}",value=f"sell_tax {token_data.sell_tax}")
        embed.add_field(name=f"can_take_back_ownership {token_data.can_take_back_ownership}",value=f"cannot_buy {token_data.cannot_buy}")
        embed.add_field(name=f"creator_address {token_data.creator_address}",value=f"cannot_buy {token_data.cannot_sell_all}")
        embed.add_field(name=f"creator_balance {token_data.creator_balance}",value=f"holder_count {token_data.holder_count}")
        embed.add_field(name=f"honeypot_with_same_creator {token_data.honeypot_with_same_creator}",value=f"is_airdrop_scam {token_data.is_airdrop_scam}")
        embed.add_field(name=f"is_anti_whale {token_data.is_anti_whale}",value=f"is_blacklisted {token_data.is_blacklisted}")
        embed.add_field(name=f"is_honeypot {token_data.is_honeypot}",value=f"is_in_dex {token_data.is_in_dex}")
        embed.add_field(name=f"is_mintable {token_data.is_mintable}",value=f"is_open_source {token_data.is_open_source}")
        embed.add_field(name=f"has whitelist {token_data.is_open_source}",value=f"note {token_data.note}")
        embed.add_field(name=f"lp_holder_count {token_data.lp_holder_count}",value=f"lp_total_supply {token_data.lp_total_supply}")
        embed.add_field(name=f"other_potential_risks {token_data.other_potential_risks}" , value =f"owner_address {token_data.owner_address}" )
        embed.add_field(name=f"owner_balance {token_data.owner_balance}" , value =f"anti_whale_modifiable {token_data.anti_whale_modifiable}" )
        embed.add_field(name=f"slippage_modifiable {token_data.slippage_modifiable}" , value =f"trading_cooldown {token_data.trading_cooldown}" )
        embed.add_field(name=f"transfer_pausable {token_data.transfer_pausable}" , value =f"(something here later " )
        await interaction.response.send_message(embed=embed)
        #
        #
        # embed = Embed(
        #     colour = colour.Color.green(),
        #     title="Trade Manager",
        #     description="Buy / Sell Tokens",
        # )
        # await interaction.response.send_message(
        #     embed=embed,
        #     view=TradeBotView(self.bot),
        #     ephemeral=True,
        #     delete_after=float(
        #         bot_settings.get("timeout", "original_message", fallback=240)
        #     ),
        # )


async def setup(bot):
    await bot.add_cog(BuyTokensCommand(bot))
