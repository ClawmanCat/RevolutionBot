from telegram.ext import CommandHandler, ConversationHandler


def respond(update, context, message):
    context.bot.send_message(chat_id = update.effective_chat.id, text = message)


def add_command(dispatcher, command, name):
    handler = CommandHandler(name, command)
    dispatcher.add_handler(handler)


def add_conversation(dispatcher, conv_handler):
    dispatcher.add_handler(conv_handler)