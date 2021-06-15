import socket, threading
import time


HOST = "Localhost"
PORT = 9000



robot = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
robot.connect((HOST, PORT))
robot.send(str("register;ajt").encode())

while 1: 
    msg = robot.recv(2048)
    print(msg.decode())
