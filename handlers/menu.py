from aiogram import Router, F, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from database.db_helper import get_categories, get_products_by_category, add_to_cart, get_user_cart, clear_user_cart
from keyboards.inline import get_categories_keyboard, get_product_keyboard, get_cart_keyboard

menu_router = Router()


@menu_router.message(F.text == "🛍️ Menyu")
async def show_menu(message: types.Message):
    categories = get_categories()
    reply_markup = get_categories_keyboard(categories)
    await message.answer(
        text="📍 Kategoriyalardan birini tanlang:",
        reply_markup=reply_markup
    )


@menu_router.callback_query(F.data.startswith("category_"))
async def show_products(call: types.CallbackQuery):
    await call.answer()
    category_id = int(call.data.split("_")[1])
    products = get_products_by_category(category_id)

    if not products:
        await call.message.answer("Hozircha bu kategoriyada mahsulotlar yo'q.")
        return

    for product in products:
        p_id, cat_id, name, price, desc, image = product
        caption = f"🍏 **{name}**\n\n📝 {desc}\n\n💰 Narxi: {price:,} so'm"

        await call.message.answer(
            text=caption,
            reply_markup=get_product_keyboard(p_id),
            parse_mode="Markdown"
        )

#
@menu_router.callback_query(F.data.startswith("add_"))
async def process_add_to_cart(call: types.CallbackQuery):
    product_id = int(call.data.split("_")[1])
    user_id = call.from_user.id

    add_to_cart(user_id, product_id)
    await call.answer(text="✅ Mahsulot savatga qo'shildi!", show_alert=False)

@menu_router.message(F.text == "🛒 Savatcha")
async def show_cart(message: types.Message):
    user_id = message.from_user.id
    cart_items = get_user_cart(user_id)

    if not cart_items:
        await message.answer("Sizning savatchangiz bo'sh. Taom buyurtma qilish uchun '🛍️ Menyu'ga kiring.")
        return

    text = "🛒 **Sizning savatchangiz:**\n\n"
    total_price = 0

    for item in cart_items:
        name, price, quantity = item
        item_total = price * quantity
        total_price += item_total
        text += f"▪️ {name} x {quantity} = {item_total:,} so'm\n"

    text += f"\n💰 **Umumiy hisob:** {total_price:,} so'm"


    await message.answer(text=text, reply_markup=get_cart_keyboard(), parse_mode="Markdown")

# 5. Savatni bo'shatish xandleri
@menu_router.callback_query(F.data == "clear_cart")
async def process_clear_cart(callback: CallbackQuery):
    user_id = callback.from_user.id
    clear_user_cart(user_id)
    await callback.message.edit_text("🗑️ Sizning savatingiz to'liq bo'shatildi!")
    await callback.answer("Savat bo'shatildi")


@menu_router.message(F.text == "📞 Biz bilan aloqa")
async def show_contact(message: types.Message):
    contact_text = (
        "📞 **Biz bilan bog'lanish:**\n\n"
        "📍 **Asosiy filial:** Toshkent sh., Chilonzor 1-kvartal\n"
        "⏰ **Ish vaqti:** 09:00 - 23:00\n"
        "☎️ **Ishonch telefoni:** +998 71 123-45-67\n\n"
        "💬 Savol va takliflar bo'lsa, adminga yozishingiz mumkin:"
    )

    admin_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✍️ Adminga yozish", url="https://t.me")]
        ]
    )
    await message.answer(text=contact_text, reply_markup=admin_keyboard, parse_mode="Markdown")


@menu_router.message(F.text == "⚙️ Sozlamalar")
async def show_settings(message: types.Message):
    settings_text = (
        "⚙️ **Sozlamalar bo'лимi**\n\n"
        "Hozirgi til: 🇺🇿 O'zbekcha\n"
        "Bot tilini o'zgartirish uchun pastdagi tugmalardan birini tanlang:"
    )

    language_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data="lang_uz"),
                InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru")
            ]
        ]
    )
    await message.answer(text=settings_text, reply_markup=language_keyboard, parse_mode="Markdown")


@menu_router.callback_query(F.data.startswith("lang_"))
async def change_language(call: types.CallbackQuery):
    selected_lang = call.data.split("_")[1]

    if selected_lang == "uz":
        await call.answer(text="Til o'zgartirilmadi, chunki allaqachon o'zbek tilidasiz!", show_alert=True)
    elif selected_lang == "ru":
        await call.answer(text="Русский язык будет доступен в следующем обновлении backend-a!", show_alert=True)
