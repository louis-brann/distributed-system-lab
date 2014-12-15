# 
# Ben Goldberg and Louis Brann 
# Networks Lab 6 - Distributed System
# Server library

import Queue
import json
from Util import *


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

        else:
            # TODO: Handle?
            print "Undefined operation"

        # Update success status
        message.payload["flag"] = message_success
        return message

    def process_lock(self, messsage):
        print "locks"
        if message.action == "create":
            print "lock"
        elif message.action == "request":
            print "lock"
        elif message.action == "release":
            print "lock"
        elif message.action == "destroy":
            print "lock"
    def process_barrier(self, message):
        print "barriers"
        if message.action == "create":
            print "barrier"
        if message.action == "wait":
            print "barrier"

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
        elif message.msg_type == "barrier":
            new_message = self.process_barrier(message)
        else:
            new_message = message
            message_success = false

        if message.source in self._clients:
            dest = message.source
            message.source = self._my_ip
            send_message(message, dest, client_port)

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

    def client_listen(self):
        while True:
            message = recv_message(client_port)
            self.add_message(message)
            # TODO: Notify processing thread correctly
            self.process_messages()

            # TODO: Change source and send Message to every other server





