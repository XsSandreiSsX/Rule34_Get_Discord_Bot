import asyncio
from bs4 import BeautifulSoup
import aiohttp


class Rule34Parser:
    domain_url = "https://rule34.xxx/index.php?page=post&s=list&tags="
    root_url = "https://rule34.xxx/index.php"

    def __init__(self, current_link: str, count_pages: int, ban_tags: list = None):
        """Инициализируем класс для дальнейшего исполования"""
        self.current_link = current_link  # Ссылка на категорию
        self.count_pages = count_pages  # Количество обрабатываемых страниц
        self.ban_tags = ban_tags

        # Пустые списки для дальнейшей работы
        self.all_pages_urls = [self.current_link]  # Список со всеми страницами
        self.all_images_urls = []  # Список со всеми ссылка на посты
        self.images_src_urls = []  # Список из всех ссылок на изображения

    async def get_all_pages(self, session: aiohttp.ClientSession):
        """Получаем ссылки на все страницы, указанные пользователя по порядку"""
        for page_num in range(self.count_pages - 1):
            async with session.get(url=self.all_pages_urls[-1]) as response:
                soup = BeautifulSoup(await response.text(), "html.parser")
                next_link = soup.select_one("a[alt='next']")["href"]
                if next_link:
                    next_link = f"{self.root_url}{soup.select_one("a[alt='next']")["href"]}"
                    self.all_pages_urls.append(next_link)

    async def get_page_images(self, page_url: str, session: aiohttp.ClientSession):
        """Получение всех изображений на одной странице"""
        async with session.get(url=page_url) as response:
            soup = BeautifulSoup(await response.text(), "html.parser")
            return [f"{self.root_url}{a["href"]}" for a in soup.select(".thumb > a")]

    async def get_image_src_link(self, image_url: str, session: aiohttp.ClientSession):
        """Получение прямой ссылки на изображение из поста Rule34"
        С дополнительной проверкой на запрещенные теги"""
        async with session.get(url=image_url) as response:
            if response.status != 200:
                return ""
            soup = BeautifulSoup(await response.text(), "html.parser")

            tags = [tag.text for tag in soup.select("#tag-sidebar .tag a:nth-child(2)")]
            if set(self.ban_tags).intersection(set(tags)):
                return ""

            image_src = soup.select_one("#image")
            if not image_src:
                return ""
            return image_src["src"]

    async def __call__(self, *args, **kwargs):
        async with aiohttp.ClientSession() as session:
            await self.get_all_pages(session)

            print(self.all_pages_urls)

            for i in range(0, len(self.all_pages_urls), 9):
                batch = self.all_pages_urls[i:i + 9]
                tasks = [self.get_page_images(cur_page_link, session) for cur_page_link in batch]

                # Выполнение 9 задач одновременно
                self.all_images_urls.extend(await asyncio.gather(*tasks))

                # Задержка перед следующей группой запросов
                if i + 9 < len(self.all_pages_urls):
                    await asyncio.sleep(2)  # Задержка в 2 секунд

            self.all_images_urls = sum(self.all_images_urls, [])

            for i in range(0, len(self.all_images_urls), 9):
                batch = self.all_images_urls[i:i + 9]
                tasks = [self.get_image_src_link(cur_image_link, session) for cur_image_link in batch]

                # Выполнение 9 задач одновременно
                self.images_src_urls.extend(await asyncio.gather(*tasks))

                # Задержка перед следующей группой запросов
                if i + 9 < len(self.all_images_urls):
                    await asyncio.sleep(2)  # Задержка в 2 секунд

            return self.images_src_urls

    @staticmethod
    async def check_url(url: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url) as response:
                soup = BeautifulSoup(await response.text(), "html.parser")
                if not soup.select(".thumb > a"):
                    return False

                return True
