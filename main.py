from telegram import InputFile
from telegram.ext import Updater, ConversationHandler

from utils import *
from items import *
import add_item


with open(path.join(asset_folder, 'token.txt'), 'r') as token_file:
    token = token_file.read()

updater = Updater(token = token, use_context = True)
dispatcher = updater.dispatcher


def on_revolve(update, context):
    file, (name, desc) = items.random_item()
    id = update.effective_chat.id

    with open('./assets/' + file, 'rb') as f:
        context.bot.set_chat_photo(id, InputFile(f, filename = name))
        context.bot.setChatTitle(id, name)
        context.bot.setChatDescription(id, desc + '\n\nDiscord: https://discord.gg/jjaFNAN')

    send_message(update, context, "The king is dead, long live the king!")


def on_list_images(update, context):
    names = '\n'.join(map(
        lambda name_desc: name_desc[0],
        items.get_items().values()
    ))

    names = "Khajiit has shitty memes if you have coin:\n\n" + names
    send_message(update, context, names)


def on_refresh(update, context):
    items.load()
    send_reply(update, context, "List has been refreshed.")


def on_del_entry(update, context):
    if items.remove_name(update.message.text[len('/del_entry '):]):
        send_reply(update, context, "That shit is gone bruh")
        items.save()
    else:
        send_reply(update, context, "I don't have a fucking clue what that is")


add_command(dispatcher, on_revolve,     'revolve'  )
add_command(dispatcher, on_list_images, 'list'     )
add_command(dispatcher, on_refresh,     'refresh'  )
add_command(dispatcher, on_del_entry,   'del_entry')
add_conversation(dispatcher, add_item.conversation_handler)

items.load()
updater.start_polling()