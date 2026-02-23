from library.protocol import Quadro, enviar_pela_rede_ruidosa
from library.colored_print import colored_print, Colors, Layers


class LinkLayer:
    def __init__(self, src_mac, client_socket):
        self.src_mac = src_mac
        self.client_socket = client_socket


    def send_data_in_link_layer(self, packet_dict, addr):
        frame = Quadro(self.src_mac, '00:1A:2B:3C:4D:5F', packet_dict)
        serialized_frame = frame.serializar()

        enviar_pela_rede_ruidosa(self.client_socket, serialized_frame, addr)

    def return_network_layer_data(self, message_frame):
        message_packet, is_frame_ok = Quadro.deserializar(message_frame)

        colored_print(f'Resposta do Servidor\n {message_packet}', Colors.MAGENTA, layer=Layers.ENLACE)

        if(not is_frame_ok):
            colored_print("O quadro recebido está corrompido", Colors.MAGENTA, layer=Layers.ENLACE)
            return None
            # raise Exception("Quadro corrompido")

        return message_packet['data']



