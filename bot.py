import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiohttp import web

TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()

# 1. Обробник команди /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Вітаю! NUL-аналітичний бот активований.\n\n"
        "Надішліть мені будь-який геополітичний або адміністративний текст, "
        "і я виконаю його онтологічний аналіз за параметрами R1, R2, R3, R4."
    )

# 2. Обробник для будь-якого тексту (NUL-аналіз)
@dp.message()
async def analyze_text(message: types.Message):
    text = message.text
    
    # Споріднена структура NUL-аналізу (розрахунок вагових коефіцієнтів)
    length = len(text)
    
    # Приклад базового розподілу (тут підключається ваша аналітична функція)
    r4_noise = round(min(40.0, length * 0.05), 1)  # Маса / шуми
    r1_substance = round(max(10.0, 100 - r4_noise - 30), 1)  # Сутність / код
    r2_trigger = 15.0  # Енергія / тригери
    r3_inertia = round(100.0 - (r1_substance + r2_trigger + r4_noise), 1) # Часова інерція

    response = (
        "📊 **NUL-онтологічний аналіз тексту:**\n\n"
        f"🔹 **R1 (Сутність / Код):** {r1_substance}%\n"
        f"⚡ **R2 (Енергія / Тригери):** {r2_trigger}%\n"
        f"⏳ **R3 (Часова інерція):** {r3_inertia}%\n"
        f"🌫 **R4 (Маса / Шум):** {r4_noise}%\n\n"
        "🔍 **Висновок системи:** Текст прийнято в обробку. Структурне редукування пройшло успішно."
    )
    
    await message.answer(response, parse_mode="Markdown")

# Простий вебсервер для задоволення вимог Render до портів
async def handle(request):
    return web.Response(text="NUL Bot is alive and running!")

async def start_web_server():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    
    port = int(os.getenv("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    logging.info(f"Web server started on port {port}")

async def main():
    await start_web_server()
    logging.info("Starting bot polling...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
