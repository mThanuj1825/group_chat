import socket
import threading
import tkinter
from tkinter import filedialog
import os

host = None  # the host ip address
PORT = 55555  # port on which the hosting is taking place
ADDRESS = None
FORMAT = "utf-8"  # format in which encoding and decoding should take place

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_connected = False


def logo_screen():
    root = tkinter.Tk()
    logo = tkinter.PhotoImage(file="logo.png")
    root.geometry("653x465")
    root.iconphoto(False, logo)
    root.resizable(False, False)
    label = tkinter.Label(root, image=logo)
    label.pack()
    root.after(2000, root.destroy)
    root.mainloop()


def main_window():
    global host, PORT, ADDRESS, FORMAT, client, server_connected
    root = tkinter.Tk()
    logo = tkinter.PhotoImage(file="logo.png")
    root.geometry("653x465")
    root.iconphoto(False, logo)
    root.resizable(False, False)
    root.title("Group Chat App")

    output_area = tkinter.Text(root)
    output_area.insert(
        tkinter.END, "Welcome to Group Chat\nEnter IP address of the server:")
    output_area.config(state="disabled")
    input_area = tkinter.Entry(root)

    def send_message():
        global host, PORT, ADDRESS, FORMAT, client, server_connected
        message = input_area.get()
        input_area.delete(0, 'end')
        client.send(message.encode(FORMAT))

    def connect_to_server():
        global host, PORT, ADDRESS, FORMAT, client, server_connected
        host_ip = input_area.get()
        output_area.config(state="normal")
        output_area.insert(tkinter.END, f"{host_ip}\n")
        output_area.config(state="disabled")
        input_area.delete(0, 'end')
        ADDRESS = (host_ip, PORT)
        try:
            client.connect(ADDRESS)
            connect_button.destroy()
            server_connected = True
            input_area.bind("<Return>", lambda send_event: send_message())
        except:
            output_area.config(state="normal")
            output_area.insert(
                tkinter.END, "\nInvalid IP Address\nEnter a valid IP Address: ")
            output_area.config(state="disabled")

    def recieve_messages():
        global host, PORT, ADDRESS, FORMAT, client, server_connected
        while True:
            try:
                if client and server_connected:
                    msg = client.recv(1024).decode(FORMAT)
                    if not msg:
                        break
                    output_area.config(state="normal")
                    output_area.insert(tkinter.END, msg)
                    output_area.config(state="disabled")
            except ConnectionAbortedError:
                break

    def on_closing():
        global host, PORT, ADDRESS, FORMAT, client, server_connected
        if client:
            client.close()
        server_connected = False
        root.destroy()
        exit(0)

    def send_file():
        global client, FORMAT
        file_path = filedialog.askopenfilename()
        file_name = os.path.basename(file_path)
        client.send(f"<FILE>{file_name}".encode(FORMAT))

        with open(file_path, "rb") as file:
            while True:
                file_data = file.read(1024)
                if not file_data:
                    break
                client.sendall(file_data)
            client.send(b"<END>")

    root.protocol("WM_DELETE_WINDOW", on_closing)

    send_button = tkinter.Button(root, text='Send', command=send_message)
    connect_button = tkinter.Button(
        root, text='Connect', command=connect_to_server)
    file_button = tkinter.Button(root, text="Send File", command=send_file)

    output_area.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
    input_area.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="EW")
    send_button.grid(row=2, column=0, columnspan=1, padx=5, pady=5)
    connect_button.grid(row=2, column=0, columnspan=1, padx=5, pady=5)
    file_button.grid(row=2, column=1, columnspan=1, padx=5, pady=5)

    recieve_thread = threading.Thread(target=recieve_messages)
    recieve_thread.start()

    root.mainloop()


logo_screen()
main_window()
