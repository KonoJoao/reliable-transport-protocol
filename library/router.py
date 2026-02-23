import json
from library.colored_print import colored_print, Colors, Layers
from library.link import LinkLayer


class NetworkLayer:
    def __init__(self, client_socket):
        self.client_socket = client_socket
        self.link_layer = LinkLayer("00:1A:2B:3C:4D:5E", client_socket)

    def send_message_in_network_layer(self, message_packet):
        self.decrement_ttl(message_packet)
        packet_dict = message_packet.to_dict()

        server_virtual_dest = packet_dict['dst_vip']
        addr = self.virtual_table.get(server_virtual_dest)

        if addr is None:
            colored_print("Servidor não encontrado pelo nome", Colors.AMARELO)
            raise Exception("Address for the server name not found")

        dest_ip = addr['ip']
        dest_port = addr['port']

        self.link_layer.send_data_in_link_layer(packet_dict, (dest_ip, dest_port))

    def decrement_ttl(self, message_packet):
        message_packet.ttl -= 1

        if message_packet.ttl <= 0:
            colored_print('TTL do pacote excedido', Colors.AMARELO, layer=Layers.REDE)
            raise Exception("TTL do pacote excedido")

    def decrement_dict_ttl(self, message_packet):
        message_packet['ttl'] -= 1

        if message_packet['ttl'] <= 0:
            colored_print('TTL do pacote excedido', Colors.AMARELO, layer=Layers.REDE)
            raise Exception("TTL do pacote excedido")

    def return_transport_layer_data(self, message_frame):
        message_packet = self.link_layer.return_network_layer_data(message_frame)

        if(message_packet == None):
            return message_packet

        colored_print(message_packet, Colors.AMARELO, layer=Layers.REDE)
        self.decrement_dict_ttl(message_packet)

        return message_packet['data']


    virtual_table = {
        'server': {"ip": "127.0.0.1", "port": 12000},
        'client': {"ip": "127.0.0.1", "port": 12001}
    }