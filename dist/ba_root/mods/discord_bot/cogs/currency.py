
import discord
from discord import app_commands
from discord.ext import commands
import settings

setting = settings.get_settings_data()

class test(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command()
    async def hi(self, ctx):
        await ctx.send("Hello")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        test(bot),
        guilds=[discord.Object(id=setting["discord"]["serverid"])])