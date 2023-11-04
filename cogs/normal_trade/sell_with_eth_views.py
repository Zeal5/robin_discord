# from discord.ext import commands
from discord import app_commands, Embed, colour
from discord.ext import commands
import discord
from discord.ui import Button, View
from typing import Optional, Dict, Any, Coroutine, List, Union
from discord import ui
from . import bot_settings


class SellModalView(ui.Modal, title="Create Wallet"):
    token_address = ui.TextInput(label="Token Adress",placeholder="Enter Token Address", min_length=40, max_length=42)
    amount_to_buy_with = ui.button(label='1')
    amount_to_buy_with = ui.button(label='2')
    amount_to_buy_with = ui.button(label='3')


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
