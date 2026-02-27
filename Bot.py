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

# --- DATABASE ---
def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            balance INTEGER DEFAULT 0,
            energy INTEGER DEFAULT 500,
            has_bot INTEGER DEFAULT 0,
            referrer_id INTEGER
        )
    """)
    conn.commit()
    conn.close()

init_db()

# --- REFERAL VA START ---
@dp.message(Command("start"))
async def start(message: types.Message, command: CommandObject):
    user_id = message.from_user.id
    args = command.args # Referal ID shu yerda keladi

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    user = cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,)).fetchone()

    if not user:
        # Yangi foydalanuvchi
        ref_id = int(args) if args and args.isdigit() else None
        cursor.execute("INSERT INTO users (user_id, referrer_id, balance) VALUES (?, ?, ?)", (user_id, ref_id, 0))
        
        # Taklif qilganga 5000 bonus
        if ref_id:
            cursor.execute("UPDATE users SET balance = balance + 5000 WHERE user_id = ?", (ref_id,))
            try:
                await bot.send_message(ref_id, "🎉 Siz taklif qilgan do'stingiz qo'shildi! +5000 tanga.")
            except: pass
        conn.commit()

    conn.close()
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="O'yinni boshlash 🎮", web_app=WebAppInfo(url=WEB_APP_URL))],
        [InlineKeyboardButton(text="Do'stlarni taklif qilish 👥", switch_inline_query=f"\nDo'stim, mana bu ajoyib o'yin! Kir va 5000 bonus ol:")]
    ])
    await message.answer("O'yin yangilandi! Endi referal va to'lovlar 100% ishlaydi.", reply_markup=kb)

# --- STARS TO'LOVI ---
@dp.message(F.web_app_data)
async def handle_shop(message: types.Message):
    data = json.loads(message.web_app_data.data)
    
    if data['action'] == "buy_bot":
        # Invoice yuborish
        await message.answer_invoice(
            title="TapBot Activator",
            description="24/7 Avtomatik bosish roboti",
            prices=[LabeledPrice(label="TapBot", amount=20)], # 20 Stars
            provider_token="", # Stars uchun bo'sh qoladi
            payload="activate_bot",
            currency="XTR"
        )

@dp.pre_checkout_query()
async def process_pre_checkout(query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(query.id, ok=True)

@dp.message(F.successful_payment)
async def success_payment(message: types.Message):
    conn = sqlite3.connect("users.db")
    conn.execute("UPDATE users SET has_bot = 1 WHERE user_id = ?", (message.from_user.id,))
    conn.commit()
    conn.close()
    await message.answer("✅ To'lov muvaffaqiyatli! Robotingiz ishga tushdi.")
