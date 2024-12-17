from telebot.async_telebot import AsyncTeleBot
from telebot import types
from config import token
from bot_algorhitms import write_file
import asyncio

bot = AsyncTeleBot(token)

@bot.message_handler(commands=["start"])
async def handle_start(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=2)
    buttons = ["Отправитe текст 💬", "Отправить файл 📄"]
    list(map(lambda x: keyboard.add(x), buttons))
    await bot.send_message(message.chat.id, "Ай, что за кондиции!!!!!!", reply_markup=keyboard)


@bot.message_handler(func=lambda message: True)
async def handle_message(message):
    await write_file(message.text)
    await bot.reply_to(message, "Текст отправлен на обработку")


asyncio.run(bot.polling(non_stop=True))
