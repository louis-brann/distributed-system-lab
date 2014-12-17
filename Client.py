# 
# Ben Goldberg and Louis Brann 
# Networks Lab 6 - Distributed System
# Client library

from Util import *

class Client:
    def __init__(self, ip):
        self.ip = ip

    def int_create(self, name, value=0):
        return self.action('int', 'create', name, value)

    def int_get(self, name):
        return self.action('int', 'get', name)

    def int_set(self, name, value):
        return self.action('int', 'set', name, value)

    def int_destroy(self, name):
        return self.action('int', 'destroy', name)
    
    def lock_create(self, name):
        return self.action('lock', 'create', name)

    def lock_request(self, name):
        return self.action('lock', 'request', name)

    def lock_release(self, name):
        return self.action('lock', 'release', name)

    def lock_destroy(self, name):
        return self.action('lock', 'destroy', name)

    def barrier_create(self, name):
        return self.action('barrier', 'create', name)

    def barrier_wait(self, name):
        return self.action('barrier', 'wait', name)

    def action(self, obj_type, action, name, value=0):
        server_ip = get_server()
        message = Message(obj_type, action, {'name':name, 'value':value, 'flag':False}, 0, self.ip)
        send_message(message, server_ip, c_to_s_port)

        # Blocking listen for a response
        return recv_message(s_to_c_port)
