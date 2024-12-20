import asyncio
from telebot.async_telebot import AsyncTeleBot
from config import token
from telebot import types
import sqlalchemy as db

bot = AsyncTeleBot(token)

engine = db.create_engine('sqlite:///text_data.db')
conn = engine.connect()
metadata = db.MetaData()

texts = db.Table('texts', metadata,
        db.Column("text_id", db.Integer, primary_key=True),
            db.Column('text', db.Text),
            db.Column('user_id', db.Integer)
                 )

metadata.create_all(engine)
buttons = ["Посмотреть тексты", "Проверить на антиплагиат", "/start", "О программе", "Удалить текст"]

@bot.message_handler(commands=["start"])
async def handle_start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    show_text = types.KeyboardButton(buttons[0])
    for_gleb = types.KeyboardButton(buttons[3])
    check_antiplag = types.KeyboardButton(buttons[1])
    markup.add(show_text)
    markup.add(for_gleb)
    markup.add(check_antiplag)
    await bot.send_message(message.chat.id, "Введите тексты для проверки или посмотрите их", reply_markup=markup)


@bot.message_handler(func=lambda message: True, content_types=['text', 'photo'])
async def handle_message(message):
    rows = conn.execute(db.select(texts).where(texts.columns.user_id == message.from_user.id)).fetchall()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    back = types.KeyboardButton(buttons[2])
    markup.add(back)
    list(map(lambda x: markup.add(types.KeyboardButton(f'Удалить текст № {str(x.text_id)}')), rows))
    if message.text not in buttons and message.text[:13] != "Удалить текст":
        if len(rows) < 2:
            insertion_query = texts.insert().values({"text": '\n'.join(message.text.split('.')), "user_id": message.from_user.id})
            conn.execute(insertion_query)
            conn.commit()
    if message.text == buttons[0]:
        for row in rows:
            await bot.send_message(message.chat.id, f"{row.text_id}.\t\n {row.text}", reply_markup=markup)
        if len(rows) == 0:
            await bot.send_message(message.chat.id, "У вас нет текстов", reply_markup=markup)
    for row in rows:
        if message.text == f'Удалить текст № {str(row.text_id)}':
            conn.execute(texts.delete().where(texts.columns.text_id == row.text_id).where(texts.columns.user_id == message.from_user.id))
            conn.commit()
            await bot.send_message(message.chat.id, f"Текст № {row.text_id} удален", reply_markup=markup)
    if message.text == buttons[1]:
            text1 = rows[0].text.split('\n')
            text2 = rows[1].text.split('\n')
            count = 0
            for i in range(len(text1)):
                for j in range(len(text2)):
                    if text1[i] == text2[j]:
                        count += 1
            await bot.send_message(message.chat.id, f"Количество совпадений: {count}")
            if count > 5:
                await bot.send_message(message.chat.id, "Тексты совпадают на более чем 5 позиции, ПОДОЗРЕНИЕ НА ПЛАГИАТ")
            if count > 10:
                await bot.send_message(message.chat.id, "Тексты совпадают более чем на 10 позиции, ПЛАГИАТ")
                await bot.send_photo(message.chat.id, open('для Глеба.png', 'rb'))
            if count < 5:
                await bot.send_message(message.chat.id, "Тексты не совпадают ни на одной позиции, НЕ ПЛАГИАТ")

asyncio.run(bot.infinity_polling())
