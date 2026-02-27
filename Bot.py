import telebot
from telebot import types

TOKEN = '8361228448:AAENkqz-ksApxYloCpd1ZPPQDWz3-3_WbMw'

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(row_width=1)
    # WEB APP URL manzilingizni tekshirib oling (oxiri / bilan tugashi kerak)
    web_app = types.WebAppInfo("https://mir2255.github.io/My_stars_bot/") 
    game_button = types.KeyboardButton("⭐ O'yinni boshlash", web_app=web_app)
    markup.add(game_button)
    
    bot.send_message(message.chat.id, f"Salom {message.from_user.first_name}! O'yinni boshlash uchun tugmani bosing:", reply_markup=markup)

bot.polling(none_stop=True)
