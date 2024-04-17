import discord
from discord.ext import commands
import settings
setting = settings.get_settings_data()

class Normal(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        Normal(bot),
        guilds=[discord.Object(id=setting["discord"]["serverid"])])