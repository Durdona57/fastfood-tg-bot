from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_categories_keyboard(categories):
    inline_keyboard = []

    for category in categories:
        cat_id = category[0]
        cat_name = category[1]

        inline_keyboard.append([
            InlineKeyboardButton(text=cat_name, callback_data=f"category_{cat_id}")
        ])
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def get_product_keyboard(product_id):
    inline_keyboard = [
        [
            InlineKeyboardButton(text="🛒 Savatga qo'shish", callback_data=f"add_{product_id}")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

def get_cart_keyboard():
    """Savat ostida chiqadigan inline tugma"""
    inline_keyboard = [
        [
            InlineKeyboardButton(text="🚖 Buyurtma berish", callback_data="start_order")
        ],
        [
            InlineKeyboardButton(text="🗑️ Savatni bo'shatish", callback_data="clear_cart")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
