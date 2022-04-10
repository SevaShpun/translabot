import asyncio
import json
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.dispatcher import FSMContext
from aiogram.utils.executor import start_polling
from database import *
from markup import *


def config_load():
    with open("config.json", "r", encoding="utf-8") as f:
        return dict(json.loads(f.read()))


CFG = config_load()
API_TOKEN = CFG.get("api_token")

logging.basicConfig(level=logging.INFO)
loop = asyncio.get_event_loop()
bot = Bot(token=API_TOKEN, loop=loop, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot)



def my_decorator(func):
    """Декоратор my_decorator"""
    async def wrapper(message):
        db=DB(message)
        try:
            user:User=db.get()
            if user:
                language.lang=user.lang
            else:
                user:User=db.reg()
                language.lang=user.lang
        except:
            db.create_tables()
            user:User=db.reg()
            language.lang=user.lang
        return await func(message)

    return wrapper


@dp.message_handler(commands=["start"])
async def command_start(message: types.Message):
    await bot.send_message(message.from_user.id, "/ct - создание БД и таблиц\n/reg - регистрация")


@dp.message_handler(commands=["ct"])
async def command_create_table(message: types.Message):
    """По команде /ct Создает базу данных и таблицу"""
    db=DB(message)
    await bot.send_message(message.from_user.id, db.create_tables())


@dp.message_handler(commands=["reg"])
@my_decorator
async def command_reg(message: types.Message):
    """По команде /reg создает запись в таблице (если она не сущетсвует) и возвращает выбор языка"""
    await bot.send_message(message.from_user.id, "✌️😁", reply_markup=keyboard(menu="lang", is_inline=True))


@dp.message_handler(lambda x: x.text in language.get_button().get("status"))
async def button_status(message: types.Message):
    """Обработка нажатия кнопки 'Статус/Status'"""
    await bot.send_message(message.from_user.id, language.get_text().get("status"), reply_markup=keyboard(menu="menu"))


@dp.message_handler(lambda x: x.text in language.get_button().get("action"))
async def button_action(message: types.Message):
    """Обработка нажатия кнопки 'Действия/Action'"""
    await bot.send_message(message.from_user.id, language.get_text().get("action"), reply_markup=keyboard(menu="menu"))


@dp.callback_query_handler(lambda c: c.data in ["ru", "en"])
async def callback_lang(callback_query: types.CallbackQuery):
    """Обработка нажатия кнопок языка"""
    db = DB(callback_query)
    user:User = db.get()
    user.lang = callback_query.data
    language.lang=callback_query.data
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text=language.get_text().get("welcome"),
        reply_markup=keyboard(menu="menu")
    )
    db.update(user)


if __name__ == '__main__':
    start_polling(dp, loop=loop, skip_updates=True)
