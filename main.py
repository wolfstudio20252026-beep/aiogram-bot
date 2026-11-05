from os import getenv
import asyncio
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from handlers.routes import router, notifier
import os
from aiohttp import web

load_dotenv()
TOKEN = getenv("BOT_TOKEN")

dp = Dispatcher()
dp.include_router(router)


async def main():
    bot = Bot(token=TOKEN)

    await start_webhook_server()
    
    asyncio.create_task(notifier(bot))
    print("Start...")
    await dp.start_polling(bot)


async def handle(request):
    return web.Response(text="Bot is running!")

async def start_webhook_server():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 8080)) 
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

if __name__ == "__main__":
    asyncio.run(main())