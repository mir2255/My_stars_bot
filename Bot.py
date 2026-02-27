import logging
import json
import httpx
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, CommandObject
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton, LabeledPrice

# ASOSIY SOZLAMALAR
TOKEN = "8361228448:AAF1x3Y87Q0vmAEs_Dp9xnJNWGJdJYCyfsg"
WEB_APP_URL = "https://mir2255.github.io/My_stars_bot/"
# Bulutli baza (ma'lumotlar o'chib ketmasligi uchun)
DB_URL = "https://kvv.io/api/v1/store" 

bot = Bot(token=TOKEN)
dp = Dispatcher()

# BAZA BILAN ISHLASH FUNKSIYALARI
async def get_user_data(user_id):
    async with httpx.AsyncClient() as client:
        try:
            r = await client.get(f"{DB_URL}/{user_id}")
            return r.json() if r.status_code == 200 else None
        except: return None

async def save_user_data(user_id, data):
    async with httpx.AsyncClient() as client:
        try: await client.post(f"{DB_URL}/{user_id}", json=data)
        except: pass

# START BUYRUG'I VA REFERAL
@dp.message(Command("start"))
async def start_cmd(message: types.Message, command: CommandObject):
    user_id = message.from_user.id
    user_data = await get_user_data(user_id)
    
    if not user_data:
        # Yangi foydalanuvchi yaratish
        user_data = {"balance": 0, "energy": 500}
        await save_user_data(user_id, user_data)
        
        # Referalni tekshirish
        if command.args and command.args.isdigit():
            ref_id = int(command.args)
            if ref_id != user_id:
                ref_data = await get_user_data(ref_id)
                if ref_data:
                    ref_data["balance"] += 5000
                    await save_user_data(ref_id, ref_data)
                    try: await bot.send_message(ref_id, "🎉 Do'stingiz qo'shildi! Sizga 5000 bonus berildi!")
                    except: pass

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="O'yinni boshlash 🎮", web_app=WebAppInfo(url=WEB_APP_URL))],
        [InlineKeyboardButton(text="Do'stlarni taklif qilish 👥", switch_inline_query=f"\nDo'stim, mana bu o'yinni o'yna va 5000 bonus ol: https://t.me/{(await bot.get_me()).username}?start={user_id}")]
    ])
    
    await message.answer(
        f"Xush kelibsiz! 👋\n\n💰 Balansingiz: {user_data['balance']} tanga\n⚡️ Energiya: {user_data['energy']}/500",
        reply_markup=kb
    )

# WEB APP'DAN MA'LUMOT QABUL QILISH
@dp.message(F.web_app_data)
async def web_app_handler(message: types.Message):
    data = json.loads(message.web_app_data.data)
    user_id = message.from_user.id
    
    if data.get("action") == "sync":
        # Tangalarni bazaga saqlash
        await save_user_data(user_id, {"balance": data['coins'], "energy": data['energy']})
        
    if data.get("action") == "buy_bot":
        # Yulduzcha (Stars) invoysini chiqarish
        await message.answer_invoice(
            title="TapBot Activator",
            description="24 soatlik avtomatik bosish roboti",
            prices=[LabeledPrice(label="TapBot", amount=20)],
            payload="bot_pay",
            currency="XTR",
            provider_token="" # Stars uchun bo'sh qoladi
        )

# TO'LOVNI TASDIQLASH
@dp.pre_checkout_query()
async def checkout_handler(query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(query.id, ok=True)

@dp.message(F.successful_payment)
async def payment_success(message: types.Message):
    await message.answer("✅ To'lov muvaffaqiyatli! Robotingiz faollashtirildi.")

# BOTNI ISHGA TUSHIRISH
async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
