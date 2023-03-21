import socket
import threading
import tkinter

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

    output_area = tkinter.Text(root, state="disabled")
    input_area = tkinter.Entry(root)

    def send_message():
        global host, PORT, ADDRESS, FORMAT, client, server_connected
        message = input_area.get()
        input_area.delete(0, 'end')
        client.send(message.encode(FORMAT))

    def connect_to_server():
        global host, PORT, ADDRESS, FORMAT, client, server_connected
        host_ip = input_area.get()
        input_area.delete(0, 'end')
        ADDRESS = (host_ip, PORT)
        try:
            client.connect(ADDRESS)
            connect_button.destroy()
            server_connected = True
            input_area.bind("<Return>", lambda send_event: send_message())
        except:
            output_area.config(state="normal")
            output_area.insert(tkinter.END, "Invalid IP Address\n")
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

    root.protocol("WM_DELETE_WINDOW", on_closing)

    send_button = tkinter.Button(root, text='Send', command=send_message)
    connect_button = tkinter.Button(
        root, text='Connect', command=connect_to_server)

    output_area.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
    input_area.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="EW")
    send_button.grid(row=2, column=0, padx=5, pady=5)
    connect_button.grid(row=2, column=0, padx=5, pady=5)

    recieve_thread = threading.Thread(target=recieve_messages)
    recieve_thread.start()

    root.mainloop()


logo_screen()
main_window()
