import json
from library.colored_print import colored_print, Colors, Layers

class LinkLayer:
    def send_message_in_link_layer(self, message_packet, client_socket):
        self.decrement_ttl(message_packet)
        packet_dict = message_packet.to_dict()
        packet_json = json.dumps(packet_dict)
        server_virtual_dest = packet_dict['dst_vip']
        addr = self.virtual_table.get(server_virtual_dest)

        if addr is None:
            colored_print("Servidor não encontrado pelo nome", Colors.RED)
            raise Exception("Address for the server name not found")

        dest_ip = addr['ip']
        dest_port = addr['port']

        # frame = Quadro('12213', dest_port, packet_dict)

        # serialized_frame = frame.serializar()

        client_socket.sendto(packet_json.encode(), (dest_ip, dest_port))

    def decrement_ttl(self, message_packet):
        message_packet.ttl -= 1

        if message_packet.ttl <= 0:
            colored_print('TTL do pacote excedido', Colors.VERDE, layer=Layers.REDE)
            raise Exception("TTL do pacote excedido")

    def return_transport_layer_data(self, message_packet):
        return message_packet['data']


    virtual_table = {
        'server': {"ip": "127.0.0.1", "port": 12000},
        'client': {"ip": "127.0.0.1", "port": 12001}
    }