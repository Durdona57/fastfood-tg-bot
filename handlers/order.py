from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from handlers.states import OrderSteps
from database.db_helper import get_user_cart, clear_user_cart

order_router = Router()



@order_router.callback_query(F.data == "start_order")
async def start_order_process(call: types.CallbackQuery, state: FSMContext):
    await call.answer()

    user_id = call.from_user.id
    cart_items = get_user_cart(user_id)

    if not cart_items:
        await call.message.answer("Sizning savatchangiz bo'sh!")
        return

    await call.message.answer("🚖 Buyurtmani rasmiylashtirish boshlandi.\n\nIltimos, ismingizni kiriting:")
    await state.set_state(OrderSteps.waiting_for_name)



@order_router.message(OrderSteps.waiting_for_name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(user_name=message.text)  # Ismni xotiraga saqlaymiz

    phone_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📱 Telefon raqamni yuborish", request_contact=True)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await message.answer("Rahmat! Endi pastdagi tugmani bosib telefon raqamingizni yuboring:",
                         reply_markup=phone_keyboard)
    await state.set_state(OrderSteps.waiting_for_phone)



@order_router.message(OrderSteps.waiting_for_phone, F.contact)
async def process_phone(message: types.Message, state: FSMContext):
    phone_number = message.contact.phone_number
    await state.update_data(user_phone=phone_number)  # Telefonni saqlaymiz

    await message.answer(
        "Ajoyib! Endi yetkazib berish manzilini kiriting (Masalan: Chilonzor 1-kvartal, 5-uy):",
        reply_markup=ReplyKeyboardRemove()  # Telefon tugmasini ekrandan tozalaymiz
    )
    await state.set_state(OrderSteps.waiting_for_address)



@order_router.message(OrderSteps.waiting_for_phone, F.contact)
async def process_phone(message: types.Message, state: FSMContext):
    phone_number = message.contact.phone_number
    await state.update_data(user_phone=phone_number)


    location_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📍 Lokatsiyani yuborish", request_location=True)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await message.answer(
        "Ajoyib! Endi pastdagi tugmani bosib turgan joyingiz lokatsiyasini yuboring:",
        reply_markup=location_keyboard
    )
    await state.set_state(OrderSteps.waiting_for_address)



@order_router.message(OrderSteps.waiting_for_address, F.location)
async def process_address(message: types.Message, state: FSMContext):

    latitude = message.location.latitude
    longitude = message.location.longitude

    user_id = message.from_user.id
    user_data = await state.get_data()
    name = user_data.get("user_name")
    phone = user_data.get("user_phone")


    clear_user_cart(user_id)

    success_text = (
        f"✅ **Buyurtmangiz muvaffaqiyatli qabul qilindi!**\n\n"
        f"👤 **Ism:** {name}\n"
        f"📞 **Telefon:** {phone}\n"
        f"📍 **Manzil:** Lokatsiya qabul qilindi.\n\n"
        f"⏳ Operatorimiz tez orada siz bilan bog'lanadi. Rahmat!"
    )

    await message.answer(text=success_text, reply_markup=ReplyKeyboardRemove(), parse_mode="Markdown")


    await state.clear()
