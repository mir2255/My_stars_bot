import telebot
from telebot import types

TOKEN = '8361228448:AAF1x3Y87Q0vmAEs_Dp9xnJNWGJdJYCyfsg'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    # Siz yaratgan o'yin linki
    web_app = types.WebAppInfo("https://mir2255.github.io/My_stars_bot/")
    btn = types.InlineKeyboardButton("O'yinni ochish", web_app=web_app)
    markup.add(btn)
    
    bot.send_message(message.chat.id, "Tabriklayman! Bot ishladi! ✅\nO'yinni boshlash uchun tugmani bosing:", reply_markup=markup)

bot.polling(none_stop=True)
