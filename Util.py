# 
# Ben Goldberg and Louis Brann 
# Networks Lab 6 - Distributed System
# Utility library

import json
import socket
import random
import Queue

# Server configuration and retrieval
c_to_s_port = 6443
s_to_s_port = 6442
s_to_c_port = 6441

clients = ['134.173.42.215', '134.173.42.214']
servers = ['134.173.42.9', '134.173.42.4']

def get_server():
    """
    Input: none
    Output: IP of random server
    """
    return random.choice(servers)

# Message class
class Message:
    """
    Wrapper for JSON message passing between Clients and Servers, and 
    between Servers
    """

    def __init__(self, msg_type="", action="", payload={}, timestamp=0, orig_src = "", last_src=""):
        self.msg_type = msg_type
        self.action = action
        self.payload = payload
        self.timestamp = timestamp
        self.orig_src = orig_src
        self.last_src = last_src

    # Rich comparison operators
    def __eq__(self, other):
        return not self<other and not other<self
    def __ne__(self, other):
        return self<other or other<self
    def __gt__(self, other):
        return other.timestamp<self.timestamp
    def __ge__(self, other):
        return not self.timestamp<other.timestamp
    def __le__(self, other):
        return not other.timestamp<self.timestamp

    def __key__(self):
        """
        timestamps are used for message comparison
        """
        return self.timestamp

    def __repr__(self):
        return "[msg_type: " + str(self.msg_type) + \
                "\naction: " + str(self.action) + \
                "\npayload: " + str(self.payload) + \
                "\ntimestamp: " + str(self.timestamp) + \
                "\norig_src: " + str(self.orig_src) + \
                "\nlast_src: " + str(self.last_src) + "]\n"

def message_to_json(message):
    """
    Input: A message object
    Output: That message object packaged as ready-to-send JSON
    """
    json_dict = {"msg_type": message.msg_type, 
                 "action": message.action, 
                 "payload": message.payload,
                 "timestamp": message.timestamp,
                 "orig_src": message.orig_src,
                 "last_src": message.last_src}
    return json.dumps(json_dict)

def json_to_message(json_serial):
    """
    Input: A message object packed as a JSON string
    Output: The message object
    """
    json_dict = json.loads(json_serial)
    return Message(json_dict["msg_type"], json_dict["action"], \
              json_dict["payload"], json_dict["timestamp"], \
              json_dict["orig_src"], json_dict["last_src"])

def send_message(message, ip, port):
    """
    Input: A sendable object, and ip/port information
    Output: None
    Details: Sends message to specified IP address and port over UDP
    """
    packet = message_to_json(message)
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.sendto(packet, (ip,port))
    udp_socket.close()

def recv_message(port):
    """
    Input: A port to listen on
    Output: A message object received on that port over UDP
    Details: Receiving has no timeout. This will hang until a message is received
    """
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(("", port))
    packet, addr = udp_socket.recvfrom(1024)
    udp_socket.close()

    return json_to_message(packet)


# Lock object
class Lock:
    """
    A Lock resource. Can only be owned by one user at a time.
    """

    def __init__(self, name):
        self.name = name
        self.owner_ip = ""
        self.queue = Queue.Queue()

    def request(self, requester_ip):
        """
        Input: IP of requester
        Output: Bool for success or failure
        Details: Requesting will hang if the lock is already owned
        """
        if self.owner_ip == "" or self.owner_ip == requester_ip:
            self.owner_ip = requester_ip
            return True

        else:
            self.queue.put(requester_ip)
            return False
            

    def release(self, releaser_ip):
        """
        Input: IP of releaser
        Output: Bool for success or failure
        """
        if self.owner_ip == releaser_ip:
            self.owner_ip = ""
            if not self.queue.empty():
                self.request(self.queue.get())
            return True

        else:
            return False


# Barrier object
class Barrier:
    """
    A Barrier resource to provide users with synchronization. Users "subscribe" 
    to a barrier. After subscribing, a user can "wait" on a barrier. Barrier
    can say if everyone who subscribed is currently waiting. 
    """

    def __init__(self, name):
        self.name = name
        self.subscribed = []
        self.waiting = []

    def subscribe(self, subscriber_ip):
        """
        Input: IP as a string, 
        Output: True if subscriber added to subscribed list
        """
        if subscriber_ip not in self.subscribed:
            self.subscribed.append(subscriber_ip)
        return True

    def wait(self, waiter_ip):
        """
        Input: IP as a string, 
        Output: True if subscriber added to waiting list
        """
        if waiter_ip in self.subscribed:
            self.waiting.append(waiter_ip)
            return True
        else: 
            return False

    def all_waiting(self):
        """
        Input: None
        Output: True if subscribed list is same as waiting list
        """
        return set(self.subscribed) == set(self.waiting)







