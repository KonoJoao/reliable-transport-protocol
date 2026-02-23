# Projeto de Protocolo de Transporte Confiável

## Pré-requisitos

- Python 3.13.1 instalado
- Sistema operacional: Windows/Linux/MacOS

## Como executar

### 1. Inicie o servidor primeiro

Abra um terminal e navegue até a pasta do servidor:

cd server
python chat-server.py

Você verá a mensagem:
The server is ready to receive
Aguardando pacotes na porta 12000...

### Inicie o cliente

Abra outro terminal (mantenha o servidor rodando) e navegue até a pasta do cliente:

cd client
python chat-client.py

Você verá:
Cliente conectado. Digite 'sair' para encerrar.
📝 Digite uma sentença para envio:

### Como usar

- Digite suas mensagens no terminal do cliente
- O servidor receberá e processará as mensagens
- Para encerrar, digite sair no cliente

## Observações importantes

- Sempre inicie o servidor primeiro antes do cliente
- Use terminais separados para servidor e cliente
- A pasta de library contém dependências tanto do server quanto do client. É de extrema importância sua integridade para que o projeto funcione
- 