import telebot
from config import token

bot = telebot.TeleBot(token)


@bot.message_handler(commands=["start"])
def handle_start(message):
    bot.send_message(message.chat.id, "Ай, что за кондиции!!!!!!")


bot.polling(non_stop=True)