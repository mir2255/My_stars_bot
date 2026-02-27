import telebot
from telebot import types
import sqlite3
import time

# Siz bergan eng yangi token
TOKEN = '8361228448:AAF7Zf-3o9ziQRtfUu1Nz_QHDWEjAX8od98'
bot = telebot.TeleBot(TOKEN)

# Ma'lumotlar bazasini sozlash
def init_db():
    conn = sqlite3.connect('startap_pro.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                      (user_id INTEGER PRIMARY KEY, balance INTEGER DEFAULT 0, wallet TEXT, referrals INTEGER DEFAULT 0)''')
    conn.commit()
    conn.close()

init_db()

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    args = message.text.split()
    
    conn = sqlite3.connect('startap_pro.db')
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
    
    # Do'stini chaqirgan bo'lsa 5000 ⭐ bonus
    if len(args) > 1 and args[1].isdigit():
        referrer_id = int(args[1])
        if referrer_id != user_id:
            cursor.execute("UPDATE users SET balance = balance + 5000, referrals = referrals + 1 WHERE user_id = ?", (referrer_id,))
    
    conn.commit()
    conn.close()

    markup = types.InlineKeyboardMarkup(row_width=1)
    web_app = types.WebAppInfo("https://mir2255.github.io/My_stars_bot/")
    
    btn_play = types.InlineKeyboardButton("🎮 StarTap-ni boshlash", web_app=web_app)
    btn_invite = types.InlineKeyboardButton("👥 Do'stni taklif qilish (+5000 ⭐)", switch_inline_query=f"\nt.me/StarTap_bot?start={user_id}")
    btn_wallet = types.InlineKeyboardButton("💎 Hamyonni ulash (TON)", callback_data="connect_wallet")
    
    markup.add(btn_play, btn_invite, btn_wallet)

    bot.send_message(message.chat.id, "🌟 **StarTap PRO** ishga tushdi!\n\nYangi token ulandi. O'yinni boshlang va do'stlarni taklif qiling!", parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "connect_wallet")
def wallet_request(call):
    msg = bot.send_message(call.message.chat.id, "TON hamyon manzilingizni yuboring:")
    bot.register_next_step_handler(msg, save_wallet)

def save_wallet(message):
    wallet_address = message.text
    user_id = message.from_user.id
    conn = sqlite3.connect('startap_pro.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET wallet = ? WHERE user_id = ?", (wallet_address, user_id))
    conn.commit()
    conn.close()
    bot.send_message(message.chat.id, "✅ Hamyon saqlandi!")

# Conflict (409) xatosini oldini olish uchun asosiy qism
if __name__ == '__main__':
    try:
        bot.remove_webhook() # Eski ulanishlarni uzish
        time.sleep(1) # Tizimga nafas olishga vaqt berish
        print("Bot muvaffaqiyatli ishga tushdi!")
        bot.polling(none_stop=True)
    except Exception as e:
        print(f"Xatolik yuz berdi: {e}")
