import socket
from threading import Thread
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from ftplib import FTP
import os
import ntpath
from tkinter import filedialog

IP_ADDRESS = '127.0.0.1'
PORT = 8050
SERVER = None
BUFFER_SIZE = 4096
clients = {}

def ftp_server_setup():
    global IP_ADDRESS

    authorizer = DummyAuthorizer()
    authorizer.add_user("lftpd", "lftpd", ".", perm="elradfmw")

    handler = FTPHandler
    handler.authorizer = authorizer

    ftp_server = FTPServer((IP_ADDRESS, 21), handler)
    ftp_server.serve_forever()

def setup():
    print("\n\t\t\t\t\t\tIP MESSENGER\n")

    global PORT
    global IP_ADDRESS
    global SERVER

    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.bind((IP_ADDRESS, PORT))

    SERVER.listen(100)

    print("\t\t\t\tSERVER IS WAITING FOR INCOMING CONNECTIONS...")
    print("\n")

    acceptConnections()

def acceptConnections():
    global SERVER
    global clients

    while True:
        client, addr = SERVER.accept()
        client_name = client.recv(BUFFER_SIZE).decode().lower()
        clients[client_name] = {
            "client": client,
            "address": addr,
            "connected_with": "",
            "file_name": "",
            "file_size": BUFFER_SIZE,
        }
        print(f"Connection established with {client_name} : {addr}")

        thread = Thread(target=handleClient, args=(client, client_name))
        thread.start()

def browseFiles():
    try:
        filename = filedialog.askopenfilename()
        HOSTNAME = "127.0.0.1"
        USERNAME = "lftpd"
        PASSWORD = "lftpd"

        ftp_client = FTP(HOSTNAME, USERNAME, PASSWORD)
        ftp_client.encoding = "utf-8"
        ftp_client.cwd("shared_files")
        fname = ntpath.basename(filename)
        with open(filename, "rb") as file:
            ftp_client.storbinary(f"STOR {fname}", file)

        ftp_client.dir()
        ftp_client.quit()

        global listbox

        listbox.insert(song_counter, fname)
        song_counter = song_counter + 1
    
    except FileNotFoundError:
        print("Cancel Button Pressed")

def download():
    song_to_download = listbox.get(ANCHOR)
    infolabel.configure(text = "Downloading "+ song_to_download)

    HOSTNAME = "127.0.0.1"
    USERNAME = "lftpd"
    PASSWORD = "lftpd"

    home = str(Path.home())
    download_path = home+"/Downloads"
    ftp_server = ftplib.FTP(HOSTNAME, USERNAME, PASSWORD)
    ftp_server.encoding = "utf-8"
    ftp_server.cwd("shared_files")
    local_filename = os.path.join(download_path, song_to_download)
    file = open(local_filename, "wb")
    ftp_server = retrbinary("RETR"+ song_to_download, file.write)
    ftp_server.dir()
    ftp_server.close()
    ftp_server.quit()
    infoLabel.configure(text = "Download Complete")
    time.sleep(1)

    if(song_selected != ""):
        infoLabel.configure(text = "Now Playing" +song_selected)
    else:
        infoLabel.configure(text = "")

def handleClient(client, client_name):
    pass  # Define your logic for handling client communication

is_dir_exists = os.path.isdir("shared_files")
print(is_dir_exists)
if (not is_dir_exists):
    os.makedirs("shared_files")

# Starting the setup and FTP server threads
setup_thread = Thread(target=setup)
setup_thread.start()

ftp_thread = Thread(target=ftp_server_setup)
ftp_thread.start()