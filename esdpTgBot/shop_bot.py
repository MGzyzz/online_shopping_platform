import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
import httpx
from aiogram.types import URLInputFile, WebAppInfo


async def shop_data():
    async with httpx.AsyncClient() as client:
        response = await client.get('http://localhost:8000/api/shop_for_telegram/')
        result = response.json()

        return result


class ShopBot:
    def __init__(self, token, shop_data):
        self.token = token
        self.bot = Bot(token=token)
        self.dp = Dispatcher()
        self.shop_data = shop_data

        @self.dp.message(Command('start'))
        async def start(message: types.Message):
            image_from_url = URLInputFile(self.shop_data['logo'])
            await message.answer_photo(image_from_url, caption=f'Здраствуйте! Вас приветствует бот магазина: {self.shop_data["name"]}\n'
                                                               f'Описание нашего магазина: {self.shop_data["description"]}')

        @self.dp.message(Command('info'))
        async def info(message: types.Message):

            await message.answer(
                'Что я могу:',
                reply_markup=self.get_keyboard()
            )

    async def run(self):
        await self.dp.start_polling(self.bot)

    def get_keyboard(self):
        buttons = [
            [
                types.InlineKeyboardButton(text="Каталог магазина", callback_data='test2'),
                types.InlineKeyboardButton(text="Оформить досатвку", web_app=WebAppInfo(url="https://market.shopuchet.kz/static/telegram.html"))
            ],
            [types.InlineKeyboardButton(text="Перейти на наш сайт", url='https://www.youtube.com/')]
        ]
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
        return keyboard


async def main() -> None:
    shop_data_list = await shop_data()
    bots = [ShopBot(token=shop['tg_token'], shop_data=shop) for shop in shop_data_list]
    await asyncio.gather(*(bot.run() for bot in bots))


if __name__ == '__main__':
    asyncio.run(main())
