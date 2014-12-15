# 
# Ben Goldberg and Louis Brann 
# Networks Lab 6 - Distributed System
# Client library

from Util import *

class Client:
    def __init__(self, ip):
        self.ip = ip

    def int_create(name, value=0):
        return int_action('create', name, value)

    def int_get(name):
        return int_action('get', name)

    def int_set(name, value):
        return int_action('set', name, value)

    def int_destroy(name):
        return int_action('destroy', name)

    def int_action(action, name, value=0):
        server_ip = get_server()
        message = Message('int', action, {'name':name, 'value':value, 'flag':0}, 0, self.ip)
        send_message(message, server_ip, client_port)

        # Blocking listen for a response
        return recv_message(client_port)