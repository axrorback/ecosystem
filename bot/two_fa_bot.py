import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery
)
import logging
import os
from dotenv import load_dotenv
load_dotenv()
from aiogram.filters import CommandStart

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


def thanks_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Tushundim, rahmat",
                    callback_data="thanks"
                )
            ]
        ]
    )
@dp.message(CommandStart())
async def start_handler(message: Message):
    user_id = message.from_user.id

    text = (
        "👋 *Salom!*\n\n"
        "Quyida sizning *Telegram ID* raqamingiz joylashgan.\n"
        "Uni ustiga bosib nusxalashingiz mumkin 👇\n\n"
        f"<code>{user_id}</code>\n"
    )
    await message.answer(
        text=text,
        parse_mode="HTML",
        reply_markup=thanks_keyboard()
    )


@dp.callback_query(F.data == "thanks")
async def thanks_handler(callback: CallbackQuery):
    await callback.message.answer(
        "🌟 Rahmat!\n\n"
        "Bugungi kuningiz a’lo darajada o‘tsin.\n"
        "Omad va muvaffaqiyat tilayman 🚀\n\n"
        "Hurmat bilan\n\n"
        "CODERBOYS ECOSYSTEM"
    )
    await callback.answer()


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
