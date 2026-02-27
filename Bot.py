import telebot
from telebot import types

# O'z tokiningizni kiriting
TOKEN = 8361228448:AAHldiripHrzrQA1rQyvbWcheuHMljJ5B7o

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    # Tugmalar to'plami
    markup = types.InlineKeyboardMarkup()
    
    # BU YERGA O'YIN SAYTINGIZ MANZILINI QO'YING
    web_app = types.WebAppInfo("https://sizning-saytingiz.uz") 
    
    button = types.InlineKeyboardButton("O'yinni ochish", web_app=web_app)
    markup.add(button)
    
    bot.send_message(message.chat.id, "Salom! O'yinni boshlash uchun pastdagi tugmani bosing:", reply_markup=markup)

# BOTNI TIRSILATIB ISHLATADIGAN ASOSIY QATOR:
bot.polling(none_stop=True)
