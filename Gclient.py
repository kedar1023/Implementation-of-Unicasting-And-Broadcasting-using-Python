import tkinter
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


def receive():
    
    while True:
        try:
            msg = sock.recv(BUFSIZ).decode("utf8")
            if ':' in msg:
                username,msg=msg.split(":")
                print(username)
                if '@' in msg:
                    inmsg,inuser=msg.split("@")
                    print(inmsg+"\n")
                    print(inuser)
                    if username==inuser:
                         msg_list.insert(tkinter.END, msg)   
                else:
                    
                    
                    msg_list.insert(tkinter.END, msg)     
            else:
                msg_list.insert(tkinter.END, msg)
                msg = sock.recv(BUFSIZ).decode("utf8")
                if ':' in msg:
                    username,msg=msg.split(":")
                    print(username)
                    if '@' in msg:
                        inmsg,inuser=msg.split("@")
                        print(inmsg+"\n")
                        print(inuser)
                        if username==inuser:
                            msg_list.insert(tkinter.END, inmsg)   
                else:
                    
                    
                    msg_list.insert(tkinter.END, msg)   
               
        except OSError:break

def send(event=None):
   
    msg = my_msg.get()
    my_msg.set("")  
    sock.send(bytes(msg, "utf8"))
    if msg == "#quit":
        sock.close()
        top.quit()

def on_closing(event=None):
  
    my_msg.set("#quit")
    send()
def uni(event=None):
    
    print("unicast");
    msg = my_msg.get()
    print(msg)
    sock.send(bytes(msg,"utf8"))
    

             
top= tkinter.Tk()
top.title("MULTIKCLIENT CHAT SREVER SYSTEM")
messages_frame = tkinter.Frame(top)

my_msg = tkinter.StringVar() 
my_msg.set("")
scrollbar = tkinter.Scrollbar(messages_frame)  
msg_list = tkinter.Listbox(messages_frame, height=15, width=70, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()

messages_frame.pack()

button_label = tkinter.Label(top, text="Enter Message:")
button_label.pack()
entry_field = tkinter.Entry(top, textvariable=my_msg, foreground="green")
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="BROADCAST", command=send,bg="green")
send_button.pack()



quit_button = tkinter.Button(top, text="QUIT", command=on_closing)
quit_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)



HOST = "127.0.0.1"
PORT = 5000
BUFSIZ = 1024
ADDR = (HOST, PORT)
sock = socket(AF_INET, SOCK_STREAM)
sock.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop() 
