import asyncio
from telebot.async_telebot import AsyncTeleBot
from config import token
from random import randint
import os
import sqlalchemy as db



bot = AsyncTeleBot(token)

engine = db.create_engine('sqlite:///text_data.db')
conn = engine.connect()
metadata = db.MetaData()

texts = db.Table('texts', metadata,
        db.Column("text_id", db.Integer, primary_key=True),
            db.Column('text_data', db.Text))

metadata.create_all(engine)


@bot.message_handler(commands=["start"])
async def handle_start(message):
    await bot.send_message(message.chat.id, "Введите первый текст затем второй")


@bot.message_handler(func=lambda message: True, content_types='text')
async def handle_message(message):
    with open(f"files/file{randint(1, 1000)}.txt", 'w', encoding='utf-8') as f:
        f.write('\n'.join(message.text.split('.')))
    with open(f"files/{os.listdir("files")[0]}", 'r', encoding='utf-8') as f:
        data = f.read().split('\n')
    with open(f"files/{os.listdir("files")[1]}", 'r', encoding='utf-8') as f:
        data2 = f.read().split('\n')
    count = 0
    for i in range(len(data)):
        for j in range(len(data2)):
            if data[i] == data2[j]:
                count += 1
    if len(os.listdir('files')) >= 2:
        await bot.send_message(message.chat.id, "Данные обработаны. Максимальное количество файлов достигнуто.")
        await bot.send_message(message.chat.id, f"Кол-во совпадений в предложениях: {count}")
        insertion_query = texts.insert().values([{"text_data": '\n'.join(data)},
                                                 {"text_data": '\n'.join(data2)}])
        conn.execute(insertion_query)
        conn.commit()
        list(map(lambda x: os.remove(f"files/{x}"), os.listdir('files')))


asyncio.run(bot.infinity_polling())
