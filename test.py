"""
Client basic test code:
-----------------------
import Client
import Util
my_ip = Util.clients[0]
my_client = Client.Client(my_ip)

my_client.int_create("Bob", 5)
my_client.int_set("Bob", 6)
my_client.int_get("Bob")
my_client.int_destroy("Bob")

my_client.barrier_create("Bob")
my_client.barrier_wait("Bob")

my_client.lock_create("Bob")
my_client.lock_request("Bob")
my_client.lock_release("Bob")
my_client.lock_destroy("Bob")


Server test code
-------------------
from Util import *
import Server
import Client
my_serv = Server.Server(clients, servers, servers[0])
my_serv.start()

from Util import *
import Server
import Client
my_serv = Server.Server(clients, servers, servers[1])
my_serv.start()
"""


