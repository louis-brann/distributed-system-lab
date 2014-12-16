# 
# Ben Goldberg and Louis Brann 
# Networks Lab 6 - Distributed System
# Utility library

import json
import socket
import random
import Queue

client_port = 6443
server_port = 6442

clients = ['134.173.42.215']
servers = ['134.173.42.9']


class Message:
    """
    Wrapper for JSON message passing between Clients and Servers, and 
    between Servers
    """

    def __init__(self, msg_type="", action="", payload={}, timestamp=0, source=""):
        self.msg_type = msg_type
        self.action = action
        self.payload = payload
        self.timestamp = timestamp
        self.source = source

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
        return self.timestamp

    def __repr__(self):
        return "[msg_type: " + str(self.msg_type) + \
                "\naction: " + str(self.action) + \
                "\npayload: " + str(self.payload) + \
                "\ntimestamp: " + str(self.timestamp) + \
                "\nsource: " + str(self.source) + "]\n"

def message_to_json(message):
        """
        Package the message as a JSON string
        """
        json_dict = {"msg_type": message.msg_type, 
                     "action": message.action, 
                     "payload": message.payload,
                     "timestamp": message.timestamp,
                     "source": message.source}
        return json.dumps(json_dict)

def json_to_message(json_serial):
    json_dict = json.loads(json_serial)
    return Message(json_dict["msg_type"], json_dict["action"], \
              json_dict["payload"], json_dict["timestamp"], json_dict["source"])

def get_server():
    """
    Input: none
    Output: IP of random server
    Side effects: none
    """
    return random.choice(servers)

def send_message(message, ip, port):
    """
    Sends message to specified IP address and port over UDP
    """
    packet = message_to_json(message)
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.sendto(packet, (ip,port))
    udp_socket.close()

def recv_message(port):
    """
    Receives message on specified port over UDP
    """
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(("", port))
    packet, addr = udp_socket.recvfrom(1024)
    udp_socket.close()

    return json_to_message(packet)


class Lock:

    def __init__(self, name):
        self.name = name
        self.owner_ip = ""
        self.queue = Queue.Queue()

    def request(self, requester_ip):
        """
        Input: IP of requester
        Output: Bool for success or failure
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
                self.request(self.queue.pop())
            return True

        else:
            return False









