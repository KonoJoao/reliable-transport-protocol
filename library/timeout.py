import socket

from library.colored_print import colored_print, Colors


def wait_response_with_timeout(clientSocket, timeout_time):
    try:
        clientSocket.settimeout(timeout_time)

        response, addr = clientSocket.recvfrom(2048)

        return response
    except socket.timeout:
        colored_print(f"Timeout de {timeout_time}s atingido!", Colors.VERMELHO)
        return None
    except Exception as e:
        colored_print(f"Erro no recebimento: {e}", Colors.VERMELHO)
        return None
    finally:
        clientSocket.settimeout(None)