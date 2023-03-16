import socket
import threading

HOST = "127.0.0.1"
PORT = 55555
ADDRESS = (HOST, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDRESS)
server.listen()

connected_clients = {}


def broadcast_message(message):
    global connected_clients
    for client in connected_clients:
        client.send(message)


def handle_client(client):
    pass


def main():
    global connected_clients
    client, client_address = server.accept()
    connected_clients[client] = ""

    client_thread = threading.Thread(target=handle_client, args=(client, ))
    client_thread.start()
