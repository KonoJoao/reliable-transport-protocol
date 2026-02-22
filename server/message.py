# message.py
import json
from datetime import datetime


class Message:
    def __init__(self, sender, receiver, message, timestamp):
        self.sender = sender
        self.receiver = receiver
        self.message = message
        self.timestamp = timestamp

    @staticmethod
    def validate_message_json(json_data):
        try:
            if not isinstance(json_data, dict):
                return False, "Mensagem não é um dicionário válido", None

            required_fields = ["sender", "receiver", "message", "timestamp"]
            for field in required_fields:
                if field not in json_data:
                    return False, f"Campo obrigatório ausente: {field}", None

            if not isinstance(json_data["sender"], str):
                return False, "Campo 'sender' deve ser string", None

            if not isinstance(json_data["receiver"], str):
                return False, "Campo 'receiver' deve ser string", None

            if not isinstance(json_data["message"], str):
                return False, "Campo 'message' deve ser string", None

            if not isinstance(json_data["timestamp"], (int, float)):
                return False, "Campo 'timestamp' deve ser número (int ou float)", None

            current_time = datetime.now().timestamp()
            if json_data["timestamp"] > current_time + 3600:  # 1 hora no futuro
                return False, "Timestamp está muito no futuro", None

            if json_data["timestamp"] < current_time - 86400 * 7:  # 7 dias no passado
                return False, "Timestamp está muito no passado", None

            message_obj = Message(
                sender=json_data["sender"],
                receiver=json_data["receiver"],
                message=json_data["message"],
                timestamp=json_data["timestamp"]
            )

            return True, "Mensagem válida", message_obj

        except Exception as e:
            return False, f"Erro na validação: {str(e)}", None

    @staticmethod
    def from_json(json_string):
        try:
            data = json.loads(json_string)

            is_valid, error_msg, message_obj = Message.validate_message_json(data)

            if is_valid:
                return True, "Mensagem processada com sucesso", message_obj
            else:
                return False, error_msg, None

        except json.JSONDecodeError as e:
            return False, f"Erro ao decodificar JSON: {str(e)}", None
        except Exception as e:
            return False, f"Erro inesperado: {str(e)}", None

    def to_dict(self):

        return {
            "sender": self.sender,
            "receiver": self.receiver,
            "message": self.message,
            "timestamp": self.timestamp
        }

    def to_json(self):
        return json.dumps(self.to_dict())

    def get_formatted_timestamp(self, format="%Y-%m-%d %H:%M:%S"):
        return datetime.fromtimestamp(self.timestamp).strftime(format)

    def __str__(self):
        return f"Message(from={self.sender}, to={self.receiver}, time={self.get_formatted_timestamp()}, msg='{self.message}')"

    def __repr__(self):
        return self.__str__()