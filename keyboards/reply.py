from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_menu():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🛍️ Menyu"), KeyboardButton(text="🛒 Savatcha")],
            [KeyboardButton(text="📞 Biz bilan aloqa"), KeyboardButton(text="⚙️ Sozlamalar")]
        ],
        resize_keyboard=True
    )
    return keyboard
