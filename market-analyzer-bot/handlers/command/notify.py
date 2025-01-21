import asyncio

from telegram import Update
from telegram.ext import ContextTypes

from service.new_tokens_test import process_new_tokens


async def notify(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    asyncio.create_task(
        process_new_tokens(context, update, user_id)
    )