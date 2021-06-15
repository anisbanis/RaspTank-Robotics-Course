import socket, threading
import time
from random import randrange

HOST = "Localhost"
PORT = 9000

commands = {"forward","backward","left","right","stop","speed"}
controllers = {}  # robot name/ socket controller 
robots = {} 	#robot name / socket robot 
# connection = {socketspc : socket robot}
bonusmalus  = ["forward","backward","left","right","stop","speed","decelerate","accelerate",]




class ClientThread(threading.Thread):
    def __init__(self, clientAddress, clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        print("New connection added: ", clientAddress)
        self.bonus = 0
        self.malus_time = 0
        self.last_bonus = time.time()
    def run(self):
        print("Connection from : ", clientAddress)
        # self.csocket.send(bytes("Hi, This is from Server..",'utf-8'))
        msg = ""
        global robots
        global controllers
        currentRobotName = None
        
        while True:
            data = self.csocket.recv(2048)
            msg = data.decode()
            if not data:
                break
            try:
                cmd, param = msg.split(";")
            except:
                cmd = msg
            if cmd == "connect":
                print("Received:", param)
                # check the name of robot
                if param not in robots:

                    self.csocket.sendall("Unkhnown".encode())
                else:
                    if param in controllers:
                        self.csocket.sendall(f"Robot {param} is already in use.".encode())
                        #controllers[param] = self.csocket normalement non vu que il est déja relié 
                    else:
                        controllers[param] = self.csocket
                        self.csocket.sendall("ok".encode())
                print(controllers)
                print(robots)

            elif cmd == "register":
                if param in robots:
                    self.csocket.sendall("Robot {param} already registered".encode())
                else:
                    print("Received: ", param)
                    robots[param] = self.csocket

            elif cmd in commands:
                for k, v in controllers.items():
                    if v == self.csocket:
                        currentRobotName = k
                if (currentRobotName):
                    if cmd == "speed":
                        print("Sending forward speed command  to Robot:", currentRobotName)
                        robots[currentRobotName].send(str(msg).encode())                 
                    else:
                        print("Sending forward command to Robot:", currentRobotName)
                        robots[currentRobotName].send(str(cmd).encode())
                else:
                    print("Controller not connected to robot ")


            ##print ("from client", msg)
            if (controllers) :
                print("sss")
                if time.time() - self.last_bonus >= 20 :
                    print("at")
                    name = list(controllers)[randrange(0,len(controllers))]#choisir aléatoirement conrolleur
                    cmd = bonusmalus[randrange(0,len(bonusmalus))]
                    print(cmd)                
                    	
                    for n, r in robots.items():
                        if n == name:
                            #t_end = time.time() + 5
                            #while time.time() < t_end:
                            r.send(str(cmd).encode())
                            break
                    self.last_bonus = time.time()

            self.csocket.send(bytes(msg, "UTF-8"))
        print("Client at ", clientAddress, " disconnected...")


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
Threads = []
print("Server started")
print("Waiting for client request..")




while True:
    server.listen(1)
    clientsock, clientAddress = server.accept()
    newthread = ClientThread(clientAddress, clientsock)
    Threads.append(newthread) 
    
    newthread.start()


