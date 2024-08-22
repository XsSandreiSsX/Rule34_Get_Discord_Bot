from config import BOT_TOKEN, COMMAND_PREFIX
from discord.ext import commands
import discord
import asyncio


class MyDiscordClient(commands.Bot):
    # При подключении бота
    async def on_ready(self):
        print(f"[!]: Бот подключен за: {self.user}")

        # Синхронизовать команды
        await self.tree.sync()


# Устанавливаем права для бота
intents = discord.Intents.all()


# Создаем клиент бота
client = MyDiscordClient(command_prefix=COMMAND_PREFIX, intents=intents)


async def main():
    extensions = [
        "cogs.commands.rule34_get",
        "cogs.commands.clear_chat",
    ]
    for extension in extensions:
        try:
            await client.load_extension(extension)
            print(f'Успешно загружен модуль: {extension}')
        except Exception as e:
            print(f'Не удалось загрузить модуль {extension}: {e}')
    await client.start(BOT_TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
