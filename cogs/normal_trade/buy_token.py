# from discord.ext import commands
from aiohttp import ClientResponse
from discord import app_commands, Embed, colour
from discord.ext import commands
import discord
from dataclasses import dataclass
from discord.ui import Button, View
from typing import Optional, Dict, Any, Coroutine, List, Union, Tuple
from discord import ui
from aiohttp import ClientResponse
from .token_models import (
    TokenInfo,
    TokenModel,
    LiquidityModel,
    PriceChangeModel,
    TxnsModel,
    VolumeModel,
    DexScreenerModel,
)
from . import bot_settings, configs
from pydantic import BaseModel
import aiohttp

from pprint import pprint


async def get_token_autopsy(tg_id: int, token_address: str) -> Tuple[DexScreenerModel, TokenInfo] :
    url = f'{configs["url"]}{configs["endpoint"]["get_token_details"]}'
    data = {"tg_id": tg_id, "token_address": token_address}
    async with aiohttp.ClientSession() as Session:
        async with Session.get(url, json=data) as response:
            print(response.status)
            if response.status == 200:
                return await success_ok(await response.json())


async def success_ok(response: dict) -> Tuple[DexScreenerModel, TokenInfo]:
    token_data: DexScreenerModel = DexScreenerModel.model_validate(
        response["dexscreener_data"]
    )
    security_data: TokenInfo = TokenInfo.model_validate(response["token_security_data"])
    return  token_data, security_data


async def not_success(response: ClientResponse):
    # @TODO handle exceptions later create a new exception class https://discordpy.readthedocs.io/en/latest/ext/commands/commands.html#error-handling
    print(await response.json())

