from telegram import BotCommand


async def set_bot_commands(app):
    commands = [
        ("notify", "Notify about new tokens on Jupiter"),
    ]
    await app.bot.set_my_commands([BotCommand(command, description) for command, description in commands])

