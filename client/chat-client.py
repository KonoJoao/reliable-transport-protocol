from socket import *
import time
from client.message import Message_Payload
from library.colored_print import colored_print, Colors, Layers
from library.transport import TransportLayer

dest_name = 'server'
host_name = 'client'
data_buffer = []
clientSocket = socket(AF_INET, SOCK_DGRAM)

class ClientForm:
    def initialize_form_loop(self):
        colored_print("Cliente conectado. Digite 'sair' para encerrar.", Colors.VERDE_BRIGHT, layer=Layers.APLICACAO)

        clientSocket.bind(('', 12001))

        transport_layer = TransportLayer(data_buffer, clientSocket, host_name, dest_name)

        transport_layer.start_send_data_thread_loop()

        while True:
            try:
                sentence = input('\nDigite uma senteça para envio: ')
                clean_input = sentence.strip()
                message = Message_Payload(dest_name, clean_input, host_name)
                dict_message = message.toDict()

                if clean_input.lower() == 'sair':
                    break

                data_buffer.append({"data": dict_message, 'is_ack': False})

                time.sleep(5)
            except KeyboardInterrupt:
                colored_print("\nCliente encerrado pelo usuário", Colors.AMARELO)
                break
            except Exception as e:
                colored_print(f"Erro: {e}", Colors.VERMELHO)
                break

        clientSocket.close()
        print("Cliente desconectado")

client_form = ClientForm()
client_form.initialize_form_loop()

