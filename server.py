import socket
import threading
import time



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverRunning = True
ip = str(socket.gethostbyname(socket.gethostname()))
port = 1234

clients = {}

s.bind(('127.0.0.1', port))
s.listen()
print('-------------------------------------SERVER STARTED---------------------------------------------------\nwith ip address:%s\n'%ip)

localtime = time.asctime( time.localtime(time.time()) )
print ("------------------------------------------------------------------------------------------------------SERVER STARTED AT::", localtime)

def handleClient(client, uname):
    clientConnected = True
    keys = clients.keys()
    help = ' -----------------------------------------------------------------------------------------------------TO USE OUR APPLICATION PLEASE REFER FOLLOWING STEPS:\n A...FOR SENDING MESSAGE TO ALL CLIENTS (THAT MEANS BROADCASTING) PLEASE REFER THIS COMMAND...\n#toall message \t For Example: #toall hi\nB...FOR SENDING THE MESSAGE TO SINGLE(INTENDED) ONLY PLEASE REFER THIS COMMAND...\n@username message\t For Example: @user1 hi\nC...TO EXIT FROM OUR APPLICATION TYPE #exitapp it will disconnect you from server\nD...TO SEE WHO USES THIS APPLICATION THIS TIME USE THIS COMMAND\T#showconnectedusers\n-------------------------------------------ENJOY THE SERVICE------------------------------------------\n'

    while clientConnected:
        try:
            msg = client.recv(1024).decode('ascii')
            response = 'CONNECTED USERS TO OUT CHAT SERVER ARE :\n'
            found = False
            if '#showconnectedusers' in msg:
                clientNo = 0
                for name in keys:
                    clientNo += 1
                    response = response + str(clientNo) +'\t:' + name+'\n'
                client.send(response.encode('ascii'))
            elif '#showmanual' in msg:
                client.send(help.encode('ascii'))
            elif '#toall' in msg:
                msg = msg.replace('#toall','')
                for k,v in clients.items():
                    v.send(msg.encode('ascii'))
            elif '#exitapp' in msg:
                response = 'CLIENT IS DISCONNECTED'
                client.send(response.encode('ascii'))
                clients.pop(uname)
                localtime = time.asctime( time.localtime(time.time()) )
                 
                print(uname + ' LEFT THE MESSANGER AT %s'%localtime)
                print('\n------------------------------------------------------------------------------------------------------\n')
                clientConnected = False
            else:
                for name in keys:
                    if('@'+name) in msg:
                        msg = msg.replace('@'+name, '')
                        clients.get(name).send(msg.encode('ascii'))
                        found = True
                if(not found):
                    client.send('OOPS.....INVALID USERNAME....PLEASE TRY INTENDED ONLY'.encode('ascii'))
        except:
            clients.pop(uname)
            localtime = time.asctime( time.localtime(time.time()) )
            print(uname + ' LEFT THE CHAT AT %s'%localtime)
            print('\n------------------------------------------------------------------------------------------------------\n')
            clientConnected = False


        


while serverRunning:
    client, address = s.accept()
    uname = client.recv(1024).decode('ascii')
    localtime = time.asctime( time.localtime(time.time()) )
    print('------------------------------------------------------------------------------------------------------%s connected to the server'%str(uname))
    print('at time of %s'%localtime)
    print('------------------------------------------------------------------------------------------------------')
    client.send('------------------------------------------------------------------------------------------------------HEY USER ...\nYOU ARE CONNECTED TO OUR MULTICLIENT CHAT SERVER\nTO KNOW THE MANUAL OF HOW TO USE THIS APPLICATION PLEASE PRESS #showmanual'.encode('ascii'))
    
    if(client not in clients):
        clients[uname] = client
        threading.Thread(target = handleClient, args = (client, uname, )).start()
        
