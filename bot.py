import asyncio
import logging
import os
import re
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiohttp import web

TOKEN = os.getenv("BOT_TOKEN")

class NULSystemAnalyzer:
    def __init__(self, text: str):
        self.raw_text = text.upper()
        self.clean_text = re.sub(r'[^А-ЯІЇЄҐA-Z0-9\s]', '', self.raw_text)
        
        self.CYRILLIC_MATRIX = {
            'А': (0, 3, 2), 'Б': (1, 1, 1), 'В': (2, 2, 0), 'Г': (0, 2, 2),
            'Ґ': (0, 2, 4), 'Д': (0, 3, 4), 'Е': (0, 4, 3), 'Є': (1, 0, 3),
            'Ж': (0, 0, 6), 'З': (0, 2, 2), 'И': (0, 3, 2), 'І': (0, 0, 2),
            'Ї': (0, 0, 4), 'Й': (0, 1, 4), 'К': (0, 3, 4), 'Л': (0, 3, 2),
            'М': (0, 4, 2), 'Н': (0, 3, 4), 'О': (1, 0, 0), 'П': (0, 3, 2),
            'Р': (1, 1, 1), 'С': (1, 0, 1), 'Т': (0, 2, 3), 'У': (0, 2, 2),
            'Ф': (1, 2, 2), 'Х': (0, 4, 4), 'Ц': (0, 4, 3), 'Ч': (0, 3, 3),
            'Ш': (0, 4, 2), 'Щ': (0, 4, 3), 'Ь': (1, 1, 1), 'Ю': (1, 3, 2),
            'Я': (1, 2, 2)
        }
        self.LATIN_MATRIX = {
            'A': (0, 3, 2), 'B': (2, 1, 2), 'C': (1, 0, 1), 'D': (1, 1, 1),
            'E': (0, 4, 3), 'F': (0, 3, 3), 'G': (1, 1, 1), 'H': (0, 3, 4),
            'I': (0, 0, 2), 'J': (0, 1, 1), 'K': (0, 3, 4), 'L': (0, 2, 2),
            'M': (0, 4, 2), 'N': (0, 3, 2), 'O': (1, 0, 0), 'P': (1, 1, 1),
            'Q': (1, 0, 1), 'R': (1, 1, 1), 'S': (1, 0, 1), 'T': (0, 2, 2),
            'U': (0, 2, 2), 'V': (0, 2, 0), 'W': (0, 4, 0), 'X': (0, 4, 4),
            'Y': (0, 2, 1), 'Z': (0, 3, 2)
        }
        self.DIGITS_MATRIX = {
            '0': (1, 0, 0), '8': (2, 0, 0), '1': (0, 0, 2), '4': (0, 4, 1)
        }

    def compute_field(self):
        total_r1, total_r2, total_r3 = 0, 0, 0
        alpha_chars_count = 0

        for char in self.clean_text:
            if char.isspace():
                continue
            
            if char in self.CYRILLIC_MATRIX:
                vector = self.CYRILLIC_MATRIX[char]
            elif char in self.LATIN_MATRIX:
                vector = self.LATIN_MATRIX[char]
            elif char in self.DIGITS_MATRIX:
                vector = self.DIGITS_MATRIX[char]
            else:
                vector = (0, 0, 1) # Fallback
            
            total_r1 += vector[0]
            total_r2 += vector[1]
            total_r3 += vector[2]
            alpha_chars_count += 1

        total_sum = total_r1 + total_r2 + total_r3
        
        if total_sum > 0:
            pct_r1 = round((total_r1 / total_sum) * 100, 1)
            pct_r2 = round((total_r2 / total_sum) * 100, 1)
            pct_r3 = round((total_r3 / total_sum) * 100, 1)
        else:
            pct_r1 = pct_r2 = pct_r3 = 0.0

        # Коефіцієнт шлюзів (R3 / R1)
        k_exchange = round(total_r3 / (total_r1 + 1), 2)

        return {
            "total_chars": alpha_chars_count,
            "total_vector": (total_r1, total_r2, total_r3),
            "percentages": (pct_r1, pct_r2, pct_r3),
            "k_exchange": k_exchange
        }

dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("Вітаю! NUL Analytical Bot активовано. Надішліть текст або план для аналізу шарів R.")

@dp.message()
async def message_handler(message: types.Message):
    if not message.text:
        return

    analyzer = NULSystemAnalyzer(message.text)
    summary = analyzer.compute_field()

    if summary["total_chars"] == 0:
        await message.answer("Текст не містить розпізнаних символів абетки чи цифр.")
        return

    r1_sum, r2_sum, r3_sum = summary['total_vector']
    p1, p2, p3 = summary['percentages']
    k_ex = summary['k_exchange']

    # Логіка станів Абсолюту
    if k_ex > 1.0:
        state_desc = "Відкритий контур / Вимагає вкладання зовнішнього сенсу для замикання"
    else:
        state_desc = "Герметичний контур / Самодостатня структура"

    # Виключно зведена інформація по шарах R
    response = f"⚡ **АНАЛІЗ ШАРІВ NUL** ⚡\n\n"
    response += f"📊 **Опрацьовано знаків:** {summary['total_chars']}\n\n"
    response += f"--- **СУКУПНЕ ПОЛЕ СИСТЕМИ** ---\n"
    response += f"• **Сумарний вектор (R1, R2, R3):** ({r1_sum}, {r2_sum}, {r3_sum})\n"
    response += f"• **Енергетичний профіль:** R1 = {p1}% | R2 = {p2}% | R3 = {p3}%\n"
    response += f"• **Коефіцієнт шлюзів (K):** {k_ex}\n"
    response += f"• **Статус:** _{state_desc}_"

    await message.answer(response, parse_mode="Markdown")

async def handle(request):
    return web.Response(text="NUL Bot is active and running!")

async def start_web_server():
    app = web.Application()
    app.add_routes([web.get('/', handle)])
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    print(f"Вебсервер запущено на порту {port}")

async def main():
    bot = Bot(token=TOKEN)
    await start_web_server()
    print("Бот запущено і готовий до роботи...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
