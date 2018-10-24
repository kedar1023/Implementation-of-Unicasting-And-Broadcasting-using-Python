from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

clients = {}
addresses = {}

HOST = "127.0.0.1"
PORT = 5000
BUFSIZ = 1024
ADDR = (HOST, PORT)
SOCK = socket(AF_INET, SOCK_STREAM)
SOCK.bind(ADDR)


def accept_incoming_connections():
    
    while True:
        client, client_address = SOCK.accept()
        print("%s:%s has connected." % client_address)
        client.send("WELCOME TO OUR CHAT SERVER ".encode("utf8"))
        client.send("PLEASE ENTER YOUR NAME IN THE PROVIDED TEXTFILED AND HIT ENTER ".encode("utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client, client_address)).start()


def handle_client(conn, addr): 
   
    name = conn.recv(BUFSIZ).decode("utf8")
	
    welcome = 'Welcome %s! If you ever want to quit, type #quit to exit.' % name
    conn.send(bytes(welcome, "utf8"))
    msg = "%s from [%s] has joined the chat!" % (name, "{}:{}".format(addr[0], addr[1]))
    broadcast(bytes(msg, "utf8"))
    clients[conn] = name
    while True:
        msg = conn.recv(BUFSIZ)
        
        print(msg)
       
        broadcast(msg, name + ": ")
			
       


def broadcast(msg, prefix=""):
    for sock in clients:
            sock.send(bytes(prefix, "utf8") + msg)
def unicast(msg):
    print("unicasted")

if __name__ == "__main__":
    SOCK.listen(5)  
    print("Chat Server has Started !!")
    print("Waiting for connections...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()  
    ACCEPT_THREAD.join()
    SOCK.close()
