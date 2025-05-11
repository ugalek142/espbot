import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

# --- Configuración básica ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("BOT_TOKEN")  # Usa variables de entorno!
if not TOKEN:
    logger.error("❌ No se encontró BOT_TOKEN")
    exit(1)

# --- Inicialización del bot ---
bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())

# --- Teclado interactivo ---
def build_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Записаться"), KeyboardButton(text="Тарифы")],
            [KeyboardButton(text="Оставить отзыв")]
        ],
        resize_keyboard=True,
        input_field_placeholder="Выберите действие..."
    )

# --- Manejadores ---
@dp.message(Command("start"))
async def start(message: types.Message):
    try:
        await message.answer(
            "👋 Привет! Я — бот разговорного испанского. Выбери действие ниже:",
            reply_markup=build_keyboard()
        )
    except Exception as e:
        logger.error(f"Error en start: {e}")

@dp.message()
async def handle_message(message: types.Message):
    try:
        text = message.text.lower()
        
        if 'записаться' in text:
            await message.answer(
                "📝 <b>Форма для записи:</b>\n"
                "👉 https://docs.google.com/forms/d/e/1FAIpQLSdR5Nvy8ltm1SyVvxCeh1NzhIvOr9kNr4C8anDu_I-cIPdHRA/viewform",
                parse_mode=ParseMode.HTML
            )
        elif 'тарифы' in text:
            await message.answer(
                "💵 <b>Наши тарифы:</b>\n\n"
                "• 30 минут: <b>500 ₽</b>\n"
                "• 5 уроков: <b>2000 ₽</b>\n"
                "• 10 уроков: <b>3500 ₽</b>",
                parse_mode=ParseMode.HTML
            )
        elif 'отзыв' in text:
            await message.answer(
                "📢 <b>Оставьте отзыв:</b>\n\n"
                "Напишите ваше мнение прямо здесь!",
                parse_mode=ParseMode.HTML
            )
        else:
            await message.answer(
                "Пожалуйста, выберите действие:",
                reply_markup=build_keyboard()
            )
            
    except Exception as e:
        logger.error(f"Error al manejar mensaje: {e}")

# --- Manejo de ciclo de vida ---
async def on_startup():
    await bot.delete_webhook(drop_pending_updates=True)
    logger.info("✅ Bot iniciado")

async def on_shutdown():
    await dp.storage.close()
    await bot.session.close()
    logger.info("❌ Bot detenido")

async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except Exception as e:
        logger.critical(f"Error crítico: {e}")
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
