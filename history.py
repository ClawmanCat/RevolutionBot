from common import *

import json
import os
import os.path as path


history = dict()    # Server ID => Name[]
hist_limit = 10


def hist_allows(chat_id, name):
    global history, hist_limit

    if chat_id not in history: return True
    else: return name not in history[chat_id]


def hist_insert(chat_id, name):
    global history, hist_limit

    if chat_id not in history: history[chat_id] = []

    history[chat_id].append(name)
    if len(history[chat_id]) > hist_limit: history[chat_id] = history[chat_id][1:]


def load_hist():
    global history, hist_limit

    with open(path.join(asset_folder, 'history.json'), 'r') as handle:
        history = dict(map(
            lambda kv: (int(kv[0]), kv[1]),
            json.load(handle).items()
        ))


def save_hist():
    global history, hist_limit

    with open(path.join(asset_folder, 'history.json'), 'w') as handle:
        json.dump(history, handle, indent = 4)


def get_hist_items(chat_id):
    global history, hist_limit

    if chat_id not in history: return ""
    else: return history[chat_id]