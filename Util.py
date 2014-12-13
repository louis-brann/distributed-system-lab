# 
# Ben Goldberg and Louis Brann 
# Networks Lab 6 - Distributed System
# Utility library

import json

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

	# Package the message as a JSON string
	def make_json(self):
		json_dict = {"msg_type": self.msg_type, 
		             "action": self.action, 
		             "payload": self.payload,
		             "timestamp": self.timestamp,
		             "source": self.source}
		return json.dumps(json_dict)

	def __repr__(self):
		return "msg_type: " + self.msg_type + 
				"\naction: " + self.action +
				"\npayload: " + self.payload +
				"\ntimestamp: " + self.timestamp +
				"\nsource: " + self.source


