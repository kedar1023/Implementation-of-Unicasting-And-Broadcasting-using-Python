import socket
import threading
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 1234
print("-----------------------------MULTICLIENT CHAT SERVER SYSTEM-------------------------------------------\n-----------------------------ENTER THE CREDENTIALS TO CONNECT TO CHAT SERVER--------------------------")


ip = input('                    ENTER THE IP ADDRESS OF THE TO WHICH YOU WANT TO CONNECT\n                    IP ADDRESS:')
uname = input("                    PLEASE ENTER THE USERNAME WHICH WILL DISPLAYED THROUGHOUT CHATTING\n                    USERNAME:")
try:
    s.connect((ip, port))
except:print("\n\t OOPS LOGIN ERROR ...PLEASE PROVIDE VALID IP ADDRESS OF SERVER\n")
try:
    s.send(uname.encode('ascii'))


    clientRunning = True

    def receiveMsg(sock):
        serverDown = False
        while clientRunning and (not serverDown):
            try:
                msg = sock.recv(1024).decode('ascii')
                print(msg)
            except:
                print('OOPS.........SERVER IS NOW STOPPED....PLEASES HIT ANY BUTTON TO LEAVE THIS APPLCATION.......')
                serverDown = True

    threading.Thread(target = receiveMsg, args = (s,)).start()
    while clientRunning:
        tempMsg = input()
        msg = uname + ' :::>>>' + tempMsg
        if '#exitapp' in msg:
            clientRunning = False
            s.send('#exitapp'.encode('ascii'))
        else:
            s.send(msg.encode('ascii'))

except:print("\n\t OOPS ERROR\n")





    
