
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
            name = "Link",
            description = "Link your discord to your server account"
            )
    @app_commands.describe(
        PbId = "Your BombSquad PbId"
    )
    async def Link(
        self,
        interaction: discord.Interaction,
        PbId: str):
        message = coinsystem.update_dcid(str(interaction.user.id), pbid=PbId)
        await interaction.response.send_message(
            message, euphemeral=True
        )

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        test(bot),
        guilds=[discord.Object(id=setting["discord"]["serverid"])])