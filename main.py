from math import ceil

from telegram import InputFile, error
from telegram.ext import Updater, ConversationHandler

from common import *
from utils import *
from items import *
from history import *
import add_item

import json
import os
import time
import os.path as path


with open(path.join(asset_folder, 'token.txt'), 'r') as token_file:
    token = token_file.read()

updater    = Updater(token = token, use_context = True)
dispatcher = updater.dispatcher
job_queue  = updater.job_queue
jobs       = dict()


def do_revolve(chat_id):
    bot = updater.bot


    file, (name, desc) = items.random_item()
    while not hist_allows(chat_id, name):
        file, (name, desc) = items.random_item()

    hist_insert(chat_id, name)
    save_hist()


    with open('./assets/' + file, 'rb') as f:
        try:
            bot.set_chat_photo(chat_id, InputFile(f, filename = name))
            bot.setChatTitle(chat_id, name)
            bot.setChatDescription(chat_id, desc + '\n\nDiscord: https://discord.gg/jjaFNAN')
        except error.BadRequest:
            # TG will throw BadRequest when the title / description are unchanged.
            bot.send_message(chat_id = chat_id, text = "The flames of revolution shall burn another day.")
            return

    jobs[chat_id][2] = time.time()
    save_job_queue()

    bot.send_message(chat_id = chat_id, text = "The king is dead, long live the king!")


def save_job_queue():
    job_data = dict(map(
        lambda kv: (kv[0], (kv[1][1], kv[1][2])),
        jobs.items()
    ))

    dest = path.join(asset_folder, 'jobs.json')

    with open(dest, 'w') as handle:
        json.dump(job_data, handle, indent = 4)


def load_job_queue():
    src = path.join(asset_folder, 'jobs.json')
    if not path.exists(src): return

    with open(src, 'r') as handle:
        job_data = json.load(handle)

        for chat_id, (interval, last_trigger) in job_data.items():
            chat_id = int(chat_id)

            next_trigger = max(last_trigger + interval - time.time(), 0)
            print('last = ' + str(last_trigger) + '\nnow  = ' + str(time.time()))
            print('next = ' + str(next_trigger) + ', dt = ' + str(interval))
            job = job_queue.run_repeating(
                lambda ctx: do_revolve(chat_id),
                interval,
                next_trigger
            )

            jobs[chat_id] = [job, interval, next_trigger]


def on_revolve(update, context):
    do_revolve(update.effective_chat.id)


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


def on_auto(update, context):
    chat_id  = update.effective_chat.id
    interval = 0
    delta_start = 0

    args = update.message.text.split(' ')[1:]

    try: interval = float(args[0])
    except (ValueError, IndexError):
        send_reply(update, context, "I need a number you fuckface.")
        return

    try: delta_start = float(args[1])
    except ValueError:
        send_reply(update, context, "Don't give me a second argument if it's not gonna be a number, idiot.")
        return
    except IndexError:
        delta_start = interval


    if chat_id in jobs: jobs[chat_id][0].schedule_removal()

    job = job_queue.run_repeating(
        lambda ctx: do_revolve(chat_id),
        interval,
        delta_start
    )

    reverse_offset = interval
    while reverse_offset < delta_start: reverse_offset += interval

    jobs[chat_id] = [job, interval, time.time() - reverse_offset + delta_start]

    send_reply(update, context, "I'll annoy you every " + str(interval) + " seconds.")

    print('store @ ' + str(time.time()) + ' with ds = ' + str(delta_start))

    save_job_queue()


def on_noauto(update, context):
    chat_id = update.effective_chat.id

    if chat_id in jobs:
        jobs[chat_id][0].schedule_removal()
        del jobs[chat_id]
        
        send_reply(update, context, "Aight, I'll shut up.")
    else:
        send_reply(update, context, "I wasn't talking to begin with, faggot.")

    save_job_queue()


def on_disabled(update, context):
    hist_items = '\n'.join(get_hist_items(update.effective_chat.id))
    send_message(update, context, "These nibbas won't show their face around here anytime soon:\n\n" + hist_items)


add_command(dispatcher, on_revolve,     'revolve'  )
add_command(dispatcher, on_list_images, 'list'     )
add_command(dispatcher, on_refresh,     'refresh'  )
add_command(dispatcher, on_del_entry,   'del_entry')
add_command(dispatcher, on_auto,        'auto'     )
add_command(dispatcher, on_noauto,      'no_auto'  )
add_command(dispatcher, on_disabled,    'recent'   )
add_conversation(dispatcher, add_item.conversation_handler)

items.load()
load_job_queue()
load_hist()
updater.start_polling()
