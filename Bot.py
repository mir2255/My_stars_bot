import telebot
from telebot import types

# BotFather'dan olgan tokenni mana shu qo'shtirnoq ichiga aniq qilib qo'ying
TOKEN = '8361228448:AAF1x3Y87Q0vmAEs_Dp9xnJNWGJdJYCyfsg' 

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    # O'yiningiz manzili
    web_app = types.WebAppInfo("https://mir2255.github.io/My_stars_bot/")
    btn = types.InlineKeyboardButton("🎮 O'yinni boshlash", web_app=web_app)
    markup.add(btn)
    
    bot.send_message(message.chat.id, "Xush kelibsiz! O'yinni boshlash uchun tugmani bosing:", reply_markup=markup)

bot.polling(none_stop=True)
