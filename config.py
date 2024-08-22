# токен бота
BOT_TOKEN = "MTI3MjQ3MjE4NjU5ODMzMDQzOA.GOpgsu.oRj3A1ctxrId9qgYOeA3Q4Es2pTiDanXjE8tQw"

# Префикс команд
COMMAND_PREFIX = "/"

# Блок для команды Rule34Get
COMMAND1 = "rule34_get"
COMMAND1_DESCRIPTION = "🔍 | Парсинг ну очень интересных картинок"
COMMAND1_ALLOW_CHANNELS = [1276204389970870283]
COMMAND1_NOT_ALLOW_CHANNEL_MESSAGE = (f"🚫 | Вы не можете использовать это здесь: "
                                      f"{[f"<#{chan}>" for chan in COMMAND1_ALLOW_CHANNELS]}")
COMMAND1_PERMISSIONS = [1276204469972893740]
COMMAND1_ACCESS_DENIED_MESSAGE = ("🚫 | Извините у вас нету прав использовать эту команду\n"
                                  "Вы должны быть истинным фанатом Андрея :heart_eyes:")
COMMAND1_UNKOWN_TAG_MESSAGE = "🚫 | Данный тег отсутствует на сайте: {tag}"
COMMAND1_IN_PROGRESS_MESSAGE = ("🔍 | Внимание парсинг в процессе!\n"
                                "🌐 | URL: {url}\n"
                                "📄 | Количество страниц: {pages}\n"
                                "🚫 | Забаненные теги: {ban_tags}\n"
                                "⏳ | Примерное время ожидания: {progress_time}")
