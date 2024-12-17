import asyncio
from telebot.async_telebot import AsyncTeleBot
from config import token
from bot_algorhitms import *
from random import randint
import os

bot = AsyncTeleBot(token)



@bot.message_handler(commands=["start"])
async def handle_start(message):
    await bot.send_message(message.chat.id, "Введите первый текст")


@bot.message_handler(func=lambda message: True, content_types='text')
async def handle_message(message):
    with open(f"files/file{randint(1, 1000)}.txt", 'w', encoding='utf-8') as f:
        f.write('\n'.join(message.text.split('.')))
    if len(os.listdir('files')) >= 2:
        await bot.send_message(message.chat.id, "Данные обработаны. Максимальное количество файлов достигнуто.")
        await bot.send_message(message.chat.id, f"Кол-во совпадений в предложениях: {check_file()}")
        list(map(lambda x: os.remove(f"files/{x}"), os.listdir('files')))


asyncio.run(bot.infinity_polling())
