from time import time

class Message_Payload:
    def __init__(self, receiver, message, client_ip):
        self.sender = client_ip
        self.receiver = receiver
        self.timestamp = time()
        self.message = message

    def toDict(self):
        return {
            "sender": self.sender,
            "receiver": self.receiver,
            "timestamp": self.timestamp,
            "message": self.message
        }
