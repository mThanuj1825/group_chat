import socket
import threading
import tkinter

host = None  # the host ip address
PORT = 55555  # port on which the hosting is taking place
ADDRESS = None
FORMAT = "utf-8"  # format in which encoding and decoding should take place

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


root = tkinter.Tk()

root.title("Group Chat App")

output_area = tkinter.Text(root, state="disabled")
input_area = tkinter.Entry(root)


def send_message():
    pass


def connect_to_server():
    host_ip = input_area.get()
    input_area.delete(0, 'end')
    ADDRESS = (host_ip, PORT)
    client.connect(ADDRESS)
    connect_button.destroy()


def receive_messages():
    while True:
        msg = client.recv(1024).decode(FORMAT)
        output_area.insert(tkinter.END, msg)


send_button = tkinter.Button(root, text='Send', command=send_message)
connect_button = tkinter.Button(
    root, text='Connect', command=connect_to_server)

output_area.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
input_area.grid(row=1, column=0, padx=5, pady=5)
send_button.grid(row=1, column=1, padx=5, pady=5)
connect_button.grid(row=2, column=0, padx=5, pady=5)


recieve_thread = threading.Thread(target=receive_messages)
recieve_thread.start()


root.mainloop()
