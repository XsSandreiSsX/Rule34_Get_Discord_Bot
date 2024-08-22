import discord
from discord.ext.commands import Cog
from discord import app_commands


class ClearChat(Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="clear", description="Очищает весь чат.")
    @app_commands.default_permissions(administrator=True)
    async def clear(self, interaction: discord.Interaction):
        await interaction.channel.purge(limit=None)
        await interaction.response.send_message("Чат полностью очищен от дерьма!")


async def setup(bot):
    await bot.add_cog(ClearChat(bot))