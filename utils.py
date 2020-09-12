from telegram.ext import CommandHandler, ConversationHandler


def send_message(update, context, message):
    context.bot.send_message(chat_id = update.effective_chat.id, text = message)


def send_reply(update, context, message):
    update.message.reply_text(message)


def add_command(dispatcher, command, name):
    handler = CommandHandler(name, command)
    dispatcher.add_handler(handler)


def add_conversation(dispatcher, conv_handler):
    dispatcher.add_handler(conv_handler)