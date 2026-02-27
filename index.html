import telebot
from telebot import types
import sqlite3

# 1. Tokenni to'g'ri o'rnatish
TOKEN = '8361228448:AAGgNsRk9Xvf5frIoUI3QthXUNEAhRRVTio'
bot = telebot.TeleBot(TOKEN)

# 2. Ma'lumotlar bazasi
def init_db():
    conn = sqlite3.connect('startap_pro.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                      (user_id INTEGER PRIMARY KEY, balance INTEGER DEFAULT 0, wallet TEXT, referrals INTEGER DEFAULT 0)''')
    conn.commit()
    conn.close()

init_db()

# 3. Start komandasi va Referal tizimi
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    args = message.text.split()
    
    conn = sqlite3.connect('startap_pro.db')
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
    
    if len(args) > 1 and args[1].isdigit():
        referrer_id = int(args[1])
        if referrer_id != user_id:
            cursor.execute("UPDATE users SET balance = balance + 5000, referrals = referrals + 1 WHERE user_id = ?", (referrer_id,))
    
    conn.commit()
    conn.close()

    markup = types.InlineKeyboardMarkup(row_width=1)
    web_app = types.WebAppInfo(f"https://mir2255.github.io/My_stars_bot/")
    
    btn_play = types.InlineKeyboardButton("🎮 StarTap-ni boshlash", web_app=web_app)
    btn_invite = types.InlineKeyboardButton("👥 Do'stni taklif qilish (+5000 ⭐)", switch_inline_query=f"\nStarTap-da yulduz yig'ing! \nt.me/StarTap_bot?start={user_id}")
    btn_wallet = types.InlineKeyboardButton("💎 Hamyonni ulash (TON)", callback_data="connect_wallet")
    
    markup.add(btn_play, btn_invite, btn_wallet)

    bot.send_message(message.chat.id, "🌟 **StarTap Pro** ishga tushdi!\n\nDo'stlarni chaqiring va darajangizni oshiring!", parse_mode="Markdown", reply_markup=markup)

# 4. Hamyonni saqlash
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

# 5. Botni ishga tushirish (Conflict xatosini oldini olish uchun)
if __name__ == '__main__':
    bot.remove_webhook() # Eski ulanishlarni uzish
    bot.polling(none_stop=True)
