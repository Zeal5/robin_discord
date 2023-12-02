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
        des_gap = 10
        _space = 14
        print(_data.priceUsd)
        embed = Embed(
            title=f"""{'ETH':<{inline_gap}}{_data.dexId:{inline_gap}}\n{'Age':<{inline_gap}}<t:{int(_data.pairCreatedAt/1000)}:R>\n{'price':<{inline_gap}}${_data.priceUsd}\n{'Holders':<{inline_gap}}{_token_security.holder_count}""",
            colour=colour.Color.green(),
            description=f"""```{'Supply':<{des_gap}}{_is_int(_token_security.total_supply)}\n{'Fdv':<{des_gap}}${_is_int(_data.fdv)}\n{'Liq':<{des_gap}}${_is_int(_data.liquidity.usd)}({_is_int(_data.liquidity.base)}{_data.baseToken.symbol}/{_is_int(_data.liquidity.quote)}{_data.quoteToken.symbol})\n{'Vol':<{des_gap}}h1:{_data.volume.h1} 1d:{_data.volume.h24}\n{'buy/sell':<{des_gap}}m5({_data.txns['m5'].buys}/{_data.txns['m5'].sells}) h1({_data.txns['h1'].buys}/{_data.txns['h1'].sells}) 1d({_data.txns['h24'].buys}/{_data.txns['h24'].sells})```""",
        )
        embed.add_field(
            name=f"`{'BUY TAX':<{_space}}{_token_security.buy_tax}`", value=f""
        )
        embed.add_field(
            name=f"`{'SELL TAX':<{_space}}{_token_security.sell_tax}`", value=f""
        )
        embed.add_field(
            name=f"`{'Lp holders':<{_space}}{_is_int(_token_security.lp_holder_count)}`",
            value="",
        )
        embed.add_field(
            name=f"`{'can buy':<{_space}}`{_bool(_token_security.cannot_buy, True)}",
            value=f"",
        )
        embed.add_field(
            name=f"`{'can sell all':<{_space}}`{_bool(_token_security.cannot_sell_all, True)}",
            value=f"",
        )
        embed.add_field(
            name=f"`{'airdrop scam':<{_space}}`{_bool(_token_security.is_airdrop_scam)}",
            value="",
        )
        embed.add_field(
            name=f"`{'honeypot':<{_space}}`{_bool(_token_security.is_honeypot)}",
            value="",
        )
        embed.add_field(
            name=f"`{'Fame/trust':<{_space}}`{_bool(_token_security.trust_list)}",
            value="",
        )

        embed.add_field(
            name=f"`{'mintable':<{_space}}`{_bool(_token_security.is_mintable)}",
            value="",
        )
        embed.add_field(
            name=f"`{'txn cooldown':<{_space}}`{_bool(_token_security.trading_cooldown)}",
            value="",
        )

        # values that can only be known if contract is open source
        embed.add_field(
            name=f"`{'verified':<{_space}}`{_bool(_token_security.is_open_source)}",
            value="",
        )
        if _token_security.is_open_source:
            embed.add_field(
                name=f"`{'anti whale':<{_space}}`{_bool(_token_security.is_anti_whale)} ",
                value=f"",
            )
            embed.add_field(
                name=f"`{'has whitelist':<{_space}}`{_bool(_token_security.is_whitelisted)}",
                value="",
            )
            embed.add_field(
                name=f"`{'has blacklist':<{_space}}`{_bool(_token_security.is_blacklisted)}",
                value="",
            )
            embed.add_field(
                name=f"`{'tax modifiable':<{_space}}`{_bool(_token_security.slippage_modifiable)}",
                value="",
            )
            embed.add_field(
                name=f"`{'proxy':<{_space}}`{_bool(_token_security.is_proxy)}", value=""
            )
            embed.add_field(
                name=f"`{'txns pauseable':<{_space}}`{_bool(_token_security.transfer_pausable)}",
                value="",
            )
            embed.add_field(
                name=f"`{'hidden owner':<{_space}}`{_bool(_token_security.hidden_owner)}",
                value="",
            )
            embed.add_field(
            name=f"`{'change balances':<{_space}}`{_bool(_token_security.owner_change_balance)}",
            value="",
        )
            embed.add_field(
                name=f"`{'retake ownership':<{_space}}`{_bool(_token_security.can_take_back_ownership)}",
                value="",
            )

        # embed.add_field(
        #     name=f"`{'true token':<{_space}}`{_bool(_token_security.is_true_token)}",
        #     value="",
        # )
        # # Inline embeds
        embed.add_field(
            name=f"`{'Previous Rugs by dev':>{_space}}`{_bool(_token_security.honeypot_with_same_creator)}",
            value="",
            inline=False,
        )
        embed.add_field(
            name=f"`{'Creator Balance ':<{_space}}{_token_security.creator_balance} ({_token_security.creator_percent:.2f}%)`",
            value=f"```{_token_security.creator_address}```",
            inline=False,
        )
        # owner/creator balances
        if _token_security.is_open_source:
            if _token_security.owner_address != _token_security.creator_address:
                embed.add_field(
                    name=f"`{'Owner Balance':<{_space}}{_token_security.owner_balance} ({_token_security.owner_percent:.2f}%)`",
                    value=f"```{_token_security.owner_address}```",
                    inline=False,
                )

        print(type(_token_security.note), _token_security.note)
        if _token_security.note is not None:
            embed.set_footer(text=_token_security.note)
        await interaction.response.send_message(
            f"{_data.baseToken.symbol}/{_data.quoteToken.symbol} `{_data.baseToken.address}`",
            embed=embed,
        )


def _is_int(_value: Optional[int]) -> Optional[str]:
    if isinstance(_value, (int, float)):
        return f"{_value:,}"
    return _value


def _bool(_value, _is_negative: bool = False) -> str:
    tick = ":white_check_mark:"
    cross = ":x:"
    no_idea = ":grey_question:"
    print(_value, type(_value), _is_negative)
    if _value is None:
        return no_idea
    if not _is_negative:
        return tick if _value else cross
    return cross if _value else tick


async def setup(bot):
    await bot.add_cog(BuyTokensCommand(bot))
