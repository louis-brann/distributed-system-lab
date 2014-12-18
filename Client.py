# 
# Ben Goldberg and Louis Brann 
# Networks Lab 6 - Distributed System
# Client library

from Util import *

class Client:
    """
    This client class as given can operate on three datatypes, Ints, Locks, or 
    Barriers. The client leverages the Util library to send the desired
    operations to a Server, which maintains the state of these operations.
    Each client can be identified by their IP, which means that this class can 
    only support one client per machine. 
    """

    def __init__(self, ip):
        self.ip = ip

    def int_create(self, name, value=0):
        """
        Input: name of int to create as a string, optional initial value
        Output: Message type indicating processing of request
        Details: 
        """
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
        """
        Details: If another client owns the lock, hangs until the lock is 
                 available
        """
        return self.action('lock', 'request', name)

    def lock_release(self, name):
        return self.action('lock', 'release', name)

    def lock_destroy(self, name):
        return self.action('lock', 'destroy', name)

    def barrier_create(self, name):
        return self.action('barrier', 'create', name)

    def barrier_wait(self, name):
        """
        Details: If this client is not the last to wait on the barrier, it 
                 hangs until all clients subscribed to the barrier are waiting
        """
        return self.action('barrier', 'wait', name)

    def action(self, obj_type, action, name, value=0):
        server_ip = get_server()
        message = Message(obj_type, action, {'name':name, 'value':value, 'flag':False}, 0, self.ip, self.ip)
        send_message(message, server_ip, c_to_s_port)

        # Blocking listen for a response
        return recv_message(s_to_c_port)
