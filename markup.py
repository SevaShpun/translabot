from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types.reply_keyboard import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from translation import *

language = Translator()

def keyboard(menu="main", is_inline=False):
    markup = InlineKeyboardMarkup() if is_inline else ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row=3

    buttons = language.get_button()
    but_status = buttons.get("status")
    but_action = buttons.get("action")

    kb_button = KeyboardButton(but_status)
    kb_action = KeyboardButton(but_action)
    
    kb_ru = InlineKeyboardButton(text="🇷🇺", callback_data="ru")
    kb_en = InlineKeyboardButton(text="🇺🇸", callback_data="en")

    if menu=="menu":
        markup.add(kb_button, kb_action)
    if menu=="lang":
        markup.add(kb_ru, kb_en)
    return markup
