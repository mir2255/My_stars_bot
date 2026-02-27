import telebot
from telebot import types

# BotFather-dan olgan YANGI TOKENNI shu yerga qo'ying
TOKEN = 'YANGI_TOKENNI_SHU_YERGA_QOYING'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    # Hozircha oddiy sayt qo'yamiz, bot ishlashini tekshirish uchun
    web_app = types.WebAppInfo("https://google.com")
    button = types.InlineKeyboardButton("O'yinni ochish", web_app=web_app)
    markup.add(button)
    
    bot.send_message(message.chat.id, "Tabriklayman! Bot ishladi! ✅", reply_markup=markup)

if __name__ == "__main__":
    bot.remove_webhook()
    bot.polling(none_stop=True)
