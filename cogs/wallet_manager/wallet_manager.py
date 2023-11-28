# from discord.ext import commands
from discord import app_commands, Embed, colour
from discord.ext import commands
import discord
from discord.ui import Button, View
from typing import Optional, Dict, Any, Coroutine, List, Union
from .call_backend import create_user_account,get_all_wallets, Wallet, WalletError
from .views import DropdownView, RecoveryPhrasePrompt ,ChangeActiveWalletView
from discord import ui
from . import bot_settings




class WalletView(View):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    @discord.ui.button(label="create_wallet", style=discord.ButtonStyle.success, row=1)
    async def create_wallet(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.response.send_message(
            view=DropdownView(),
            ephemeral=True,
            delete_after=float(
                bot_settings.get("timeout", "dropdown_message", fallback=180)
            ),
        )

    @discord.ui.button(label="add_wallet", style=discord.ButtonStyle.danger, row=1)
    async def add_wallet(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.response.send_modal(RecoveryPhrasePrompt())

    @discord.ui.button(label="get_wallets", style=discord.ButtonStyle.gray, row=1)
    async def get_wallets(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        wallets: List[Wallet] = await get_all_wallets(interaction.user.id)
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


class Manager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="wallet",description="Add Wallet or create a new Wallet")
    async def my_command(self, interaction: discord.Interaction) -> None:

        embed = Embed(
            title="Wallet Manager",
            description="Manager wallets, Create New wallet, check existing wallet",
        )
        await interaction.response.send_message(
            embed=embed,
            view=WalletView(self.bot),
            ephemeral=True,
            delete_after=float(
                bot_settings.get("timeout", "original_message", fallback=240)
            ),
        )


async def setup(bot):
    await bot.add_cog(Manager(bot))
