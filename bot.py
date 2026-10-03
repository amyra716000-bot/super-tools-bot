
import os
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        "👋 أهلاً بك في Super Tools!\n\n"
        "⚡ البوت قيد التطوير...\n"
        "📥 التحميل\n"
        "✨ الزخرفة\n"
        "🤖 أدوات AI\n"
        "🛠 أدوات الملفات\n\n"
        "انتظرونا 🔥"
    )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
