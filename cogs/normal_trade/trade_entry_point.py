# from discord.ext import commands
from discord import app_commands, Embed, colour
from discord.ext import commands
import discord
from discord.ui import Button, View
from typing import Optional, Dict, Any, Coroutine, List, Union
from discord import ui
from . import bot_settings
import datetime
from .buy_token import get_token_autopsy
from pprint import pprint


class BuyTokensCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="sell", description="Sell tokens into eth")
    async def sell_tokens(
        self, interactions: discord.Interaction, token_address: str
    ) -> None:
        await interactions.response.send_message("sold")

    @app_commands.command(name="buy", description="Buy tokens with eth")
    async def my_command(
        self, interaction: discord.Interaction, token_address: str
    ) -> None:
        # print(token_address)\n{'Holders':<{inline_gap}}{_token_security.holders}
        _data, _token_security = await get_token_autopsy(
            interaction.user.id, token_address
        )
        inline_gap = 15
        des_gap = 20
        # pprint(_data.__dict__)
        # pprint(_token_security.__dict__)
        embed = Embed(
            title=f"""{'ETH':<{inline_gap}}{_data.dexId:{inline_gap}}\n{'Age':<{inline_gap}}<t:{int(_data.pairCreatedAt/1000)}:R>\n{'price':<{inline_gap}}{_data.priceUsd:<{inline_gap}}\n{'Holders':<{inline_gap}}{_token_security.holder_count}""",
            colour=colour.Color.green(),

            description=f"""{'Fdv':<{des_gap}}**{_data.fdv}**\n{'Liq':<{des_gap}}**{_data.liquidity.usd}**({_data.liquidity.base}{_data.baseToken.symbol}/{_data.liquidity.quote}{_data.quoteToken.symbol})\n{'Vol':<{des_gap}} h1:{_data.volume.h1} 1D:{_data.volume.h24}\n{'buy/sell':<{des_gap}} m5:**({_data.txns['m5'].buys}/{_data.txns['m5'].sells})** h1 ({_data.txns['h1'].buys}/{_data.txns['h1'].sells}) 1d ({_data.txns['h24'].buys}/{_data.txns['h24'].sells})""",
            timestamp=datetime.datetime(year=2023, month=3, day=16, hour=9, minute=8),
        )
        embed.add_field(
            name=f"**{'BUY TAX':<{inline_gap}}{_token_security.buy_tax}\t{'SELL TAX':<{inline_gap}}{_token_security.sell_tax}**",
            value=f"",
            inline=False,
        )
        embed.add_field(name=f"""**{'can buy':<{inline_gap}}{_bool(_token_security.cannot_buy, True)}\t{'can sell all':<{inline_gap}}{_bool(_token_security.cannot_sell_all, True)}**""",value=f"",inline=False)
        embed.add_field(name=f"""**{'dev wallet':<{inline_gap}}{_token_security.creator_balance} ({_token_security.creator_percent:.2f}%)**""",value=f"")
        # embed.add_field(name=f"creator_address {token_data.creator_address}",value=f"cannot_buy {token_data.cannot_sell_all}")
        # embed.add_field(name=f"creator_balance {token_data.creator_balance}",value=f"holder_count {token_data.holder_count}")
        # embed.add_field(name=f"honeypot_with_same_creator {token_data.honeypot_with_same_creator}",value=f"is_airdrop_scam {token_data.is_airdrop_scam}")
        # embed.add_field(name=f"is_anti_whale {token_data.is_anti_whale}",value=f"is_blacklisted {token_data.is_blacklisted}")
        # embed.add_field(name=f"is_honeypot {token_data.is_honeypot}",value=f"is_in_dex {token_data.is_in_dex}")
        # embed.add_field(name=f"is_mintable {token_data.is_mintable}",value=f"is_open_source {token_data.is_open_source}")
        # embed.add_field(name=f"has whitelist {token_data.is_open_source}",value=f"note {token_data.note}")
        # embed.add_field(name=f"lp_holder_count {token_data.lp_holder_count}",value=f"lp_total_supply {token_data.lp_total_supply}")
        # embed.add_field(name=f"other_potential_risks {token_data.other_potential_risks}" , value =f"owner_address {token_data.owner_address}" )
        # embed.add_field(name=f"owner_balance {token_data.owner_balance}" , value =f"anti_whale_modifiable {token_data.anti_whale_modifiable}" )
        # embed.add_field(name=f"slippage_modifiable {token_data.slippage_modifiable}" , value =f"trading_cooldown {token_data.trading_cooldown}" )
        # embed.add_field(name=f"transfer_pausable {token_data.transfer_pausable}" , value =f"(something here later " )
        await interaction.response.send_message(
            f"{_data.baseToken.symbol}/{_data.quoteToken.symbol}", embed=embed
        )
def _bool(_value, _is_negative:bool = False) -> str:
    tick = ':white_check_mark:'
    cross =':x:'
    no_idea=':grey_question:'
    print(_value,type(_value), _is_negative)
    if not _is_negative:
        return tick if _value == '1' else cross if _value == '0' else no_idea 
    return cross if _value == '1' else tick if _value == '0' else no_idea

async def setup(bot):
    await bot.add_cog(BuyTokensCommand(bot))
