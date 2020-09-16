from common import *

import json
import os
import os.path as path
import shutil
import random


class item_manager:
    def __init__(self):
        # Dict of Filename => (Server name, Server desc)
        self.items = dict()
        self.load()


    def load(self):
        with open(path.join(asset_folder, 'items.json'), 'r') as json_file:
            self.items = dict(map(
                lambda item: (item['file'], (item['name'], item['desc'])),
                json.load(json_file)['items']
            ))


    def save(self):
        shutil.copyfile(
            path.join(asset_folder, 'items.json'),
            path.join(asset_folder, 'items_backup.json')
        )

        with open(path.join(asset_folder, 'items.json'), 'w') as json_file:
            json_data = dict()
            json_data['items'] = list(map(
                lambda item: { "file": item[0], "name": item[1][0], "desc": item[1][1] },
                self.items.items()
            ))

            json.dump(json_data, json_file, indent=4)


    def random_item(self):
        return random.choice(list(self.items.items()))


    def add_item(self, filename, server_name, server_desc, overwrite=True):
        if overwrite or filename not in self.items:
            self.items[filename] = (server_name, server_desc)


    def remove_file(self, filename):
        if filename in self.items:
            del self.items[filename]
            return True

        return False


    def remove_name(self, server_name):
        keys = [k for k, v in self.items.items() if v[0] == server_name]
        for k in keys: del self.items[k]

        return len(keys) > 0


    def get_items(self):
        return self.items

items = item_manager()