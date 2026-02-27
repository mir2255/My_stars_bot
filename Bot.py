import telebot
from telebot import types

TOKEN = '7629202302:AAHgO_WzL94XpW9L1kM_XqY_lXzXzXzXzXz' # Tokeningizni tekshiring

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    web_app = types.WebAppInfo("https://mir2255.github.io/My_stars_bot/")
    btn = types.InlineKeyboardButton("🎮 O'yinni boshlash", web_app=web_app)
    markup.add(btn)
    bot.send_message(message.chat.id, "Salom! O'yin tayyor. Boshlash uchun bosing:", reply_markup=markup)

bot.polling(none_stop=True)
