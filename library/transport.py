import json
from threading import Thread, Lock
from socket import *
from library.colored_print import colored_print, Colors, Layers
from library.protocol import Segmento, Pacote
from library.router import  LinkLayer
from library.timeout import wait_response_with_timeout


class TransportLayer:
    def __init__(self, buffer, client_socket, host_name, dest_name):
        self.buffer = buffer
        self.buffer_lock = Lock()
        self.host_name = host_name
        self.dest_name = dest_name
        self.client_socket = client_socket
        self.current_seq_number = 0
        self.link_layer = LinkLayer()

    def start_send_data_thread_loop(self):
        t1 = Thread(target=self.send_data_thread_loop)
        t1.start()

    def send_data_thread_loop(self):
        while True:
            with self.buffer_lock:  # <-- LOCK AQUI
                if len(self.buffer) > 0:
                    self.send_data_in_transport_layer(self.buffer[0])

    def send_data_in_transport_layer(self, dict_data, retry_number = 0):
        if retry_number == 3:
            return colored_print("Número máximo de tentativas excedido", Colors.VERMELHO, layer=Layers.TRANSPORTE)

        is_ack = dict_data['is_ack']
        segment = Segmento(self.current_seq_number, is_ack, dict_data['data'])
        segment_dict = segment.to_dict()
        packet = Pacote(self.host_name, self.dest_name, 5, segment_dict)

        self.link_layer.send_message_in_link_layer(packet, self.client_socket)

        print(self.buffer)
        if is_ack:
            with self.buffer_lock:
                self.buffer.pop(0)
        else:
            response = wait_response_with_timeout(self.client_socket, 5)

            if response is not None:
                colored_print('==============\nResposta do Servidor\n', response, '\n==============\n', Colors.VERDE, layer=Layers.TRANSPORTE)
                response_loaded = json.loads(response)
                extracted_segment = self.link_layer.return_transport_layer_data(response_loaded)
                self.verify_segment_response(extracted_segment)
                return None
            else:
                colored_print('Servidor não confirmou dentro do tempo limite.', Colors.VERMELHO, layer=Layers.TRANSPORTE)
                self.send_data_in_transport_layer(dict_data, retry_number + 1)
                return None
        return None

    def verify_segment_response(self, response_obj):
        print(response_obj)
        if response_obj['is_ack'] and response_obj['seq_num'] == self.current_seq_number:
            with self.buffer_lock:
                self.buffer.pop(0)
                self.current_seq_number = 1 if self.current_seq_number == 0 else 0
