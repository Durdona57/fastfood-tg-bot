import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from config import BOT_TOKEN
from database.db_helper import init_db, seed_data
from keyboards.reply import get_main_menu
from handlers.menu import menu_router
from handlers.order import order_router


from handlers.menu import menu_router

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


dp.include_router(menu_router)
dp.include_router(order_router)

init_db()
seed_data()

@dp.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer(
        f"Salom {message.from_user.full_name}! FastFood botimizga xush kelibsiz.\n"
        f"Buyurtma berish uchun '🛍️ Menyu' tugmasini bosing.",
        reply_markup=get_main_menu()
    )

async def main():
    print("Fastfood boti ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
