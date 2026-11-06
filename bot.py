import asyncio
import math
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

# Читання токена безпечно зі змінних середовища хмари
TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()


class ForecastState(StatesGroup):
  waiting_for_event = State()


def calculate_nul_forecast(event_text: str):
  words = event_text.split()
  r1_code = len(words) * 1.2
  r4_mass = len(event_text)

  if r4_mass == 0:
    k_tr = 0
  else:
    k_tr = min(round((r1_code / r4_mass) * 15, 2), 1.0)

  impulse_words = ["злам", "старт", "прорив", "криза", "рішення", "не"]
  r2_energy = (
      sum(1 for word in impulse_words if word in event_text.lower()) * 8 + 12
  )
  r3_duration = round(math.sqrt(r1_code * r2_energy), 2)

  return {
      "transparency": k_tr,
      "energy": r2_energy,
      "duration_shadow": r3_duration,
  }


@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
  await message.answer(
      "Систему НУЛ активовано. Інтерфейс ЯR підключено.\n\nВведіть опис події"
      " для структурного аналізу:"
  )
  await state.set_state(ForecastState.waiting_for_event)


@dp.message(ForecastState.waiting_for_event)
async def process_forecast(message: types.Message, state: FSMContext):
  metrics = calculate_nul_forecast(message.text)

  if metrics["transparency"] > 0.4:
    conclusion = (
        "Система має високу прозорість. Перехід можливий через точку НЕ"
        " (Старт)."
    )
  else:
    conclusion = (
        "Система перевантажена ентропійним осадом (R4). Потрібне очищення від"
        " шуму."
    )

  response = (
      f"--- СТРУКТУРНИЙ ПРОГНОЗ ПОДІЇ ---\n\n"
      f"Вхідний сигнал: {message.text}\n\n"
      f"Коефіцієнт прозорості (K_tr): {metrics['transparency']}\n"
      f"Енергетичний потенціал (R2): {metrics['energy']}\n"
      f"Тінь сили / Тривалість (R3): {metrics['duration_shadow']}\n\n"
      f"Висновок Оператора: {conclusion}"
  )

  await message.answer(response)
  await state.clear()


async def main():
  await dp.start_polling(bot)


if __name__ == "__main__":
  asyncio.run(main())
