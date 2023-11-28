# from discord.ext import commands
from aiohttp import ClientResponse
from discord import app_commands, Embed, colour
from discord.ext import commands
import discord
from dataclasses import dataclass
from discord.ui import Button, View
from typing import Optional, Dict, Any, Coroutine, List, Union
from discord import ui
from aiohttp import ClientResponse

from . import bot_settings,configs
from pydantic import BaseModel
import aiohttp
import json


class TokenInfo(BaseModel):
    anti_whale_modifiable: Optional[str]
    buy_tax: Optional[str]
    can_take_back_ownership: Optional[str]
    cannot_buy: Optional[str]
    cannot_sell_all: Optional[str]
    creator_address: Optional[str]
    creator_balance: Optional[str]
    creator_percent: Optional[str]
    dex: Optional[List[Dict]]
    external_call: Optional[str]
    hidden_owner: Optional[str]
    holder_count: Optional[str]
    holders: Optional[List[Dict]]
    honeypot_with_same_creator: Optional[str]
    is_airdrop_scam: Optional[str]
    is_anti_whale: Optional[str]
    is_blacklisted: Optional[str]
    is_honeypot: Optional[str]
    is_in_dex: Optional[str]
    is_mintable: Optional[str]
    is_open_source: Optional[str]
    is_proxy: Optional[str]
    is_true_token: Optional[str]
    is_whitelisted: Optional[str]
    lp_holder_count: Optional[str]
    lp_holders: Optional[List[Dict]]
    lp_total_supply: Optional[str]
    note: Optional[str]
    other_potential_risks: Optional[str]
    owner_address: Optional[str]
    owner_balance: Optional[str]
    owner_change_balance: Optional[str]
    owner_percent: Optional[str]
    personal_slippage_modifiable: Optional[str]
    selfdestruct: Optional[str]
    sell_tax: Optional[str]
    slippage_modifiable: Optional[str]
    token_name: Optional[str]
    token_symbol: Optional[str]
    total_supply: Optional[str]
    trading_cooldown: Optional[str]
    transfer_pausable: Optional[str]
    trust_list: Optional[str]
    error: Optional[str] = None

async def get_token_autopsy(tg_id:int, token_address:str):
    url = f'{configs["url"]}{configs["endpoint"]["get_token_details"]}'
    data = {"tg_id": tg_id, "token_address" : token_address}
    async with aiohttp.ClientSession() as Session:
        async with Session.get(url, json=data) as response:
            print(response.status)
            if response.status == 200:
                return await success_ok(await response.json())
            return await not_success(response)



async def success_ok(response:dict):
    return TokenInfo(**response)


async def not_success(response : ClientResponse):
    return response

"""
{
  "code": 1,
  "message": "OK",
  "result": {
    "0xd7e1055aa8ca4bc723788c5e69e38d27b90c5097": {
      "anti_whale_modifiable": "0",
      "buy_tax": "0.05",
      "can_take_back_ownership": "0",
      "cannot_buy": "0",
      "cannot_sell_all": "0",
      "creator_address": "0x1088e4d83f6483530f99807896c909aaf564908c",
      "creator_balance": "0",
      "creator_percent": "0.000000",
      "external_call": "0",
      "hidden_owner": "0",
      "holder_count": "3",
      "holders": [
        {
          "address": "0x663a5c229c09b049e36dcc11a9b0d4a8eb9db214",
          "tag": "UniCrypt",
          "is_contract": 1,
          "balance": "3661.661917763572010459",
          "percent": "0.989999999999999999",
          "is_locked": 1,
          "locked_detail": [
            {
              "amount": "3661.661917763572010459",
              "end_time": "2024-11-01T05:00:00+00:00",
              "opt_time": "2023-11-24T18:19:59+00:00"
            }
          ]
        },
        {
          "address": "0x04bda42de3bc32abb00df46004204424d4cf8287",
          "tag": "",
          "is_contract": 0,
          "balance": "36.986484017813858691",
          "percent": "0.009999999999999999",
          "is_locked": 0
        },
        {
          "address": "0x0000000000000000000000000000000000000000",
          "tag": "Null Address",
          "is_contract": 0,
          "balance": "0.000000000000001",
          "percent": "0.000000000000000000",
          "is_locked": 1
        }
      ],
      "honeypot_with_same_creator": "0",
      "is_anti_whale": "0",
      "is_blacklisted": "0",
      "is_honeypot": "0",
      "is_in_dex": "0",
      "is_mintable": "1",
      "is_open_source": "1",
      "is_proxy": "0",
      "is_whitelisted": "0",
      "owner_address": "0x5c69bee701ef814a2b6a3edd4b1652cb9cc5aa6f",
      "owner_balance": "0",
      "owner_change_balance": "0",
      "owner_percent": "0.000000",
      "personal_slippage_modifiable": "0",
      "selfdestruct": "0",
      "sell_tax": "0.0493",
      "slippage_modifiable": "0",
      "token_name": "Uniswap V2",
      "token_symbol": "UNI-V2",
      "total_supply": "3698.64840178138587015",
      "trading_cooldown": "0",
      "transfer_pausable": "0"
    }
  }
}
"""
