import Util
import Server

def main():
    clients = []
    servers = ['12.13.14.15','16.17.18.19']
    my_ip = '16.17.18.19'

    msg1 = Util.Message(0,0,0,0,'12.13.14.15')
    msg2 = Util.Message(1,1,1,1,'16.17.18.19')

    my_serv = Server.Server(clients, servers, my_ip)
    my_serv.add_message(msg1)
    my_serv.add_message(msg2)
    print my_serv.timestamps

    msg3 = Util.Message(2,2,2,2,'12.13.14.15')
    my_serv.process_messages()
    my_serv.add_message(msg3)
    my_serv.process_messages()

if __name__ == '__main__':
    main()