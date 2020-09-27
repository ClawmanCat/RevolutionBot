from multiprocessing.connection import Client


address = ('localhost', 420)

def send_revolve_notification(chat_id, chat_name):
    try:
        sender = Client(address)
        sender.send(('name_changed', (chat_id, chat_name)))
    except ConnectionRefusedError:
        # No listeners.
        pass