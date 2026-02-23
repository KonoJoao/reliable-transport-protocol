import json
from threading import Thread, Lock
from library.colored_print import colored_print, Colors, Layers
from library.protocol import Segmento, Pacote
from library.router import  NetworkLayer
from library.timeout import wait_response_with_timeout
import time  # <-- IMPORTANTE: adicionar time

class TransportLayer:
    def __init__(self, buffer, client_socket, host_name, dest_name):
        self.buffer = buffer
        self.buffer_lock = Lock()
        self.host_name = host_name
        self.dest_name = dest_name
        self.client_socket = client_socket
        self.current_seq_number = 0
        self.network_layer = NetworkLayer(client_socket)
        self.running = True  # <-- ADICIONAR FLAG

    def start_send_data_thread_loop(self):
        t1 = Thread(target=self.send_data_thread_loop)
        t1.start()

    def send_data_thread_loop(self):
        while self.running:  # <-- USAR FLAG
            item_to_send = None
            with self.buffer_lock:
                if len(self.buffer) > 0:
                    item_to_send = self.buffer[0]  # <-- PEGA REFERÊNCIA, NÃO PROCESSA AQUI

            if item_to_send:
                self.send_data_in_transport_layer(item_to_send)
            else:
                time.sleep(0.1)  # <-- PAUSA PARA NÃO SOBRECARREGAR CPU

    def send_data_in_transport_layer(self, dict_data, retry_number = 0):
        if retry_number == 3:
            self.increment_seq_num_and_pop_buffer()
            return colored_print("Número máximo de tentativas excedido", Colors.VERMELHO, layer=Layers.TRANSPORTE)

        is_ack = dict_data['is_ack']
        segment = Segmento(self.current_seq_number, is_ack, dict_data['data'])
        segment_dict = segment.to_dict()
        packet = Pacote(self.host_name, self.dest_name, 5, segment_dict)

        self.network_layer.send_message_in_network_layer(packet)

        if is_ack:
            self.increment_seq_num_and_pop_buffer()
            return None

        response = wait_response_with_timeout(self.client_socket, 5)

        resend_data = False if (response is not None) else True

        if response is not None:
            resend_data = self.verify_segment_response(response)
            return None

        if resend_data:
            colored_print('Servidor não confirmou dentro do tempo limite.', Colors.VERMELHO, layer=Layers.TRANSPORTE)
            self.send_data_in_transport_layer(dict_data, retry_number + 1)
            return None

    def verify_segment_response(self, response):
        try:
            extracted_segment = self.network_layer.return_transport_layer_data(response)
            colored_print(extracted_segment, Colors.VERMELHO, layer=Layers.TRANSPORTE)

            if(extracted_segment is None):
                return True

            if extracted_segment['is_ack'] and extracted_segment['seq_num'] == self.current_seq_number:
                self.increment_seq_num_and_pop_buffer()
                return False

        except json.decoder.JSONDecodeError:
            return True

    def increment_seq_num_and_pop_buffer(self):
        if(len(self.buffer) > 0):
            with self.buffer_lock:
                self.buffer.pop(0)
                self.current_seq_number = 1 if self.current_seq_number == 0 else 0