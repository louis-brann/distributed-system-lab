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

    def __init__(self):
        self.ints = {}
        self.locks = {}
        self.barriers = {}
        self.timestamps = {}
        self.message_queue = Queue.PriorityQueue()

    def process_messages(self):
        """
        Process all messages in the message_queue before the earliest
        entry in timestamps
        """

    def add_message(message):
        """
        Parses a Message object and appropriately adds it to Server
        """

    




