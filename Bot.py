import logging
import json
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton

# --- SOZLAMALAR ---
TOKEN = "8361228448:AAF1x3Y87Q0vmAEs_Dp9xnJNWGJdJYCyfsg"
WEB_APP_URL = "https://mir2255.github.io/My_stars_bot/"
# ------------------

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    # Asosiy klaviatura
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="O'yinni boshlash 🎮", web_app=WebAppInfo(url=WEB_APP_URL))]
    ])
    
    welcome_text = (
        f"Salom, {message.from_user.first_name}! 👋\n\n"
        "TapSwap uslubidagi o'yinimizga xush kelibsiz!\n"
        "Tanga yig'ish va do'kondan foydalanish uchun pastdagi tugmani bosing."
    )
    
    await message.answer(welcome_text, reply_markup=kb)

@dp.message(F.web_app_data)
async def web_app_data_handler(message: types.Message):
    # Web App'dan kelgan JSON ma'lumotni o'qiymiz
    try:
        data = json.loads(message.web_app_data.data)
        
        action = data.get("action")
        item_type = data.get("type")
        new_lvl = data.get("new_level")
        balance = data.get("balance")
        
        if action == "buy":
            msg = (
                "✅ **Xarid muvaffaqiyatli yakunlandi!**\n\n"
                f"🛒 Buyum: {item_type.capitalize()}\n"
                f"🆙 Yangi daraja: {new_lvl}\n"
                f"💰 Qolgan balans: {balance} tanga"
            )
            await message.answer(msg, parse_mode="Markdown")
            
    except Exception as e:
        logging.error(f"Xatolik yuz berdi: {e}")
        await message.answer("Xarid ma'lumotlarini qabul qilishda xatolik yuz berdi.")

async def main():
    logging.basicConfig(level=logging.INFO)
    print("Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
