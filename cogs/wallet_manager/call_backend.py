from typing import Optional, Union, Dict, List
from pydantic import BaseModel
from aiohttp import ClientResponse
from . import configs
import aiohttp
from . import configs


class UserWallet(BaseModel):
    tg_id: int
    secret: Optional[str] = None


class Wallet(BaseModel):
    wallet_name: str
    address: str
    secret: Optional[str] = None
    is_active: Optional[bool] = None
    id: Optional[int] = None



class WalletError(BaseModel):
    reason: str


async def success_ok(response: dict) -> Union[Wallet, List[Wallet]]:
    print(f"response from success_ok = {response}")
    if isinstance(response, list):
        wallets = []
        for i in response:
            wallets.append(Wallet(**i))
        return wallets
    return Wallet(**response)


async def not_success(response: ClientResponse) -> WalletError:
    res = await response.json()
    print(f"json response from backend = {res}")
    match response.status:
        case 400:
            return WalletError(reason=f"{res['detail']}")
        case _:
            return WalletError(reason="Unkown error")


async def make_request(url: str, data: Dict) -> Union[List[Wallet], Wallet, WalletError]:
    async with aiohttp.ClientSession() as Session:
        async with Session.post(f"{url}", json=data) as response:
            print(response.status)
            if response.status == 200:
                return await success_ok(await response.json())
            return await not_success(response)

async def get_all_wallets(tg_id : int) -> List[Wallet] | WalletError | Wallet :
    url = configs['url']['get_wallets']
    data = UserWallet(tg_id = tg_id)
    _data = data.model_dump(mode='json')
    response = await make_request(url, _data)
    return response 

async def create_user_account(
    tg_id: int, secret: Optional[str] = None
) -> Wallet | WalletError:
    """takes in user id and wallet secret and returns a str"""
    url = configs["url"]["create_wallet"]
    data = UserWallet(tg_id=tg_id, secret=secret)
    _data = data.model_dump(mode="json")  # convert UserWallet to python dict | json
    print(_data)
    response = await make_request(url, _data)
    return response
