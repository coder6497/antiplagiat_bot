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
    markup.add(show_text)
    markup.add(for_gleb)
    await bot.send_message(message.chat.id, "Введите тексты для проверки или посмотрите их", reply_markup=markup)


@bot.message_handler(func=lambda message: True, content_types=['text', "photo"])
async def handle_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    check_antiplag = types.KeyboardButton(buttons[1])
    back = types.KeyboardButton(buttons[2])
    markup.add(check_antiplag)
    markup.add(back)
    if message.text not in buttons:
        insertion_query = texts.insert().values({"text": '\n'.join(message.text.split('.')), "user_id": message.from_user.id})
        conn.execute(insertion_query)
        conn.commit()
    if message.text == buttons[0]:
        rows = conn.execute(db.select(texts).where(texts.columns.user_id == message.from_user.id)).fetchall()
        for row in rows:
            await bot.send_message(message.chat.id, f"{row.text_id}.\t\n {row.text}", reply_markup=markup)
        if len(rows) == 0:
            await bot.send_message(message.chat.id, "У вас нет текстов", reply_markup=markup)


asyncio.run(bot.infinity_polling())
