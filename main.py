import telebot
from config import token
from bot_algorhitms import write_file

bot = telebot.TeleBot(token)


@bot.message_handler(commands=["start"])
def handle_start(message):
    bot.send_message(message.chat.id, "Ай, что за кондиции!!!!!!")


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    write_file(message.text)
    bot.reply_to(message, "Текст отправлен на обработку")


bot.polling(non_stop=True)