# 
# Ben Goldberg and Louis Brann 
# Networks Lab 6 - Distributed System
# Server library

import Queue
import json

client_port = 6443

class Server:
    """
    A server node in a distributed system that can create
    and manage ints, locks, and barriers
    """

    def __init__(self, clients, servers, my_ip):
        self.ints = {}
        self.locks = {}
        self.barriers = {}
        self.timestamps = {}
        self.message_queue = Queue.PriorityQueue()

        self._clients = clients
        self._servers = servers
        self._my_ip = my_ip
        self._current_time = 0

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
                process_one_message(next_message)

    def process_one_message(self, message):
        if message.msg_type.equals("int"):
            new_message = process_int(message)
        elif lock:
            new_message = process_lock(message)
        elif barrier:
            new_message = process_barrier(message)
        else:
            new_message = message
            message_success = false

        if source in clients:
            dest = message.source
            message.source = self._my_ip
            message.send(dest, client_port)


    def add_message(self, message):
        """
        Parses a Message object and appropriately adds it to Server
        """
        self._current_time += 1

        if message.source in self._clients:
            self.timestamps[self._my_ip] = self._current_time
            self.message_queue.put(message)

        if message.source in self._servers:
            self.timestamps[message.source] = message.timestamp
            self.message_queue.put(message)

    def process_int(self, message):
        """
        Input: Received message that needs to be processed
        Output: Same message modified to reflect success status and data as 
                appropriate
        Side effects: self.ints modified as appropriate
        """
        message_success = False
        int_name = message.payload["name"]
        int_value = message.payload["value"]

        # Create
        if message.action.equals("create"):
            message_success = int_name not in self.ints.keys()
            if message_success:
                self.ints[int_name] = int_value

        # Get
        elif message.action.equals("get"):
            message_success = int_name in self.ints.keys()
            if message_success:
                message.payload["value"] = self.ints[int_name]

        # Set 
        elif message.action.equals("set"):
            message_success = int_name in self.ints.keys()
            if message_success:
                self.ints[int_name] = int_value

        # Destroy 
        elif message.action.equals("destroy"):
            message_success = int_name in self.ints.keys()
            if message_success:
                del self.ints[int_name]

        else:
            # TODO: Handle?
            print "Undefined operation"

        # Update success status
        message.payload["flag"] = message_success
        return message

    def process_lock(self, messsage):
        print "locks"
        if message.action.equals("create"):
        elif message.action.equals("request"):
        elif message.action.equals("destroy"):

    def process_barrier(self, message):
        print "barriers"
        if message.action.equals("create"):
        if message.action.equals("wait"):




