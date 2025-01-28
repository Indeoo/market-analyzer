import asyncio

from telegram.ext import ApplicationBuilder

from config.logs import load_logger
from data.migration import run_migrations
from envs import TELEGRAM_API
from handlers.handler_utils import create_telegram_handlers
from service.telegram_service import set_bot_commands


async def create_app():
    load_logger(None, False, None)
    app = ApplicationBuilder().token(TELEGRAM_API).build()
    handlers = create_telegram_handlers()
    app.add_handlers(handlers)
    await set_bot_commands(app)

    return app


if __name__ == "__main__":
    #run_migrations()
    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(create_app())
    app.run_polling()
