import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    MenuButtonWebApp,
    WebAppInfo,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBAPP_URL = os.getenv("WEBAPP_URL")  # masalan: https://username.github.io/ig-launcher/

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN environment variable o'rnatilmagan")
if not WEBAPP_URL:
    raise RuntimeError("WEBAPP_URL environment variable o'rnatilmagan")

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

WELCOME_TEXT = (
    "<b>Salom!</b>\n\n"
    "Endi Instagram'ga Telegramdan chiqmasdan tezkor o'tishingiz mumkin — "
    "kompyuterda ishlayotganingizda ham qulay.\n\n"
    "Pastdagi tugmani bosing 👇"
)


def main_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📷 Instagram'ni ochish",
                    web_app=WebAppInfo(url=WEBAPP_URL),
                )
            ]
        ]
    )


@dp.message(CommandStart())
async def handle_start(message: Message) -> None:
    await message.answer(WELCOME_TEXT, reply_markup=main_keyboard())


@dp.message()
async def handle_other(message: Message) -> None:
    await message.answer(
        "Instagram'ga o'tish uchun pastdagi tugmadan foydalaning 👇",
        reply_markup=main_keyboard(),
    )


async def setup_menu_button() -> None:
    await bot.set_chat_menu_button(
        menu_button=MenuButtonWebApp(
            text="Instagram",
            web_app=WebAppInfo(url=WEBAPP_URL),
        )
    )


async def main() -> None:
    await setup_menu_button()
    logger.info("Bot ishga tushdi")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
