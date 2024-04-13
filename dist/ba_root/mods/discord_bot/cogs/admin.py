
import ba
import _ba
import discord
from discord import app_commands
from discord.ext import commands
import settings

setting = settings.get_settings_data()

class Admin(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(
        name = "servermessage",
        description = "Sends a chat message to your server"
    )
    async def servermessage(
        self, interaction: discord.Interaction, message: str
        ):
        _ba.pushcall(
            ba.Call(ba.internal.chatmessage, message), from_other_thread=True
            )
        await interaction.response.send_message(
            f"Sent message to server", ephemeral=True
            )

    

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        Admin(bot),
        guilds=[discord.Object(id=setting["discord"]["serverid"])])