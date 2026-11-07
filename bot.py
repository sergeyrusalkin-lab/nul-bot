import asyncio
import logging
import re
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# Вставте сюди ваш токен Telegram-бота
import os
TOKEN = os.getenv("BOT_TOKEN")

# Клас первинної векторної матриці
class NULPrimaryVectorIsolator:
    def __init__(self, text: str):
        self.clean_text = re.sub(r'[^А-ЯІЇЄҐA-Z0-9]', '', text.upper())
        
        # Кирилична матриця
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
        
        # Латинська матриця
        self.LATIN_MATRIX = {
            'A': (0, 3, 2), 'B': (2, 1, 2), 'C': (1, 0, 1), 'D': (1, 1, 1),
            'E': (0, 4, 3), 'F': (0, 3, 3), 'G': (1, 1, 1), 'H': (0, 3, 4),
            'I': (0, 0, 2), 'J': (0, 1, 1), 'K': (0, 3, 4), 'L': (0, 2, 2),
            'M': (0, 4, 2), 'N': (0, 3, 2), 'O': (1, 0, 0), 'P': (1, 1, 1),
            'Q': (1, 0, 1), 'R': (1, 1, 1), 'S': (1, 0, 1), 'T': (0, 2, 2),
            'U': (0, 2, 2), 'V': (0, 2, 0), 'W': (0, 4, 0), 'X': (0, 4, 4),
            'Y': (0, 2, 1), 'Z': (0, 3, 2)
        }

        # Цифри
        self.DIGITS_MATRIX = {
            '0': (1, 0, 0), '8': (2, 0, 0), '1': (0, 0, 2), '4': (0, 4, 1)
        }

    def extract_primary_vectors(self):
        breakdown = []
        for char in self.clean_text:
            if char in self.CYRILLIC_MATRIX:
                vector = self.CYRILLIC_MATRIX[char]
            elif char in self.LATIN_MATRIX:
                vector = self.LATIN_MATRIX[char]
            elif char in self.DIGITS_MATRIX:
                vector = self.DIGITS_MATRIX[char]
            else:
                vector = (0, 0, 1)
            breakdown.append({"char": char, "vector": vector})
        return self.clean_text, breakdown

# Ініціалізація диспетчера
dp = Dispatcher()

# Правильні декоратори для обробників у aiogram 3.x
@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("Вітаю! Надішліть слово або текст, і я розкладу його на первинні вектори (R1, R2, R3).")

@dp.message()
async def message_handler(message: types.Message):
    if not message.text:
        return
        
    isolator = NULPrimaryVectorIsolator(message.text)
    clean_text, breakdown = isolator.extract_primary_vectors()
    
    if not clean_text:
        await message.answer("Текст не містить розпізнаних символів (кирилиця/латиниця).")
        return
        
    response = f"Очищений текст: {clean_text}\nПервинні вектори:\n"
    for item in breakdown:
        response += f"'{item['char']}' -> {item['vector']}\n"
        
    await message.answer(response)

async def main():
    bot = Bot(token=TOKEN)
    print("Бот запущено і готовий до роботи...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
