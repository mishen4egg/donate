import asyncio
import requests
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, LabeledPrice
from aiogram.filters import Command

BOT_TOKEN = "8586324359:AAFDJ2U85e61UrhtU10MzAO3zApqxbXizw0"
SERVER_URL = "https://donate-rcty.onrender.com/donation"

bot = Bot(BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def start(msg: Message):
    await msg.answer(
        "💫 Донат звёздами",
        reply_markup={
            "inline_keyboard": [[
                {"text": "⭐ 50", "callback_data": "donate_50"},
                {"text": "⭐ 100", "callback_data": "donate_100"}
            ]]
        }
    )


@dp.callback_query(F.data.startswith("donate_"))
async def donate(call):
    amount = int(call.data.split("_")[1])

    await bot.send_invoice(
        chat_id=call.from_user.id,
        title="Донат",
        description="Спасибо за поддержку ❤️",
        payload="donate",
        currency="XTR",
        prices=[LabeledPrice(label="Stars", amount=amount)]
    )


@dp.pre_checkout_query()
async def checkout(query):
    await bot.answer_pre_checkout_query(query.id, ok=True)


@dp.message(F.successful_payment)
async def success(msg: Message):
    requests.post(SERVER_URL, json={
        "user": msg.from_user.username or msg.from_user.first_name,
        "amount": msg.successful_payment.total_amount
    })

    await msg.answer("🔥 Спасибо за донат!")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
