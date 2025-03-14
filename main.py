import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv
from db import create_table
from handlers import router

load_dotenv()
BOT_TOKEN = os.getenv("TOKEN")
bot = Bot(token=BOT_TOKEN,
          default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
dp.include_router(router)


async def main():
    await create_table()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
