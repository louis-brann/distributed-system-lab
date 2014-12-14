import Util
import Server

def main():
    clients = []
    servers = ['12.13.14.15','16.17.18.19']
    my_ip = '16.17.18.19'

    msg1 = Util.Message("int","create",{"name":"Bob", "value":5, "flag":0},0,'12.13.14.15')
    msg2 = Util.Message("int","get",{"name":"Bob", "value":0, "flag":0},1,'16.17.18.19')

    my_serv = Server.Server(clients, servers, my_ip)
    my_serv.add_message(msg1)
    my_serv.add_message(msg2)
    print "timestamps: ", my_serv.timestamps

    # Manually update timestamps for processing
    my_serv.timestamps[msg1.source] = 3
    my_serv.timestamps[msg2.source] = 3
    my_serv.process_messages()

if __name__ == '__main__':
    main()