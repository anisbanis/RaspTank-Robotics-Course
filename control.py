# -*- coding: utf-8 -*-
"""
Created on Thu May 27 23:02:49 2021

@author: ASUS
"""
from pynput.keyboard import Key, Listener


import socket, threading
import time
from random import randrange
from pynput.keyboard import Key, Listener
import sys



HOST = "192.168.1.1"
PORT = 9000

commands = {"forward","backward","left","right","stop","speed"}

controller = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
controller.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
controller.connect((HOST, PORT))
controller.send("connect robotajt".encode())


controller.send(str("speed 50").encode())

speed = 50
last_cmd= ""
while True :
    def on_press(key):
        print('{0} pressed'.format(
            key))
        global last_cmd
        global speed
        try:
            if key==Key.up:
                controller.send(str("forward").encode())
                if last_cmd == "forward":
                    speed+=10
                    controller.send(("speed " + str(speed)).encode())
                last_cmd= "forward"
            elif key==Key.down:
                controller.send(str("backward").encode())
                if last_cmd == "backward":
                    speed-=10
                    controller.send(("speed " + str(speed)).encode())
                last_cmd= "backward"
            elif key==Key.left:
                controller.send(str("left").encode())
                
            elif key==Key.right:
                controller.send(str("right").encode())
                
            elif key==Key.enter:
                speed+=10
                controller.send(str("speed "+speed).encode())
                
            elif key==Key.esc:
                controller.send(str("stop").encode())
                
        except AttributeError:
            sys.exit()

    def on_release(key):
        print('{0} release'.format(
            key))
        if key == Key.esc:
        # Stop listener
           return False

# Collect events until released
    with Listener(
        on_press=on_press,
        on_release=on_release) as listener:
        listener.join()
