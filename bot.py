import os
import asyncio
import logging
import math
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
        "⚡ **NUL-Онтологічний Сканер активований.**\n\n"
        "Математичне ядро ('Теорія Абсолюту', Глава III) завантажено в систему.\n"
        "Надішліть будь-який текст, закон чи новину, і я виконаю розрахунок за формулами потенційного балансу, "
        "визначивши $R_1-R_4$, ентропію ($S$) та мниму вісь сенсу ($i$)."
    )

# НУЛ-математичний апарат на основі Третьої глави
def calculate_nul_matrix(text: str):
    length = len(text)
    if length == 0:
        return 0, 0, 0, 0, 0, 0

    words = text.split()
    word_count = len(words)
    
    # Оцінка щільності та структури (R1 - Твердий Код / Сутність)
    # Формула базується на співвідношенні унікальних символів та довжини
    structural_density = min(85.0, max(15.0, (len(set(text)) / length) * 250))
    
    # Енергетичний тригер / Потенціал (R2)
    # Чим більше знаків оклику, активних дієслів або коротких різких конструкцій — тим вищий потенціал
    action_triggers = text.count("!") + text.count("?") + sum(1 for w in words if len(w) > 6)
    r2_energy = min(50.0, max(10.0, (action_triggers / max(1, word_count)) * 100))
    
    # Часова інерція (R3)
    r3_inertia = round(max(5.0, 30.0 - (r2_energy * 0.3)), 1)
    
    # Ентропійний залишок та Матеріальний осад (R4) через квадрат мнимого потенціалу (i^2 = -1)
    # Вода, зайві символи та розмиті формулювання створюють ентропію (S)
    entropy_noise = max(5.0, 100.0 - (structural_density + r2_energy + r3_inertia))
    
    # Нормалізація суми до 100%
    total = structural_density + r2_energy + r3_inertia + entropy_noise
    r1 = round((structural_density / total) * 100, 1)
    r2 = round((r2_energy / total) * 100, 1)
    r3 = round((r3_inertia / total) * 100, 1)
    r4 = round((entropy_noise / total) * 100, 1)

    # Вилучення оператора сенсу (i = sqrt(-1) аналог для напруги системи)
    # Мнима складова відображає прихований вектором потенціал
    imaginary_index = round(math.sqrt(abs(r2 * r4)) / 10, 2)
    
    return r1, r2, r3, r4, imaginary_index

# 2. Обробник для текстових повідомлень (Онтологічний аналіз)
@dp.message()
async def analyze_text(message: types.Message):
    text = message.text
    r1, r2, r3, r4, i_index = calculate_nul_matrix(text)
    
    response = (
        "📐 **NUL-АНАЛІЗ СИГНАЛУ (Теорія Абсолюту):**\n\n"
        f"🔹 **R1 (Твердий Код / Сутність):** `{r1}%`\n"
        f"⚡ **R2 (Енергетичний Тригер):** `{r2}%`\n"
        f"⏳ **R3 (Часова Інерція):** `{r3}%`\n"
        f"🌫 **R4 (Маса / Ентропійний Осад):** `{r4}%`\n\n"
        f"🔮 **Оператор Сенсу (Мнима вісь $i$):** `{i_index}*i`\n"
        f"⚖ **Статичний Компенсатор ($\equiv$):** Потенційний баланс збережено.\n\n"
        "🔍 *Висновок системи:* Структурне редукування виконано за законами низькорівневої логіки."
    )
    
    await message.answer(response, parse_mode="Markdown")

# Простий вебсервер для Render
async def handle(request):
    return web.Response(text="NUL Mathematical Bot is alive and running!")

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
