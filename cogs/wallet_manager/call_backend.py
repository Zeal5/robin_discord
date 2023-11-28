from typing import Optional, Union, Dict, List
from pydantic import BaseModel
from aiohttp import ClientResponse
from . import configs
import aiohttp
from . import configs
from discord import Embed, colour


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

# class GetAllWalletsList:

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
    url = f'{configs["url"]}{configs["endpoint"]["get_wallets"]}'
    data = UserWallet(tg_id = tg_id)
    _data = data.model_dump(mode='json')
    response = await make_request(url, _data)
    return response 

async def create_user_account(
    tg_id: int, secret: Optional[str] = None
) -> Wallet | WalletError:
    """takes in user id and wallet secret and returns a str"""
    url = f'{configs["url"]}{configs["endpoint"]["create_wallet"]}'
    data = UserWallet(tg_id=tg_id, secret=secret)
    _data = data.model_dump(mode="json")  # convert UserWallet to python dict | json
    print(_data)
    response = await make_request(url, _data)
    return response


class ChangeActiveWallet:
    class ActiveWallet(BaseModel):
        tg_id : int
        button_id : int

    def __init__(self):
        pass

    async def change_active_wallet_function(self,tg_id:int,  wallet_id : int) -> Union[bool, Embed]:
        url = f'{configs["url"]}{configs["endpoint"]["change_active_wallet"]}'
        data =  ChangeActiveWallet.ActiveWallet(tg_id = tg_id, button_id = wallet_id)
        _data= data.model_dump(mode= 'json')
        self.response = await self.make_request(url , _data)
        print(self.response)
        if isinstance(self.response,bool) and self.response:
            return True
        return await self._clean_response()  


    async def make_request(self, url: str, data: Dict) -> Union[bool, WalletError]:
        async with aiohttp.ClientSession() as Session:
            async with Session.patch(f"{url}", json=data) as response:
                print(response.status)
                if response.status == 200:
                    return await response.json()
                else:
                    return await self.not_success(response)


    async def not_success(self, response: ClientResponse) -> WalletError:
        res = await response.json()
        print(f"json response from backend = {res}")
        match response.status:
            case 400:
                return WalletError(reason=f"{res['detail']}")
            case _:
                print(f"not success_ok from change active wallet {response.status} : {await response.json()}")
                return WalletError(reason="Unkown error")
                
    
    async def _clean_response(self) -> Embed :
        if isinstance(self.response, WalletError):
            embed = Embed(
                title="Failed to Change Active Wallet",
                description=f"{self.response.reason}",
                color=colour.Colour.red(),
            )
        else:
            embed = Embed(
                title="Couldn't load embed",
                color=colour.Colour.red())


        return embed
            

