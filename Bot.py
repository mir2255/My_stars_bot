import telebot
from telebot import types
import time

# Sizning eng yangi tokeningiz
TOKEN = '8361228448:AAF7Zf-3o9ziQRtfUu1Nz_QHDWEjAX8od98'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    # O'yin manzili (GitHub Pages orqali)
    web_app = types.WebAppInfo("https://mir2255.github.io/My_stars_bot/")
    
    btn_play = types.InlineKeyboardButton("🎮 StarTap-ni boshlash", web_app=web_app)
    markup.add(btn_play)
    
    bot.send_message(message.chat.id, "🌟 **StarTap**-ga xush kelibsiz!\n\nO'yinni boshlash uchun quyidagi tugmani bosing:", 
                     parse_mode="Markdown", reply_markup=markup)

if __name__ == '__main__':
    bot.remove_webhook()
    time.sleep(1)
    print("Bot muvaffaqiyatli ishga tushdi!")
    bot.polling(none_stop=True)
