import logging
import sqlite3
import json
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, CommandObject
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton, LabeledPrice

TOKEN = "8361228448:AAF1x3Y87Q0vmAEs_Dp9xnJNWGJdJYCyfsg"
WEB_APP_URL = "https://mir2255.github.io/My_stars_bot/"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# DATABASE - Ma'lumotlarni saqlash
def get_db():
    conn = sqlite3.connect("users.db")
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            balance INTEGER DEFAULT 0,
            energy INTEGER DEFAULT 500,
            referrer_id INTEGER,
            has_bot INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

init_db()

@dp.message(Command("start"))
async def start_handler(message: types.Message, command: CommandObject):
    user_id = message.from_user.id
    args = command.args # Referal ID shu yerda keladi
    
    conn = get_db()
    cursor = conn.cursor()
    user = cursor.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,)).fetchone()
    
    if not user:
        ref_id = None
        if args and args.isdigit() and int(args) != user_id:
            ref_id = int(args)
            # Taklif qilganga 5000 bonus
            cursor.execute("UPDATE users SET balance = balance + 5000 WHERE user_id = ?", (ref_id,))
            try:
                await bot.send_message(ref_id, "🎁 Do'stingiz qo'shildi! Sizga 5000 tanga berildi.")
            except: pass
        
        cursor.execute("INSERT INTO users (user_id, referrer_id, balance) VALUES (?, ?, ?)", (user_id, ref_id, 0))
        conn.commit()
    
    current_balance = user[0] if user else 0
    conn.close()

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="O'yinni boshlash 🎮", web_app=WebAppInfo(url=WEB_APP_URL))],
        [InlineKeyboardButton(text="Do'stlarni taklif qilish 👥", switch_inline_query=f"\nDo'stim, mana bu o'yinni o'yna va 5000 bonus ol: https://t.me/{(await bot.get_me()).username}?start={user_id}")]
    ])
    
    await message.answer(f"Salom! Balansingiz: {current_balance} 💰\nO'yinni boshlash uchun bosing:", reply_markup=kb)

# Web App'dan kelgan ma'lumotlarni bazaga yozish
@dp.message(F.web_app_data)
async def handle_webapp_data(message: types.Message):
    data = json.loads(message.web_app_data.data)
    user_id = message.from_user.id
    
    if data.get("action") == "sync":
        conn = get_db()
        conn.execute("UPDATE users SET balance = ?, energy = ? WHERE user_id = ?", 
                     (data['coins'], data['energy'], user_id))
        conn.commit()
        conn.close()
        
    if data.get("action") == "buy_bot":
        # Telegram Stars Invoysi
        await message.answer_invoice(
            title="TapBot Activator",
            description="24 soatlik avto-kliker",
            prices=[LabeledPrice(label="TapBot", amount=20)],
            payload="bot_purchase",
            currency="XTR",
            provider_token="" # Stars uchun bo'sh bo'lishi shart
        )

@dp.pre_checkout_query()
async def pre_checkout(query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(query.id, ok=True)

@dp.message(F.successful_payment)
async def on_success_pay(message: types.Message):
    conn = get_db()
    conn.execute("UPDATE users SET has_bot = 1 WHERE user_id = ?", (message.from_user.id,))
    conn.commit()
    conn.close()
    await message.answer("✅ To'lov qabul qilindi! Robotingiz faollashdi.")

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
