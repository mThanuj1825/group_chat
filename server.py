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
-> Broadcasts teh message to all the clients on the server
    '''
    global connected_clients
    # consider the first message sent to the server as a username of the client
    username = client.recv(1024).decode(FORMAT)
    # add an entry of the client with their respective username in the dictionary
    connected_clients[client] = username
    print(f"[NEW CONNECTION] {username} connected.")

    while True:  # infinite loop to recieve messages until there is an error or termination of the client socket
        try:  # try recieving a message or else disconnect the client
            message = client.recv(1024).decode(FORMAT)
            if message:  # only if message is not None, we will decode and broadcast it to all the clients
                print(f"[{username}] {message}")
                broadcast_message(
                    client, f"[{username}] {message}".encode(FORMAT))
        except:
            print(f"[DISCONNECTED] {username} disconnected.")
            # delete the disconnected ckient entry from the dictionary
            del connected_clients[client]
            broadcast_message(client,
                              f"[SERVER] {username} has left the chat.".encode(FORMAT))  # send the disconnected message to all the clients on the servers
            print(
                f"[TOTAL CONNECTIONS] Online users: {threading.active_count() - 1}")  # displays the total number of active / online clients in the server after deletion
            break


def main():
    '''
This function is used to run the main loop of the server
-> Accepts new client connections into the server
-> Adds an entry in the clients dictionary
-> Each client is given a thread for parallel processing
-> Can be terminated using keyboardInterrupt
    '''
    global connected_clients
    try:
        while True:
            # accept new client connection and returns the client socket and its ip address
            client, client_address = server.accept()
            # adds an entry of the client in the dictionary
            connected_clients[client] = ""

            client_thread = threading.Thread(
                target=handle_client, args=(client, ))  # create a thread for every client addded in the server
            client_thread.start()  # start the client thread for the parallel execution of the clients

            print(
                f"[TOTAL CONNECTIONS] Online users: {threading.active_count() - 1}")  # displays the total number of active / online clients in the server after addition
    except KeyboardInterrupt:
        print("Server stopped.")
