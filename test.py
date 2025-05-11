import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

# Configura logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("BOT_TOKEN")  # Usa variables de entorno!

# --- Solución al conflicto ---
async def cleanup_previous_sessions():
    """Elimina webhooks y sesiones previas"""
    temp_bot = Bot(token=TOKEN)
    await temp_bot.delete_webhook(drop_pending_updates=True)
    await temp_bot.session.close()

# Configura bot con timeout extendido
bot = Bot(
    token=TOKEN,
    parse_mode=ParseMode.HTML,
    session_timeout=600  # 10 minutos
)
dp = Dispatcher(storage=MemoryStorage())

# Teclado
def build_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Записаться"), KeyboardButton(text="Тарифы")],
            [KeyboardButton(text="Оставить отзыв")]
        ],
        resize_keyboard=True
    )

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "👋 Привет! Я — бот разговорного испанского. Выбери действие ниже:",
        reply_markup=build_keyboard()
    )

@dp.message()
async def handle_message(message: types.Message):
    text = message.text.lower()
    if 'записаться' in text:
        await message.answer("📝 Форма для записи 👉 [tu_enlace]")
    elif 'тарифы' in text:
        await message.answer("💸 Тарифы:\n— 30 мин: 500 ₽\n— 5 уроков: 2000 ₽")
    elif 'отзыв' in text:
        await message.answer("🙏 Отзыв можно оставить здесь или по ссылке 👉 [tu_enlace]")
    else:
        await message.answer("Пожалуйста, выбери одну из кнопок ниже ⬇️")

async def main():
    # Limpieza inicial crítica
    await cleanup_previous_sessions()
    
    try:
        await dp.start_polling(
            bot,
            handle_signals=False,  # Evita conflictos con señales del sistema
            allowed_updates=dp.resolve_used_update_types(),
            close_bot_session=False  # Previene cierres abruptos
        )
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
if __name__ == "__main__":
    asyncio.run(main())
