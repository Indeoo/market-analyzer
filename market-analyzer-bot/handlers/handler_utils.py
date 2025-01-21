from telegram.ext import CommandHandler

from handlers.command.notify import notify


def create_telegram_handlers():
    handlers = []

    handlers.append(CommandHandler("notify", notify))

    return handlers
