from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import requests
import os

BOT_TOKEN = "ТВОЙ_BOT_TOKEN"
SERVER_URL = "https://ТВОЙ-СЕРВЕР"

bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start(msg: types.Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("⭐ 10", callback_data="donate_10"),
         InlineKeyboardButton("⭐ 25", callback_data="donate_25")],
        [InlineKeyboardButton("⭐ 50", callback_data="donate_50"),
         InlineKeyboardButton("⭐ 100", callback_data="donate_100")],
        [InlineKeyboardButton("✍️ Ввести свою сумму", callback_data="custom")]
    ])

    await msg.answer("✍️ Напиши сообщение к донату\n⬇️ Потом выбери сумму ⭐", reply_markup=kb)


@dp.callback_query_handler(lambda c: c.data.startswith("donate_"))
async def donate(cb: types.CallbackQuery):
    amount = int(cb.data.split("_")[1])

    await bot.send_invoice(
        chat_id=cb.from_user.id,
        title="Поддержка стрима",
        description="Спасибо за поддержку ❤️",
        payload=f"donate_{amount}",
        currency="XTR",
        prices=[types.LabeledPrice(label="Donation", amount=amount)],
    )


@dp.message_handler(content_types=types.ContentType.SUCCESSFUL_PAYMENT)
async def success(msg: types.Message):
    user = msg.from_user.username or msg.from_user.first_name
    amount = msg.successful_payment.total_amount

    requests.get(
        f"{SERVER_URL}/donate",
        params={
            "user": user,
            "amount": amount,
            "text": "⭐"
        }
    )

    await msg.answer("Спасибо за донат ⭐❤️")


if __name__ == "__main__":
    executor.start_polling(dp)
