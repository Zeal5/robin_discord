# from discord.ext import commands
from discord import app_commands, Embed, colour
from discord.ext import commands
import discord
from discord.ui import Button, View
from typing import Optional, Dict, Any, Coroutine, List, Union
from discord import ui
from . import bot_settings


class BuyModalView(ui.Modal, title="Create Wallet"):
    token_address = ui.TextInput(label="Token Adress",placeholder="Enter Token Address", min_length=40, max_length=42)
    amount = ui.button()
    
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message("bought")


    async def on_timeout(self) -> None:
        return await super().on_timeout()

