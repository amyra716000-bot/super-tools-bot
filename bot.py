import os
import hashlib

from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application


# =========================
# إعدادات البوت
# =========================

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise RuntimeError("BOT_TOKEN is not set")

PORT = int(os.getenv("PORT", "10000"))
RENDER_URL = os.getenv("RENDER_EXTERNAL_URL")

if not RENDER_URL:
    raise RuntimeError("RENDER_EXTERNAL_URL is not set")


# إنشاء البوت والـ Dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher()


# =========================
# أمر /start
# =========================

@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        "👋 أهلاً بك في Super Tools!\n\n"
        "🚀 البوت يعمل بنجاح\n\n"
        "📥 تحميل من YouTube\n"
        "📸 تحميل من Instagram\n"
        "🎵 تحميل من TikTok\n"
        "📘 تحميل من Facebook\n"
        "✨ زخرفة النصوص\n"
        "🤖 أدوات AI\n"
        "🛠 أدوات الملفات\n\n"
        "🔥 قريباً المزيد من الأدوات..."
    )


# =========================
# صفحة فحص Render
# =========================

async def health_check(request):
    return web.Response(text="Super Tools Bot is running!")


# =========================
# تشغيل Webhook
# =========================

async def on_startup(bot: Bot):
    # إنشاء مسار Webhook غير واضح
    webhook_hash = hashlib.sha256(TOKEN.encode()).hexdigest()[:32]
    webhook_path = f"/telegram/{webhook_hash}"

    webhook_url = f"{RENDER_URL}{webhook_path}"

    await bot.set_webhook(
        url=webhook_url,
        drop_pending_updates=True
    )

    print(f"Webhook set: {webhook_url}")


# =========================
# إنشاء Web Server
# =========================

app = web.Application()

app.router.add_get("/", health_check)

webhook_hash = hashlib.sha256(TOKEN.encode()).hexdigest()[:32]
webhook_path = f"/telegram/{webhook_hash}"

webhook_handler = SimpleRequestHandler(
    dispatcher=dp,
    bot=bot
)

webhook_handler.register(
    app,
    path=webhook_path
)

dp.startup.register(on_startup)

setup_application(
    app,
    dp,
    bot=bot
)


# =========================
# تشغيل البرنامج
# =========================

if __name__ == "__main__":
    web.run_app(
        app,
        host="0.0.0.0",
        port=PORT
    )
