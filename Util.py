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

    def __init__(self, msg_type, action, payload, timestamp, source):
        self.msg_type = msg_type
        self.action = action
        self.payload = payload
        self.timestamp = timestamp
        self.source = source

    def send(self, socket, ip, port):
        """
        Sends message to specified IP address over UDP
        """

        packet = self.make_json()
        socket.sendto(packet, (ip,port))

    def receive(self, socket, port):
        """
        Receives message on specified socket over UDP
        """

        currentPacket, addr = udpSocket.recvfrom(packetSize)
        return currentPacket

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
        return "[msg_type: " + self.msg_type + \
                "\naction: " + self.action + \
                "\npayload: " + self.payload + \
                "\ntimestamp: " + self.timestamp + \
                "\nsource: " + self.source + "]\n"



