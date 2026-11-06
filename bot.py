import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiohttp import web

# Отримуємо токен з безпечних змінних середовища Render
TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Базовий обробник команди /start
@dp.message(lambda message: message.text == "/start")
async def cmd_start(message: types.Message):
    await message.answer("Вітаю! NUL-аналітичний бот активований і готовий до роботи.")

# Простий вебсервер для задоволення вимог Render до портів
async def handle(request):
    return web.Response(text="NUL Bot is alive and running!")

async def start_web_server():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    
    # Render автоматично виділяє порт через змінну середовища PORT
    port = int(os.getenv("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    logging.info(f"Web server started on port {port}")

async def main():
    # Запускаємо вебсервер і бота одночасно
    await start_web_server()
    logging.info("Starting bot polling...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
