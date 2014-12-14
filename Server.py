# 
# Ben Goldberg and Louis Brann 
# Networks Lab 6 - Distributed System
# Server library

import Queue

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
                #TODO lots
                if int:
                    add to ints
                if lock:
                    add to locks
                if barrier:
                    add to barriers
                if source in clients:
                    send_response_to_client()


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








