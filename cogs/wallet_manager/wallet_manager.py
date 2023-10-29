# from discord.ext import commands
from discord import app_commands, Embed, colour
from discord.ext import commands
import discord
from discord.ui import Button, View
from typing import Optional, Dict, Any, Coroutine
from .call_backend import create_user_account, Wallet, WalletError
from discord import ui
from . import bot_settings


class RecoveryPhrasePrompt(ui.Modal, title="Create Wallet"):
    secret = ui.TextInput(label="Wallet Secret")

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        print(f"user is {interaction.user.id}")
        backend_response = await create_user_account(
            interaction.user.id
        )  # TODO take secret as input
        print(backend_response)
        print(type(backend_response))
        if isinstance(backend_response, WalletError):
            await interaction.response.send_message(
                f"{WalletError.reason}",
                ephemeral=True,
                delete_after=float(
                    bot_settings.get("timeout", "ephemeral_message", fallback=15)
                ),
            )
        if isinstance(backend_response, Wallet):
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
            await interaction.user.send(embed=embed)
        # await interaction.response.send_message(
        #     f"Thanks for your response, {backend_response}!",
        #     ephemeral=True,
        #     delete_after=float(
        #         bot_settings.get("timeout", "ephemeral_message", fallback=15)
        #     ),
        # )

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

        # The placeholder is what will be shown when no option is chosen
        # The min and max values indicate we can only pick one of the three options
        # The options parameter defines the dropdown options. We defined this above
        super().__init__(
            placeholder="How many wallet do you want to create",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: discord.Interaction):
        # Use the interaction object to send a response message containing
        # the user's favourite colour or choice. The self object refers to the
        # Select object, and the values attribute gets a list of the user's
        # selected options. We only want the first one.
        await interaction.response.send_message(
            f"{self.values[0]} New Wallets have been created"
        )
        self._view =None 
    # async def interaction_check(self, interaction: discord.Interaction):
    #     print(interaction.data)
    #     #     await self.message.delete()
    #     #     return False
    #     # return True
    #
    #     await interaction.delete_original_response()


class DropdownView(discord.ui.View):
    def __init__(self):
        super().__init__()
        # Adds the dropdown to our view object.
        self.add_item(Dropdown())


class WalletView(View):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    @discord.ui.button(label="create_wallet", style=discord.ButtonStyle.success, row=1)
    async def create_wallet(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        # backend_response = await create_user_account(interaction.user.id)
        # embed = Embed(
        #     title="adding new wallet",
        #     description=f"{mes}",
        #     color=colour.Colour.green(),
        # )
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
        embed = Embed(
            title="getting new wallet",
            description="geting getin fetin",
            color=colour.Colour.green(),
        )
        await interaction.response.defer(ephemeral=True)
        await interaction.edit_original_response(embed=embed)


class Manager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="wallet_manager")
    async def my_command(self, interaction: discord.Interaction) -> None:
        """Add wallet or create new wallet"""

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
