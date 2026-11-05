from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import Bot
import asyncio

router = Router()

subscribers = set()

async def notifier(bot: Bot):
    while True:
        if subscribers:
            for user_id in list(subscribers):
                try:
                    await bot.send_message(user_id, "You message")
                except Exception:
                    pass

        await asyncio.sleep(10)

@router.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "Привет!\n"
        "Я могу помочь с рассылкой!\n\n"
        "Команды:\n"
        "/subscribe – подписаться на уведомления\n"
        "/unsubscribe – отписка\n"
        "/subscribers – список подписчиков"
    )

@router.message(Command("subscribe"))
async def subscribe(message: Message):
    user_id = message.from_user.id

    subscribers.add(user_id)
    await message.answer("You subscribe")

@router.message(Command("unsubscribe"))
async def unsubscribe(message: Message):
    user_id = message.from_user.id

    subscribers.discard(user_id)
    await message.answer("You unsubscribe!")


@router.message(Command("subscribers"))
async def get_subscribers(message: Message):
    if not subscribers:
        await message.answer("Null")
        return

    text = "Subscribers:\n"
    for user_id in subscribers:
        text += f"{user_id}\n"
    
    await message.answer(text)