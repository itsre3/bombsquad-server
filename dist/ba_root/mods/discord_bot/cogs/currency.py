
import discord
from discord import app_commands
from discord.ext import commands
import settings
import coinsystem

setting = settings.get_settings_data()

class test(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command()
    async def hi(self, ctx):
        await ctx.send("Hello")

    @app_commands.command(
            name = "connect",
            description = "Link your discord to your server account"
            )
    @app_commands.describe(
        pid = "Your BombSquad PbId"
    )
    async def connect(
        self,
        interaction: discord.Interaction,
        pid: str):
        message = coinsystem.update_dcid(interaction.user.id, pbid=pid)
        await interaction.response.send_message(
            message, ephemeral=True
        )

    @app_commands.command(
        name = "balance",
        description = "Check your balance"
    )
    async def balance(
        self, interaction: discord.Interaction
    ):
        balance = coinsystem.get_coins_by_dcid(interaction.user.id)
        await interaction.response.send_message(
            balance, ephemeral=True
        )

    @app_commands.command(
        name = "reset",
        description = "Reset your linked pbid"
    )
    async def reset(
        self, interaction: discord.Interaction
    ):
        message = coinsystem.reset_dcid(interaction.user.id)
        await interaction.response.send_message(
            message, ephemeral=True
        )

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        test(bot),
        guilds=[discord.Object(id=setting["discord"]["serverid"])])