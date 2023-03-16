import socket
import threading

HOST = "127.0.0.1"  # the host ip address
PORT = 55555  # port on which the hosting is taking place
ADDRESS = (HOST, PORT)
FORMAT = "utf-8"  # format in which encoding and decoding should take place

# creates a 'server' socket through which we can communicate further
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# binds the 'server' socket to the given ip address and host port
server.bind(ADDRESS)
server.listen()  # server starts to listen for connections

connected_clients = {}  # dictionary holds the connected clients and their usernames


def broadcast_message(sender_client, message):
    global connected_clients
    for client in connected_clients:
        if client != sender_client:
            client.send(message)


def handle_client(client):
    global connected_clients
    username = client.recv(1024).decode(FORMAT)
    connected_clients[client] = username
    print(f"[NEW CONNECTION] {username} connected.")

    while True:
        try:
            message = client.recv(1024).decode(FORMAT)
            if message:
                print(f"[{username}] {message}")
                broadcast_message(
                    client, f"[{username}] {message}".encode(FORMAT))
        except:
            print(f"[DISCONNECTED] {username} disconnected.")
            del connected_clients[client]
            broadcast_message(client,
                              f"[SERVER] {username} has left the chat.".encode(FORMAT))
            break


def main():
    global connected_clients
    try:
        while True:
            client, client_address = server.accept()
            connected_clients[client] = ""

            client_thread = threading.Thread(
                target=handle_client, args=(client, ))
            client_thread.start()

            print(
                f"[TOTAL CONNECTIONS] Online users: {threading.active_count() - 1}")
    except KeyboardInterrupt:
        print("Server stopped.")
