# 
# Ben Goldberg and Louis Brann 
# Networks Lab 6 - Distributed System
# Utility library

import json, socket

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

    def send(self, ip, port):
        """
        Sends message to specified IP address and port over UDP
        """
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        message = self.make_json()
        socket.sendto(message, (ip,port))
        udp_socket.close()

    def receive(self, port):
        """
        Receives message on specified port over UDP
        """
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        upd_socket.bind(("", port))
        packet, addr = udp_socket.recvfrom(1024)
        message = json.loads(packet)
        udp_socket.close()
        return message

    def make_json(self):
        """
        Package the message as a JSON string
        """
        json_dict = {"msg_type": self.msg_type, 
                     "action": self.action, 
                     "payload": self.payload,
                     "timestamp": self.timestamp,
                     "source": self.source}
        return json.dumps(json_dict)

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



