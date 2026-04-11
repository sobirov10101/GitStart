import asyncio
import os
import logging
from dotenv import load_dotenv
 
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart, Command
 
from deep_translator import GoogleTranslator
 
# .env fayldan tokenni olish
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
 
# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
 
# Bot va Dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher()
 
# Har bir foydalanuvchining rejimini saqlash
user_mode = {}  # {user_id: "en-uz" yoki "uz-en"}
 
 
def main_keyboard():
    """Asosiy tugmalar"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇬🇧 Ingliz → O'zbek", callback_data="en-uz")],
        [InlineKeyboardButton(text="🇺🇿 O'zbek → Ingliz", callback_data="uz-en")],
    ])
    return keyboard
 
 
@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        "👋 *Salom! Men Tarjimon Botman!*\n\n"
        "Quyidagi tugmalardan birini tanlang:\n\n"
        "🇬🇧 *Ingliz → O'zbek* — inglizcha matnni o'zbekchaga tarjima qiladi\n"
        "🇺🇿 *O'zbek → Ingliz* — o'zbekcha matnni inglizchaga tarjima qiladi",
        parse_mode="Markdown",
        reply_markup=main_keyboard()
    )
 
 
@dp.message(Command("help"))
async def help_handler(message: Message):
    await message.answer(
        "ℹ️ *Yordam*\n\n"
        "Bu bot matnlarni tarjima qilishga yordam beradi.\n\n"
        "*Buyruqlar:*\n"
        "/start — Botni ishga tushirish\n"
        "/help — Yordam\n\n"
        "*Foydalanish:*\n"
        "1. Tugmalardan birini tanlang\n"
        "2. Matn yuboring\n"
        "3. Tarjimani oling ✅",
        parse_mode="Markdown",
        reply_markup=main_keyboard()
    )
 
 
@dp.callback_query(F.data.in_({"en-uz", "uz-en"}))
async def mode_handler(callback: CallbackQuery):
    user_id = callback.from_user.id
    mode = callback.data
    user_mode[user_id] = mode
 
    if mode == "en-uz":
        text = (
            "✅ *Ingliz → O'zbek* rejimi tanlandi!\n\n"
            "📝 Endi inglizcha matn yuboring."
        )
    else:
        text = (
            "✅ *O'zbek → Ingliz* rejimi tanlandi!\n\n"
            "📝 Endi o'zbekcha matn yuboring."
        )
 
    await callback.message.edit_text(
        text=text,
        parse_mode="Markdown",
        reply_markup=main_keyboard()
    )
    await callback.answer()
 
 
@dp.message(F.text)
async def translate_handler(message: Message):
    user_id = message.from_user.id
    text = message.text
 
    # Rejim tanlanmagan bo'lsa
    if user_id not in user_mode:
        await message.answer(
            "⚠️ Avval tarjima yo'nalishini tanlang:",
            reply_markup=main_keyboard()
        )
        return
 
    mode = user_mode[user_id]
 
    try:
        if mode == "en-uz":
            translated = GoogleTranslator(source="en", target="uz").translate(text)
            flag_from, flag_to = "🇬🇧", "🇺🇿"
            lang_from, lang_to = "Inglizcha", "O'zbekcha"
        else:
            translated = GoogleTranslator(source="uz", target="en").translate(text)
            flag_from, flag_to = "🇺🇿", "🇬🇧"
            lang_from, lang_to = "O'zbekcha", "Inglizcha"
 
        response = (
            f"{flag_from} *{lang_from}:*\n{text}\n\n"
            f"{flag_to} *{lang_to}:*\n{translated}"
        )
 
        await message.answer(
            response,
            parse_mode="Markdown",
            reply_markup=main_keyboard()
        )
 
    except Exception as e:
        logger.error(f"Tarjima xatosi: {e}")
        await message.answer("❌ Xatolik yuz berdi. Qayta urinib ko'ring.")
 
 
async def main():
    logger.info("Bot ishga tushdi...")
    await dp.start_polling(bot)
 
 
if __name__ == "__main__":
    asyncio.run(main())
