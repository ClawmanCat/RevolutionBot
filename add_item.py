from telegram.ext import CommandHandler, ConversationHandler, MessageHandler, Filters

from utils import *
from items import *

import os
import os.path as path


NAME, DESC, FILE = range(3)
asset_folder = './assets/'


class conversation_state_storage:
    def __init__(self):
        # Username => [Server Name, Server Desc, Server Image]
        self.storage = dict()


    def insert_or_create(self, key, index, value):
        dictionary = self.storage

        if key in dictionary:
            dictionary[key][index] = value
        else:
            entry = [None] * 3
            entry[index] = value

            dictionary[key] = entry


    def add_name(self, username, server_name):
        self.insert_or_create(username, 0, server_name)

    def add_desc(self, username, server_desc):
        self.insert_or_create(username, 1, server_desc)

    def add_image(self, username, server_img):
        self.insert_or_create(username, 2, server_img)


    def is_complete(self, username):
        return username in self.storage and None not in self.storage[username]

    def get_userdata(self, username):
        return self.storage[username]

    def remove_userdata(self, username):
        if username in self.storage: del self.storage[username]

storage = conversation_state_storage()



def start_converstation(update, context):
    update.message.reply_text("Bitch, I need a name")
    return NAME


def get_name(update, context):
    name = update.message.text
    user = update.message.from_user.username

    storage.add_name(user, name)
    update.message.reply_text("Bitch, I need a description")

    return DESC


def get_desc(update, context):
    desc = update.message.text
    user = update.message.from_user.username

    storage.add_desc(user, desc)
    update.message.reply_text("Bitch, I need an image")

    return FILE


def get_file(update, context):
    file = update.message.photo[-1].get_file()
    user = update.message.from_user.username

    name = storage.get_userdata(user)[0] + '.jpg'
    file.download(path.join(asset_folder, name))
    storage.add_image(user, name)

    userdata = storage.get_userdata(user)

    items.add_item(name, userdata[0], userdata[1])
    items.save()

    storage.remove_userdata(user)

    update.message.reply_text("It has been done my dude.")

    return ConversationHandler.END


def cancel(update, context):
    user = update.message.from_user.username
    storage.remove_userdata(user)

    update.message.reply_text("Okay, nevermind then u fucking twat.")

    return ConversationHandler.END


conversation_handler = ConversationHandler(
    entry_points = [CommandHandler('add_entry', start_converstation)],
    fallbacks    = [CommandHandler('cancel', cancel)],
    states = {
        NAME: [MessageHandler(Filters.text & ~Filters.command, get_name)],
        DESC: [MessageHandler(Filters.text & ~Filters.command, get_desc)],
        FILE: [MessageHandler(Filters.photo, get_file)]
    }
)