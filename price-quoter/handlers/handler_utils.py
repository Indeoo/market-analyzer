from loguru import logger
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes


def create_telegram_handlers():
    handlers = []

    handlers.append(CommandHandler("quote", quote))

    return handlers


async def quote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    logger.info(f"Notifying {user_id}")
