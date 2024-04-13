
import ba
import _ba
import discord
from discord import app_commands
from discord.ext import commands
from discord.app_commands import Choice
import settings
from admin.permissions import GiveRole
from core.Core import namer

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

    @app_commands.command(
        name = "giverole",
        description = "Gives role directly from discord"
    )
    @app_commands.describe(
        role = "Role to be assigned",
        pid = "Player id"
    )
    @app_commands.choices(role = [
        Choice(name="Admin", value="admin"),
        Choice(name="Muted", value="mmute"),
        Choice(name="Owner", value="owner"),
        Choice(name="Vip", value="vip")
    ])
    async def giverole(
        self, interaction: discord.Interaction, role: str, pid: str
    ):
        name = namer(pid)
        if name == "Name":
            await interaction.response.send_message(
                f"Incorrect player id {pid}", ephemeral=True
            )
            return
        else:
            givenresponse = GiveRole(role, pid)
        if givenresponse:
            await interaction.response.send_message(
                f"Gave {role} to {name}", ephemeral=True
            )
        elif givenresponse is None:
            await interaction.response.send_message(
                f"Role {role} does not exist", ephemeral=True
            )
        elif not givenresponse:
            await interaction.response.send_message(
                f"{name} already has a role higher than {role}", ephemeral=True
            )

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        Admin(bot),
        guilds=[discord.Object(id=setting["discord"]["serverid"])])