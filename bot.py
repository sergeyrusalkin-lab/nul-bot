import os
import asyncio
import logging
import math
import re
from collections import Counter
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiohttp import web

TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()


# ====================== НУЛ-МАТЕМАТИЧНИЙ АПАРАТ ======================

def calculate_nul_matrix(text: str):
    """
    Покращена реалізація математичного апарату Глави III.
    Повертає: r1, r2, r3, r4, i_index, ten_power, compensator, interpretation
    """
    text = text.strip()
    length = len(text)
    
    if length < 5:
        return 25.0, 25.0, 25.0, 25.0, 0.5, 0.0, 50.0, "Текст занадто короткий для аналізу."

    words = re.findall(r'\b\w+\b', text.lower())
    word_count = max(1, len(words))
    sentences = re.split(r'[.!?]+', text)
    sentence_count = max(1, len([s for s in sentences if s.strip()]))

    # ---------- R1: Структурна щільність / Твердий код (каркас) ----------
    unique_chars_ratio = len(set(text)) / length
    unique_words_ratio = len(set(words)) / word_count
    avg_word_len = sum(len(w) for w in words) / word_count
    punctuation_density = (text.count('.') + text.count(',') + text.count(';') + text.count(':')) / length * 100

    r1_raw = (
        unique_words_ratio * 45 +
        min(unique_chars_ratio * 80, 25) +
        min(avg_word_len * 3.5, 20) +
        min(punctuation_density * 1.8, 15)
    )
    r1_raw = max(12.0, min(78.0, r1_raw))

    # ---------- R2: Енергетичний тригер / Потенціал ----------
    exclam = text.count('!')
    questions = text.count('?')
    long_words = sum(1 for w in words if len(w) > 7)
    intense_words = sum(1 for w in words if w in {
        'критично', 'негайно', 'обов', 'потрібно', 'важливо', 'катастрофа',
        'прорив', 'загроза', 'сила', 'тиск', 'напруга', 'вибух', 'пік',
        'must', 'urgent', 'critical', 'now', 'force', 'power'
    })
    caps_ratio = sum(1 for c in text if c.isupper()) / max(1, length) * 100

    r2_raw = (
        (exclam * 8) +
        (questions * 5) +
        (long_words / word_count * 35) +
        (intense_words * 6) +
        min(caps_ratio * 1.2, 18)
    )
    r2_raw = max(8.0, min(65.0, r2_raw))

    # ---------- R3: Часова інерція / Процес ----------
    avg_sentence_len = word_count / sentence_count
    repetition = 1.0 - unique_words_ratio
    r3_raw = (
        min(avg_sentence_len * 2.2, 35) +
        (repetition * 40) +
        max(0, 25 - r2_raw * 0.25)
    )
    r3_raw = max(8.0, min(55.0, r3_raw))

    # ---------- R4: Ентропійний / Матеріальний осад ----------
    # Чим більше "води", розмитості і шуму — тим вищий R4
    filler_ratio = sum(1 for w in words if w in {
        'дуже', 'просто', 'насправді', 'взагалі', 'типу', 'якось',
        'somehow', 'really', 'just', 'actually', 'basically'
    }) / word_count
    r4_raw = (
        (1 - unique_words_ratio) * 35 +
        filler_ratio * 50 +
        max(0, 40 - r1_raw * 0.4) +
        max(0, 25 - r2_raw * 0.2)
    )
    r4_raw = max(8.0, min(60.0, r4_raw))

    # ---------- Нормалізація до 100% ----------
    total = r1_raw + r2_raw + r3_raw + r4_raw
    r1 = round((r1_raw / total) * 100, 1)
    r2 = round((r2_raw / total) * 100, 1)
    r3 = round((r3_raw / total) * 100, 1)
    r4 = round((r4_raw / total) * 100, 1)

    # ---------- Оператор сенсу i (ближче до теорії) ----------
    # i виникає з напруги між енергією і осадом (R2 і R4)
    i_index = round(math.sqrt(abs(r2 * r4)) / 12.5, 2)

    # ---------- ТЕН (Точка Екстремальної Напруги) ----------
    # Високий ТЕН = сильний розрив між структурою і енергією + висока напруга
    tension = abs(r1 - r2) * 0.6 + abs(r2 - r4) * 0.4 + (r2 * 0.35)
    ten_power = round(min(100.0, tension), 1)

    # ---------- Компенсатор (наскільки добре виконується AR ≈ RA) ----------
    # Ідеальний баланс ближчий до 50
    balance_diff = abs(r1 - r4) + abs(r2 - r3) * 0.7
    compensator = round(max(0.0, 100.0 - balance_diff * 1.1), 1)

    # ---------- Інтерпретація ----------
    interpretation = generate_interpretation(r1, r2, r3, r4, i_index, ten_power, compensator)

    return r1, r2, r3, r4, i_index, ten_power, compensator, interpretation


def generate_interpretation(r1, r2, r3, r4, i, ten, comp):
    """Розумна інтерпретація результатів згідно з логікою теорії"""
    
    dominant = max(
        ("R1 (Структура)", r1),
        ("R2 (Енергія)", r2),
        ("R3 (Інерція)", r3),
        ("R4 (Осад)", r4),
        key=lambda x: x[1]
    )[0]

    lines = []

    # Основний характер тексту
    if r1 >= 32 and r2 < 22:
        lines.append("• Текст має сильний структурний каркас (високий R1). Сенс відносно стабільний.")
    elif r2 >= 30:
        lines.append("• Висока енергетична напруга (R2). Текст тисне, провокує, вимагає реакції.")
    elif r4 >= 30:
        lines.append("• Значний ентропійний осад (R4). Багато «матерії» і шуму, сенс розмитий.")
    elif r3 >= 28:
        lines.append("• Висока інерція процесу (R3). Текст важкий, повільний, з великою часовою масою.")

    # ТЕН
    if ten >= 55:
        lines.append(f"• **ТЕН сильний** ({ten}). Точка екстремальної напруги активна — система близька до трансформації.")
    elif ten >= 35:
        lines.append(f"• ТЕН помірний ({ten}). Є напруга, але вона ще не критична.")
    else:
        lines.append(f"• ТЕН слабкий ({ten}). Система відносно врівноважена.")

    # Компенсатор
    if comp >= 70:
        lines.append(f"• Компенсатор високий ({comp}%). Принцип AR ≈ RA виконується добре.")
    elif comp >= 45:
        lines.append(f"• Компенсатор середній ({comp}%). Баланс частковий.")
    else:
        lines.append(f"• Компенсатор низький ({comp}%). Сильний дисбаланс між проявом і зворотним боком.")

    # Оператор сенсу
    if i >= 4.5:
        lines.append(f"• Оператор сенсу **i = {i}** високий. Текст несе сильний заряд значення.")
    elif i >= 2.8:
        lines.append(f"• Оператор сенсу i = {i} помірний.")
    else:
        lines.append(f"• Оператор сенсу i = {i} низький. Сенс слабко проявлений.")

    # Домінанта
    lines.append(f"• Домінуючий шар: **{dominant}**")

    return "\n".join(lines)


# ====================== ОБРОБНИКИ ======================

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "⚡ **NUL-Онтологічний Сканер v2** активований.\n\n"
        "Математичне ядро «Теорія Абсолюту» (Глава III) завантажено.\n\n"
        "Надішли будь-який текст, і я розрахую:\n"
        "• R1–R4\n"
        "• Оператор сенсу **i**\n"
        "• Силу **ТЕНу**\n"
        "• Якість **Компенсатора**\n"
        "• Інтерпретацію згідно з низькорівневою логікою\n\n"
        "Команди: /start • /help",
        parse_mode="Markdown"
    )


@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(
        "📖 **Довідка NUL-Сканера**\n\n"
        "**R1** — Структурний каркас / Твердий код\n"
        "**R2** — Енергетичний тригер / Потенціал\n"
        "**R3** — Часова інерція / Процес\n"
        "**R4** — Ентропійний осад / Матерія\n\n"
        "**i** — Оператор сенсу (мнима вісь)\n"
        "**ТЕН** — Точка Екстремальної Напруги\n"
        "**Компенсатор** — наскільки добре виконується принцип AR(1) ≈ RA(-1)\n\n"
        "Просто надішли текст для аналізу.",
        parse_mode="Markdown"
    )


@dp.message()
async def analyze_text(message: types.Message):
    text = message.text
    if not text or text.startswith('/'):
        return

    r1, r2, r3, r4, i_index, ten, comp, interpretation = calculate_nul_matrix(text)

    response = (
        "📐 **NUL-АНАЛІЗ СИГНАЛУ**\n"
        "*(Теорія Абсолюту • Глава III)*\n\n"
        f"🔹 **R1 (Структура / Каркас):** `{r1}%`\n"
        f"⚡ **R2 (Енергія / Тригер):** `{r2}%`\n"
        f"⏳ **R3 (Інерція / Процес):** `{r3}%`\n"
        f"🌫 **R4 (Осад / Матерія):** `{r4}%`\n\n"
        f"🔮 **Оператор сенсу i:** `{i_index}·i`\n"
        f"💥 **ТЕН (напруга):** `{ten}`\n"
        f"⚖ **Компенсатор:** `{comp}%`\n\n"
        f"**Інтерпретація:**\n{interpretation}"
    )

    await message.answer(response, parse_mode="Markdown")


# ====================== ВЕБСЕРВЕР ДЛЯ RENDER ======================

async def handle(request):
    return web.Response(text="NUL Mathematical Bot v2 is alive")

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
