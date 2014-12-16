# 
# Ben Goldberg and Louis Brann 
# Networks Lab 6 - Distributed System
# Server library

import Queue
import json
from Util import *
from time import sleep

LOCK_AVAILABLE = 1

class Server:
    """
    A server node in a distributed system that can create
    and manage ints, locks, and barriers
    """

    def __init__(self, clients, servers, my_ip):
        """
        Detail: self.locks is a map from lockname -> IPaddr of owner of lock.
                This value is 0 if nobody owns the lock.
        """
        self.ints = {}
        self.locks = {}
        self.barriers = {}
        self.timestamps = {}
        self.message_queue = Queue.PriorityQueue()

        self._clients = clients
        self._servers = servers
        self._my_ip = my_ip
        self._current_time = 0
        self._lock_queue = Queue.PriorityQueue()

    def process_int(self, message):
        """
        Input: Received message that needs to be processed
        Output: Same message with success-status and payload modified as
                appropriate
        Side effects: self.ints modified as appropriate
        """
        message_success = False
        int_name = message.payload["name"]
        int_value = message.payload["value"]

        # Create
        if message.action == "create":
            message_success = int_name not in self.ints.keys()
            if message_success:
                self.ints[int_name] = int_value

        # Get
        elif message.action == "get":
            message_success = int_name in self.ints.keys()
            if message_success:
                message.payload["value"] = self.ints[int_name]

        # Set 
        elif message.action == "set":
            message_success = int_name in self.ints.keys()
            if message_success:
                self.ints[int_name] = int_value

        # Destroy 
        elif message.action == "destroy":
            message_success = int_name in self.ints.keys()
            if message_success:
                del self.ints[int_name]

        # Invalid Request
        else:
            message_success = False

        # Update success status
        message.payload["flag"] = message_success
        return message

    def process_lock(self, message):
        """
        Input: Received message that needs to be processed
        Output: Same message with success-status and payload modified as
                appropriate
        Side effects: self.locks modified as appropriate
        """
        message_success = False
        lock_name = message.payload["name"]

        # Create
        if message.action == "create":
            message_success = lock_name not in self.locks.keys()
            if message_success:
                self.locks[lock_name] = Lock(lock_name)

        # Request
        elif message.action == "request":
            if lock_name in self.locks.keys():
                message_success = self.locks[lock_name].request(message.source)
                if not message_success:
                    return message_success

        # Release 
        elif message.action == "release":
            if lock_name in self.locks.keys():
                message_success = self.locks[lock_name].release(message.source)
                this_lock = self.locks[lock_name]
                if message_success:
                    # If there's a new owner
                    if this_lock.owner_ip != "":
                        # Send new owner success message
                        request_response = Message('lock', \
                                                   'request', \
                                                   {'name':lock_name, \
                                                    'value':0, \
                                                    'flag':1}, \
                                                    self._current_time, \
                                                    self._my_ip)
                        send_message(request_response, this_lock.owner_ip, client_port)


        # Destroy 
        elif message.action == "destroy":
            message_success = lock_name in self.locks.keys() \
                              and self.locks[lock_name].owner_ip == ""
            if message_success:
                del self.locks[lock_name]

        # Invalid Request
        else:
            message_success = False

        # Update success status
        message.payload["flag"] = message_success
        return message
            
    def process_barrier(self, message):
        """
        Input: Received message that needs to be processed
        Output: Same message with success-status and payload modified as
                appropriate
        Side effects: self.barriers modified as appropriate
        """
        message_success = False
        barrier_name = message.payload["name"]

        # Create
        if message.action == "create":
            if barrier_name not in self.barriers.keys():
                self.barriers[barrier_name] = Barrier(barrier_name)
            message_success = self.barriers[barrier_name].subscribe(message.source)

        # Wait
        if message.action == "wait":
            if barrier_name in self.barriers.keys():
                if self.barriers[barrier_name].wait(message.source):
                    if self.barriers[barrier_name].all_waiting():
                        wait_response = Message('barrier', \
                                                'wait', \
                                                {'name':barrier_name, \
                                                 'value':0, \
                                                 'flag':1}, \
                                                self._current_time, \
                                                self._my_ip)
                        for source in self.barriers[barrier_name].waiting:
                            send_message(wait_response, source, client_port)
                    return False



        # Invalid Request
        else:
            message_success = False

        # Update success status
        message.payload["flag"] = message_success
        return message

    def process_one_message(self, message):
        """
        Input: Message to process
        Output: none
        Side effects: Changes server data based on what Message specified
                      and sends message back if needed
        """
        if message.msg_type == "int":
            new_message = self.process_int(message)

        elif message.msg_type == "lock":
            new_message = self.process_lock(message)
            if not new_message: #"send no response" code
                return

        elif message.msg_type == "barrier":
            new_message = self.process_barrier(message)
            if not new_message: #"send no response" code
                return

        else:
            new_message = message
            message_success = False

        if new_message.source in self._clients:
            dest = new_message.source
            new_message.source = self._my_ip
            send_message(new_message, dest, client_port)

    def process_messages(self):
        """
        Process all messages in the message_queue before the earliest
        entry in timestamps
        """
        min_timestamp = min(self.timestamps.values())

        # While we have messages, and while messages are earlier than timestamp
        while not self.message_queue.empty():
            next_message = self.message_queue.get()
            if next_message.timestamp >=  min_timestamp:
                self.message_queue.put(next_message)
                break
            else:
                self.process_one_message(next_message)

    def add_message(self, message):
        """
        Parses a Message object and appropriately adds it to Server
        """
        self._current_time += 1
        message.timestamp = self._current_time

        if message.source in self._clients:
            self.timestamps[self._my_ip] = self._current_time
            self.message_queue.put(message)

        if message.source in self._servers:
            self.timestamps[message.source] = message.timestamp
            self.message_queue.put(message)

    #def client_listen(self, client_queue):
    def client_listen(self):
        while True:
            message = recv_message(client_port)
            print "Client message received, yo"
            self.add_message(message)
            # TODO: Notify processing thread correctly
            self.process_messages()

            # TODO: Change source and send Message to every other server

    def server_listen(self, server_queue):
        while True:
            message = recv_message(client_port)
            print "Server message received, yo"



    def pinger(self):
        ping_message = Message("ping", "", {}, self._current_time, self._my_ip)
        while True:
            sleep(.5)
            for server in servers:
                # Ping that server to update timestamp
                ping_message.timestamp = self._current_time
                send_message(ping_message, server, server_port)








