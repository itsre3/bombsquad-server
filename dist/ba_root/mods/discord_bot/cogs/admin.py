
import ba
import _ba
import discord
from discord import app_commands
from discord.ext import commands
from discord.app_commands import Choice
import settings
from admin.permissions import GiveRole, TakeRole, Effect
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

    @app_commands.command(
        name = "takerole",
        description = "Removes roles directly from discord"
    )
    @app_commands.describe(
        role = "The role to remove",
        pbid = "Player id"
    )
    @app_commands.choices(role = [
        Choice(name="Admin", value="admin"),
        Choice(name="Mute", value="mute"),
        Choice(name="Owner", value="owner"),
        Choice(name="Vip", value="vip")
    ])
    async def takerole(
        self, interaction: discord.Interaction, role: str, pbid: str
    ):
        name = namer(pbid)
        if name == "Name":
            await interaction.response.send_message(
                f"Player id is incorrect {pbid}", ephemeral=True
            )
            return
        givenresponse = TakeRole(role, pbid)
        if givenresponse:
            await interaction.response.send_message(
                f"Successfully removed role {role} from {name}", ephemeral=True
            )
        elif not givenresponse:
            await interaction.response.send_message(
                f"{name} does not have specified role {role}", ephemeral=True
            )
        elif givenresponse is None:
            await interaction.response.send_message(
                f"Role {role} does not exist", ephemeral=True
            )

    @app_commands.command(
        name="effect",
        description="Add and remove effects directly from dicord"
    )
    @app_commands.describe(
        action="Add or Remove effect",
        effect="Effect to assign or remove",
        pbid="Player Id"
    )
    @app_commands.choices(
        action=[
            Choice(name="Add", value="add"),
            Choice(name="Remove", value="remove")
        ],
        effect=[
            Choice(name="Ice", value="Ice"),
            Choice(name="Metal", value="Metal"),
            Choice(name="ProSurround", value="ProSurround"),
            Choice(name="Rainbow", value="Rainbow"),
            Choice(name="Stickers", value="Stickers"),
            Choice(name="Slime", value="Slime")
        ]
    )
    async def effect(
        self, interaction: discord.Interaction, action: str, effect: str, pbid: str
        ):
        name = namer(pbid)
        if name == "Name":
            await interaction.response.send_message(
                f"Invalid player id {pbid}", ephemeral=True
            )
            return
        givenresponse = Effect(action, effect, pbid)
        if not givenresponse:
            await interaction.response.send_message(
                f"Effect does not exist {effect}", ephemeral=True
            )
            return
        if action == "add":
            if givenresponse:
                await interaction.response.send_message(
                    f"Succesfully added {effect} to {name}", ephemeral=True
                )
            elif givenresponse is None:
                await interaction.response.send_message(
                    f"Players cannot have more than 2 effects", ephemeral=True
                )
            elif givenresponse == "AlreadyHas":
                await interaction.response.send_message(
                    f"Player {name} already has {effect}", ephemeral=True
                )
        elif action == "remove":
            if givenresponse:
                await interaction.response.send_message(
                    f"Succesfully removed {effect} from {name}", ephemeral=True
                )
            elif not givenresponse:
                await interaction.response.send_message(
                    f"Player do not have any effecct", ephemeral=True
                )
            elif givenresponse is None:
                await interaction.response.send_message(
                    f"Player {name} does not have {effect}", ephemeral=True
                )
        else:
            await interaction.response.send_message(
                f"Error processing. Try again", ephemeral=True
            )

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        Admin(bot),
        guilds=[discord.Object(id=setting["discord"]["serverid"])])