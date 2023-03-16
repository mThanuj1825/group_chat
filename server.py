import socket
import threading

HOST = "127.0.0.1"
PORT = 55555
ADDRESS = (HOST, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDRESS)
server.listen()

connected_clients = []


def broadcast_message(message):
    pass


def handle_client(client):
    pass


def main():
    pass
