import logging
import sqlite3
import json
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton, LabeledPrice

TOKEN = "8361228448:AAF1x3Y87Q0vmAEs_Dp9xnJNWGJdJYCyfsg"
WEB_APP_URL = "https://mir2255.github.io/My_stars_bot/"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- DATABASE SOZLAMALARI ---
def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            balance INTEGER DEFAULT 0,
            energy INTEGER DEFAULT 500,
            league TEXT DEFAULT 'Mis',
            has_bot INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

init_db()

def update_user(user_id, balance, energy):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
    cursor.execute("UPDATE users SET balance = ?, energy = ? WHERE user_id = ?", (balance, energy, user_id))
    conn.commit()
    conn.close()

# --- BOT BUYRUQLARI ---
@dp.message(Command("start"))
async def start(message: types.Message):
    user_id = message.from_user.id
    
    # Bazada bormi tekshirish
    conn = sqlite3.connect("users.db")
    user = conn.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,)).fetchone()
    conn.close()
    
    msg = "Salom! TapSwap botingiz tayyor.\n\n"
    if user:
        msg += f"Sizning balansingiz: {user[0]} tanga 💰"
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="O'yinni ochish 🎮", web_app=WebAppInfo(url=WEB_APP_URL))],
        [InlineKeyboardButton(text="Do'stlarni taklif qilish 👥", switch_inline_query=f"\nDo'stim, mana link: https://t.me/{(await bot.get_me()).username}?start={user_id}")]
    ])
    await message.answer(msg, reply_markup=kb)

@dp.message(F.web_app_data)
async def handle_data(message: types.Message):
    data = json.loads(message.web_app_data.data)
    user_id = message.from_user.id
    
    if data['action'] == "sync":
        update_user(user_id, data['coins'], data['energy'])
        
    if data['action'] == "buy_bot":
        await bot.send_invoice(
            chat_id=message.chat.id,
            title="TapBot",
            description="Avtomatik bosuvchi robot",
            payload="bot_pay",
            currency="XTR",
            prices=[LabeledPrice(label="Robot", amount=20)]
        )

@dp.pre_checkout_query()
async def checkout(query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(query.id, ok=True)

@dp.message(F.successful_payment)
async def success(message: types.Message):
    conn = sqlite3.connect("users.db")
    conn.execute("UPDATE users SET has_bot = 1 WHERE user_id = ?", (message.from_user.id,))
    conn.commit()
    conn.close()
    await message.answer("✅ Rahmat! TapBot faollashdi. Yulduzchalar hisobingizga tushdi.")

if __name__ == "__main__":
    import asyncio
    async def main():
        logging.basicConfig(level=logging.INFO)
        await dp.start_polling(bot)
    asyncio.run(main())
