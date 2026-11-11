import asyncio
import logging
import math
import os
import re
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiohttp import web

TOKEN = os.getenv("BOT_TOKEN")

class NULAbsoluteAnalyzer:
    def __init__(self, text: str):
        self.raw_text = text.upper()
        self.clean_text = re.sub(r'[^А-ЯІЇЄҐA-Z0-9\s]', '', self.raw_text)
        
        # Топологічна матриця НУЛ: (Сфера/R1_контур, Розірваний шлюз, Ортогональний каркас R2, Векторний прорив R3)
        self.CYRILLIC_MATRIX = {
            'А': (0, 0, 1, 3), 'Б': (1, 1, 1, 1), 'В': (2, 0, 2, 0), 'Г': (0, 0, 2, 1),
            'Ґ': (0, 0, 2, 2), 'Д': (0, 0, 3, 2), 'Е': (0, 0, 4, 2), 'Є': (1, 1, 1, 1),
            'Ж': (0, 0, 0, 6), 'З': (0, 2, 0, 1), 'И': (0, 0, 2, 3), 'І': (0, 0, 2, 0),
            'Ї': (0, 0, 2, 2), 'Й': (0, 0, 3, 2), 'К': (0, 0, 3, 3), 'Л': (0, 0, 3, 1),
            'М': (0, 0, 2, 4), 'Н': (0, 0, 4, 1), 'О': (1, 0, 0, 0), 'П': (0, 0, 3, 1),
            'Р': (1, 1, 1, 0), 'С': (1, 1, 0, 0), 'Т': (0, 0, 3, 1), 'У': (0, 0, 1, 3),
            'Ф': (1, 0, 2, 2), 'Х': (0, 0, 2, 4), 'Ц': (0, 0, 4, 2), 'Ч': (0, 0, 3, 2),
            'Ш': (0, 0, 4, 2), 'Щ': (0, 0, 4, 3), 'Ь': (1, 1, 1, 0), 'Ю': (1, 0, 2, 2),
            'Я': (1, 0, 2, 1)
        }
        self.LATIN_MATRIX = {
            'A': (0, 0, 1, 3), 'B': (2, 1, 1, 1), 'C': (1, 1, 0, 0), 'D': (1, 1, 1, 0),
            'E': (0, 0, 4, 2), 'F': (0, 0, 3, 2), 'G': (1, 1, 1, 0), 'H': (0, 0, 4, 1),
            'I': (0, 0, 2, 0), 'J': (0, 1, 1, 0), 'K': (0, 0, 3, 3), 'L': (0, 0, 2, 1),
            'M': (0, 0, 2, 4), 'N': (0, 0, 3, 2), 'O': (1, 0, 0, 0), 'P': (1, 1, 1, 0),
            'Q': (1, 1, 0, 0), 'R': (1, 1, 1, 0), 'S': (1, 1, 0, 0), 'T': (0, 0, 2, 1),
            'U': (0, 2, 0, 1), 'V': (0, 0, 0, 3), 'W': (0, 0, 0, 5), 'X': (0, 0, 0, 4),
            'Y': (0, 0, 1, 2), 'Z': (0, 0, 3, 2)
        }
        self.DIGITS_MATRIX = {
            '0': (1, 0, 0, 0), '8': (2, 0, 0, 0), '1': (0, 0, 2, 0), '4': (0, 0, 2, 2)
        }

    def compute_field(self):
        t_sphere, t_open, t_square, t_vector = 0, 0, 0, 0
        alpha_chars_count = 0

        for char in self.clean_text:
            if char.isspace():
                continue
            
            if char in self.CYRILLIC_MATRIX:
                vec = self.CYRILLIC_MATRIX[char]
            elif char in self.LATIN_MATRIX:
                vec = self.LATIN_MATRIX[char]
            elif char in self.DIGITS_MATRIX:
                vec = self.DIGITS_MATRIX[char]
            else:
                vec = (0, 0, 1, 1)
            
            t_sphere += vec[0]
            t_open += vec[1]
            t_square += vec[2]
            t_vector += vec[3]
            alpha_chars_count += 1

        total_sum = t_sphere + t_open + t_square + t_vector
        
        if total_sum > 0:
            pct_sphere = round((t_sphere / total_sum) * 100, 1)
            pct_open = round((t_open / total_sum) * 100, 1)
            pct_square = round((t_square / total_sum) * 100, 1)
            pct_vector = round((t_vector / total_sum) * 100, 1)
        else:
            pct_sphere = pct_open = pct_square = pct_vector = 0.0

        # --- НОВА МАТЕМАТИЧНА МОДЕЛЬ НУЛ ---
        # 1. Коефіцієнт шлюзів ( K ) враховує як відкриті кола, так і векторні прориви відносно каркаса
        k_exchange = (t_open + t_vector) / (t_square + 1)

        # 2. Мнимий оператор сенсу i
        i_sense = round(math.sqrt(k_exchange), 3)

        # 3. Матеріальна цегла / осад R4 = i^2
        r4_matter = round(k_exchange, 2)

        # 4. Необхідна напруга свідомості R5 (компенсація ентропії каркаса)
        entropy_s = (t_square / (t_sphere + t_open + 1)) if t_sphere > 0 else 1.0
        r5_compensation = round(i_sense / (entropy_s + 1e-5), 3)

        # 5. Реліктовий енергетичний вплив тексту R1_impact
        r1_impact = round((t_open * t_vector) / (t_square + 0.001), 2)

        return {
            "total_chars": alpha_chars_count,
            "vector": (t_sphere, t_open, t_square, t_vector),
            "percentages": (pct_sphere, pct_open, pct_square, pct_vector),
            "k_exchange": round(k_exchange, 2),
            "i_sense": i_sense,
            "r4_matter": r4_matter,
            "r5_compensation": r5_compensation,
            "r1_impact": r1_impact
        }

dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("Вітаю! NUL Relic Spectral Analyzer активовано. Надішліть текст для розрахунку геометрії шлюзів, мнимого сенсу та енергетичного впливу R1.")

@dp.message()
async def message_handler(message: types.Message):
    if not message.text:
        return

    analyzer = NULAbsoluteAnalyzer(message.text)
    summary = analyzer.compute_field()

    if summary["total_chars"] == 0:
        await message.answer("Текст не містить розпізнаних символів абетки чи цифр.")
        return

    s_sum, o_sum, sq_sum, v_sum = summary['vector']
    p1, p2, p3, p4 = summary['percentages']
    k_ex = summary['k_exchange']
    i_s = summary['i_sense']
    r4_m = summary['r4_matter']
    r5_c = summary['r5_compensation']
    r1_imp = summary['r1_impact']

    if r1_imp > 2.5:
        status = "Живий трансцендентний вихор / Висока провідність істини"
    elif r1_imp >= 1.0:
        status = "Відігранований кристал / Ідеальний баланс каркаса та шлюзів"
    else:
        status = "Мертвий ентропійний шар / Залізобетонна догма"

    response = f"⚡ **СПЕКТРАЛЬНИЙ АНАЛІЗ NUL** ⚡\n\n"
    response += f"📊 **Опрацьовано знаків:** {summary['total_chars']}\n\n"
    
    response += f"--- **ТОПОЛОГІЧНИЙ ПРОФІЛЬ ФОРМИ** ---\n"
    response += f"• **Сферичні контури (кола):** {s_sum} ({p1}%)\n"
    response += f"• **Розірвані шлюзи (портали):** {o_sum} ({p2}%)\n"
    response += f"• **Ортогональні каркаси (прямі):** {sq_sum} ({p3}%)\n"
    response += f"• **Векторні прориви (кути):** {v_sum} ({p4}%)\n"
    response += f"• **Коефіцієнт шлюзів (K):** {k_ex}\n\n"
    
    response += f"--- **МАТЕМАТИКА АБСОЛЮТУ** ---\n"
    response += f"• **Мнимий оператор сенсу (i):** {i_s} i\n"
    response += f"• **Матеріальний осад (R4 = i^2):** {r4_m}\n"
    response += f"• **Необхідна напруга свідомості (R5):** {r5_c}\n"
    response += f"• **Енергетичний вплив (R1_impact):** {r1_imp}\n\n"
    
    response += f"• **Статус структури:** _{status}_"

    await message.answer(response, parse_mode="Markdown")

async def handle(request):
    return web.Response(text="NUL Relic Analyzer Bot is active and running!")

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
