import socket
import threading

HOST = socket.gethostbyname(socket.gethostname())  # the host ip address
PORT = 55555  # port on which the hosting is taking place
ADDRESS = (HOST, PORT)
FORMAT = "utf-8"  # format in which encoding and decoding should take place
DISCONNECT = "/dc"
server_running = True

# creates a 'server' socket through which we can communicate further
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# binds the 'server' socket to the given ip address and host port
server.bind(ADDRESS)
server.listen()  # server starts to listen for connections

connected_clients = {}  # dictionary holds the connected clients and their usernames


def broadcast_message(sender_client, message):
    '''
This function is used to broadcast a given message to all the clients in the server using a for loop
It takes 2 arguments
-> the client who is sending the message
-> the message (must be encoded before itself)
    '''
    global connected_clients
    for client in connected_clients:
        if client != sender_client:  # only send message if client is not the sender_client
            client.send(message)


def handle_client(client):
    '''
This function is used to handle the connections with individual clients
-> Recieves the first message as username
-> Infinitely listens for any message recieved by the client
-> Broadcasts the message to all the clients on the server
    '''
    global connected_clients
    # consider the first message sent to the server as a username of the client
    connected = True
    try:
        client.send("Enter your username: ".encode(FORMAT))
        username = client.recv(1024).decode(FORMAT)
        # add an entry of the client with their respective username in the dictionary
        connected_clients[client] = username
        print(f"[NEW CONNECTION] {username} connected.")
        broadcast_message(client, f"[NEW USER] {username} joined the chat room.\n".encode(FORMAT))
    except ConnectionResetError:
        pass

    while connected:  # infinite loop to recieve messages until there is an error or termination of the client socket
        try:  # try recieving a message or else disconnect the client
            message = client.recv(1024).decode(FORMAT)
            if message:  # only if message is not None, we will decode and broadcast it to all the clients
                if message == DISCONNECT:
                    connected = False
                    print(f"[DISCONNECTED] {username} disconnected.")
                    # delete the disconnected ckient entry from the dictionary
                    del connected_clients[client]
                    broadcast_message(client,
                                      f"[SERVER] {username} has left the chat.".encode(FORMAT))  # send the disconnected message to all the clients on the servers
                    print(
                        f"[TOTAL CONNECTIONS] Online users: {threading.active_count() - 3}")  # displays the total number of active / online clients in the server after deletion
                    break
                print(f"[{username}] {message}")
                broadcast_message(
                    client, f"[{username}] {message}".encode(FORMAT))
        except ConnectionResetError:
            connected = False
            print(f"[DISCONNECTED] {username} disconnected.")
            # delete the disconnected client entry from the dictionary
            del connected_clients[client]
            broadcast_message(client,
                              f"[SERVER] {username} has left the chat.".encode(FORMAT))  # send the disconnected message to all the clients on the servers
            print(
                f"[TOTAL CONNECTIONS] Online users: {threading.active_count() - 1}")  # displays the total number of active / online clients in the server after deletion
            break


def server_commands():
    '''
This function handles the stoppage of the server by a specific command
    '''
    global server, connected_clients, server_running
    while True:
        command = input("[COMMAND] ")
        if command == "/tnt":
            server_running = False
            server.close()
            if len(connected_clients) != 0:
                for client in connected_clients:
                    client.close()
            break
        else:
            print("[SERVER] Unknown command")


def main():
    '''
This function is used to run the main loop of the server
-> Accepts new client connections into the server
-> Adds an entry in the clients dictionary
-> Each client is given a thread for parallel processing
-> Can be terminated using keyboardInterrupt
    '''
    global connected_clients, server_running
    while server_running:
        try:
            if not server_running:
                break
            # accept new client connection and returns the client socket and its ip address
            client, client_address = server.accept()
            # adds an entry of the client in the dictionary
            connected_clients[client] = ""

            client_thread = threading.Thread(
                target=handle_client, args=(client, ))  # create a thread for every client addded in the server
            client_thread.start()  # start the client thread for the parallel execution of the clients

            print(
                f"[TOTAL CONNECTIONS] Online users: {threading.active_count() - 3}")  # displays the total number of active / online clients in the server after addition
        except:
            print(f"[SERVER] Stopping the server...")
            print(f"[SERVER] Server closed")


print(f"[SERVER] Server started at {ADDRESS}")
main_thread = threading.Thread(target=main)
main_thread.start()


stop_event = threading.Event()
server_command_thread = threading.Thread(target=server_commands)
server_command_thread.start()
