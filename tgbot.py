import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ChatMemberStatus
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater
TOKEN = "7777140690:AAFw7gZY70TGevp3eGxBCVyEBZJ79LhH_As"
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHANNELS = [
    {"id": -1002355813716, "username": "+ayCbCpVmkHFkMDEy", "title": "📢 Rasmiy Kanal 1"},
    {"id": -1002395187547, "username": "+y8kS1O3XEEpjNmFi", "title": "🔥 Yangiliklar 2"}
]
updater = Updater(TOKEN, use_context=True)
bot = Bot(token=TOKEN)
dp = Dispatcher()

async def is_subscribed(user_id: int) -> bool:
    """Foydalanuvchining kanalga obuna bo‘lganligini tekshiradi"""
    for channel in CHANNELS:
        try:
            chat_member = await bot.get_chat_member(channel["id"], user_id)
            if chat_member.status in [ChatMemberStatus.LEFT, ChatMemberStatus.KICKED]:
                return False
        except Exception as e:
            print(f"❌ Xatolik: {e}")
            return False
    return True

@dp.message(Command("start"))
async def start(message: Message):
    user_id = message.from_user.id
    if await is_subscribed(user_id):
        await message.answer("✅ Siz barcha kanallarga a'zo bo‘lgansiz. Botdan foydalanishingiz mumkin!")
    else:
        # 🔹 Tugmalar yaratish
        buttons = [
            [InlineKeyboardButton(text=channel["title"], url=f"https://t.me/{channel['username']}")]
            for channel in CHANNELS
        ]
        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

        await message.answer(
            "❌ *Botdan foydalanish uchun quyidagi kanallarga a'zo bo‘ling:*\n\n"
            "📌 *Obuna bo‘lgach, /start ni qaytadan bosing!*",
            parse_mode="Markdown",
            reply_markup=keyboard
        )

async def main():
    """Botni ishga tushirish"""
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
