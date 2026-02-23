from json import JSONDecodeError
from socket import *
import json

from library.colored_print import colored_print, Colors, Layers
from library.transport import TransportLayer

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('',serverPort))
data_buffer = []
host_name = 'server'
dest_name = 'client'


class ServerActivities:
    def __init__(self):
        self.transport_layer = TransportLayer(data_buffer, serverSocket, host_name, dest_name)

    def initialize_activities(self):
        colored_print('The server is ready to receive', Colors.VERDE, layer=Layers.APLICACAO)
        while True:
            try:
                self.transport_layer.start_send_data_thread_loop()
                request_data, addr = serverSocket.recvfrom(2048)

                if not request_data:
                    break

                data_buffer.append({"data": {}, 'is_ack': True})
            except JSONDecodeError as e:
                print(f"The server due to a error {e}")

        serverSocket.close()

server_activities = ServerActivities()
server_activities.initialize_activities()