# 
# Ben Goldberg and Louis Brann 
# Networks Lab 6 - Distributed System
# Client library

from Util import *

class Client:
    def __init__(self, ip):
        self.ip = ip

    def int_create(self, name, value=0):
        return self.int_action('create', name, value)

    def int_get(self, name):
        return self.int_action('get', name)

    def int_set(self, name, value):
        return self.int_action('set', name, value)

    def int_destroy(self, name):
        return self.int_action('destroy', name)

    def int_action(self, action, name, value=0):
        server_ip = get_server()
        message = Message('int', action, {'name':name, 'value':value, 'flag':0}, 0, self.ip)
        send_message(message, server_ip, client_port)

        # Blocking listen for a response
        return recv_message(client_port)

    
    def lock_create(self, name):
        return self.lock_action('create', name)

    def lock_request(self, name):
        return self.lock_action('request', name)

    def lock_release(self, name):
        return self.lock_action('release', name)

    def lock_destroy(self, name):
        return self.lock_action('destroy', name)

    def lock_action(self, action, name):
        server_ip = get_server()
        message = Message('lock', action, {'name':name, 'value':0, 'flag':0}, 0, self.ip)
        send_message(message, server_ip, client_port)

        # Blocking listen for a response
        return recv_message(client_port)

    def barrier_create(self, name):
        return self.barrier_action('create', name)

    def barrier_wait(self, name):
        return self.barrier_action('wait', name)

    def barrier_action(self, action, name):
        server_ip = get_server()
        message = Message('barrier', action, {'name':name, 'value':0, 'flag':0}, 0, self.ip)
        send_message(message, server_ip, client_port)

        # Blocking listen for a response
        return recv_message(client_port)
