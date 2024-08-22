from service.chrome.Rule34Parser import Rule34Parser
from discord import app_commands
from discord.ext import commands
from discord import Interaction
import discord.ui
import config


class ModalWindow(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="Заполните ваш запрос")

        self.tag = discord.ui.TextInput(label="Введите тег или ссылку Rule34",
                                        placeholder="one_piece",
                                        required=True,
                                        max_length=60,
                                        style=discord.TextStyle.long)

        self.count_pages = discord.ui.TextInput(label="Введите количество страниц",
                                                placeholder="5",
                                                required=True,
                                                max_length=2,
                                                style=discord.TextStyle.short)

        self.ban_tags = discord.ui.TextInput(label="Введите запретные теги через пробел",
                                             placeholder="futanari",
                                             required=False,
                                             max_length=450,
                                             style=discord.TextStyle.paragraph)

        self.add_item(self.tag)
        self.add_item(self.count_pages)
        self.add_item(self.ban_tags)

    async def on_submit(self, interaction: Interaction):
        if "https" not in self.tag.value:
            self.tag = f"{Rule34Parser.domain_url}{self.tag.value}&pid=0"
        if self.ban_tags:
            self.ban_tags = self.ban_tags.value.split()

        if not await Rule34Parser.check_url(self.tag):
            await interaction.response.send_message(config.COMMAND1_UNKOWN_TAG_MESSAGE.format(tag=self.tag), ephemeral=True)

        expected_time = 9.333 * int(self.count_pages.value)

        await interaction.response.send_message(config.COMMAND1_IN_PROGRESS_MESSAGE.format(url=self.tag,
                                                                                           pages=self.count_pages,
                                                                                           ban_tags=self.ban_tags,
                                                                                           progress_time=expected_time))

        # Начало действия
        parser = Rule34Parser(self.tag, int(self.count_pages.value), ban_tags=self.ban_tags)
        process_done = await parser()
        print(process_done)
        for src_url in process_done:
            if src_url:
                await interaction.channel.send(src_url)


class Rule34Get(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name=config.COMMAND1, description=config.COMMAND1_DESCRIPTION)
    async def rule34_get(self, interaction: Interaction):
        # Проверка на разрешенный канал
        if interaction.channel.id not in config.COMMAND1_ALLOW_CHANNELS:
            await interaction.response.send_message(config.COMMAND1_NOT_ALLOW_CHANNEL_MESSAGE, ephemeral=True)
            return
        # Проверка на разрешенные права
        if not set(config.COMMAND1_PERMISSIONS).intersection(set([role.id for role in interaction.user.roles])):
            await interaction.response.send_message(config.COMMAND1_ACCESS_DENIED_MESSAGE, ephemeral=True)
            return

        # Отправить модальное окно
        await interaction.response.send_modal(ModalWindow())


async def setup(bot):
    await bot.add_cog(Rule34Get(bot))
