# from discord.ext import commands
from discord import (
    Forbidden as forbidden_exception,
    HTTPException as discord_httpexception,
)
from discord import app_commands, Embed, colour
from discord.ext import commands
import discord
from discord.ui import Button, View
from typing import Optional, Dict, Any, Coroutine, Union, List
from .call_backend import create_user_account, Wallet, WalletError, ChangeActiveWallet, get_all_wallets
from discord import ui
from . import bot_settings
import asyncio


def clean_message(backend_response: Union[Wallet, WalletError]) -> Embed:
    if isinstance(backend_response, WalletError):
        embed = Embed(
            title="Failed to create new wallet",
            description=f"{backend_response.reason}",
            color=colour.Colour.red(),
        )

    elif isinstance(backend_response, Wallet):
        embed = Embed(
            title="New Wallet has been created",
            description=f"{backend_response.wallet_name}",
            color=colour.Colour.green(),
        )
        embed.add_field(
            name="Address", value=f"```{backend_response.address}```", inline=False
        )
        embed.add_field(
            name="Secret", value=f"```{backend_response.secret}```", inline=False
        )
    return embed


class RecoveryPhrasePrompt(ui.Modal, title="Create Wallet"):
    secret = ui.TextInput(label="Wallet Secret",placeholder="enter Seed phrase or Private Keys", min_length=36, max_length=120)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        print(f"user is {interaction.user.id}")
        backend_response = await create_user_account(
            interaction.user.id, secret=str(self.secret)
        )  # TODO take secret as input
        print(backend_response)
        print(type(backend_response))
        embed = clean_message(backend_response)
        try:
            await interaction.user.send(embed=embed)
        except (discord_httpexception, forbidden_exception) as e:
            # @TODO add to logs
            print(str(e))
        await interaction.edit_original_response(embed=embed)

    async def on_timeout(self) -> None:
        return await super().on_timeout()


class Dropdown(discord.ui.Select):
    def __init__(self):
        # Set the options that will be presented inside the dropdown
        options = [
            discord.SelectOption(label="1"),
            discord.SelectOption(label="2"),
            discord.SelectOption(label="3"),
        ]

        super().__init__(
            placeholder="How many wallet do you want to create",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: discord.Interaction):
        # First reply after user selects how many wallets he wants to create
        await interaction.response.edit_message(
            content=f"Creating {self.values[0]} Wallet[s]",
            delete_after=float(
                bot_settings.get("timeout", "dropdown_message", fallback=300)
            ),
            view=None,
        )
        embeds_list = []
        for _ in range(0, int(self.values[0])):
            new_wallet: Union[Wallet, WalletError] = await create_user_account(
                interaction.user.id
            )
            embeds_list.append(clean_message(new_wallet))

        try:
            await interaction.user.send(
                # content=f"{self.values[0]} New Wallet[s] have been created",
                embeds=embeds_list,
            )
        except (forbidden_exception, discord_httpexception) as e:
            # @TODO add to logs
            print(str(e))

        embeds_with_footer = []
        for i in embeds_list:
            embeds_with_footer.append(
                i.set_footer(text="This message will be deleted in about 5 minutes")
            )
        await interaction.edit_original_response(
            # content=f"{self.values[0]} New Wallet[s] have been created",
            embeds=embeds_with_footer,
            # ephemeral= True,
            # delete_after=float(
            #     bot_settings.get("timeout", "original_message", fallback=300)
            # ),
            # # view=None,
        )


class DropdownView(discord.ui.View):
    def __init__(self):
        super().__init__()
        # Adds the dropdown to our view object to select number of wallets to be created.
        self.add_item(Dropdown())


class SelectWalletButton(discord.ui.Button):
    def __init__(self, wallet: Wallet):
        super().__init__(
            custom_id=str(wallet.id),
            style=discord.ButtonStyle.primary,
            disabled=wallet.is_active,
            label=f"{wallet.id}",
        )

    async def callback(self, interaction: discord.Interaction):
        is_changed: bool | Embed = await ChangeActiveWallet().change_active_wallet_function(
            tg_id=interaction.user.id, wallet_id=int(interaction.data.get("custom_id"))
        )

        if isinstance( is_changed,bool):
            wallets: List[Wallet] | Any = await get_all_wallets(interaction.user.id)
            embed = Embed(
                title="All Wallets",
                # description="",
                color=colour.Colour.green(),
            )
            embed.set_footer(text = "This message will be deleted after 4 minutes")
            for wallet in wallets:
                embed.add_field(
                    name = f"{wallet.wallet_name} {' :white_check_mark:' if wallet.is_active else ''}",
                    value= f"```{wallet.address}```",
                    inline = False )
            await interaction.response.edit_message(embed=embed,view = ChangeActiveWalletView(interaction, wallets))
        elif isinstance(is_changed, Embed):
            await interaction.response.edit_message(embed=is_changed)
            


class ChangeActiveWalletView(discord.ui.View):
    def __init__(self, interaction: discord.Interaction, wallets_list: List[Wallet]):
        super().__init__()
        for wallet in wallets_list:
            self.add_item(SelectWalletButton(wallet))
