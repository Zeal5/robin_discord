from pydantic import BaseModel
from typing import List, Dict, Optional


class TokenInfo(BaseModel):
   anti_whale_modifiable: Optional[bool] = None
   buy_tax: Optional[float] = None
   can_take_back_ownership: Optional[float] = None
   cannot_buy: Optional[bool] = None
   cannot_sell_all: Optional[bool] = None
   creator_address: Optional[str] = None
   creator_balance: Optional[float] = None
   creator_percent: Optional[float] = None
   dex: Optional[List[Dict]] = None
   external_call: Optional[str] = None
   hidden_owner: Optional[bool] = None
   holder_count: Optional[int] = None
   holders: Optional[List[Dict]] = None
   honeypot_with_same_creator: Optional[bool] = None
   is_airdrop_scam: Optional[bool] = None
   is_anti_whale: Optional[bool] = None
   is_blacklisted: Optional[bool] = None
   is_honeypot: Optional[bool] = None
   is_in_dex: Optional[bool] = None
   is_mintable: Optional[str] = None
   is_open_source: Optional[bool] = None
   is_proxy: Optional[bool] = None
   is_true_token: Optional[bool] = None
   is_whitelisted: Optional[bool] = None
   lp_holder_count: Optional[int] = None
   lp_holders: Optional[List[Dict]] = None
   lp_total_supply: Optional[float] = None
   note: Optional[str] = None
   other_potential_risks: Optional[str] = None
   owner_address: Optional[str] = None
   owner_balance: Optional[int] = None
   owner_change_balance: Optional[bool] = None
   owner_percent: Optional[float] = None
   personal_slippage_modifiable: Optional[bool] = None
   selfdestruct: Optional[bool] = None
   sell_tax: Optional[float] = None
   slippage_modifiable: Optional[bool] = None
   token_name: Optional[str] = None
   token_symbol: Optional[str] = None
   total_supply: Optional[int] = None
   trading_cooldown: Optional[bool] = None
   transfer_pausable: Optional[bool] = None
   trust_list: Optional[bool] = None
   error: Optional[str] = None


class TokenModel(BaseModel):
 address: Optional[str] = None
 name: Optional[str] = None
 symbol: Optional[str] = None

class LiquidityModel(BaseModel):
 base: Optional[float] = None
 quote: Optional[float] = None
 usd: Optional[float] = None

class PriceChangeModel(BaseModel):
 h1: Optional[float] = None
 h24: Optional[float] = None
 h6: Optional[float] = None
 m5: Optional[float] = None

class TxnsModel(BaseModel):
 buys: Optional[int] = None
 sells: Optional[int] = None

class VolumeModel(BaseModel):
 h1: Optional[float] = None
 h24: Optional[float] = None
 h6: Optional[float] = None
 m5: Optional[float] = None

class DexScreenerModel(BaseModel):
 baseToken: Optional[TokenModel] = None
 chainId: Optional[str] = None
 dexId: Optional[str] = None
 fdv: Optional[int] = None
 labels: Optional[List[str]] = None
 liquidity: Optional[LiquidityModel] = None
 pairAddress: Optional[str] = None
 pairCreatedAt: Optional[int] = None
 priceChange: Optional[PriceChangeModel] = None
 priceNative: Optional[str] = None
 priceUsd: Optional[str] = None
 quoteToken: Optional[TokenModel] = None
 txns: Optional[Dict[str, TxnsModel]] = None
 url: Optional[str] = None
 volume: Optional[VolumeModel] = None
