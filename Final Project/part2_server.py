# Group#: 4
# Student Names: Katie Goncalves & Sant Sumetpong

#C ontent of server.py; To complete/implement

from tkinter import *
import socket
import threading

class ChatServer:
    """
    This class implements the chat server.
    It uses the socket module to create a TCP socket and act as the chat server.
    Each chat client connects to the server and sends chat messages to it. When 
    the server receives a message, it displays it in its own GUI and also sents 
    the message to the other client.  
    It uses the tkinter module to create the GUI for the server client.
    See the project info/video for the specs.
    """
    # To implement 
    def __init__(self, guiScreen):
        """
        gui setup
        """
        self.window_open = True
        self.guiScreen = guiScreen
        self.guiSetup()
        self.socketSetUp()
        
    def guiSetup(self):
        """
        sets up GUI
        """
        self.chatMessage = Text(self.guiScreen, height=40)
        self.chatMessage.pack(fill=BOTH , expand=TRUE)

    def socketSetUp(self, host='127.0.0.1', port=11111):  # random/arbitrary port number
        """
        sets up server socket 
        """
        self.clients = []
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)
        print(f"The server is ready to receive on {host}:{port}...")
        threading.Thread(target=self.acceptConnections).start()

    def acceptConnections(self):
        """
        accepts connections
        """
        while self.window_open:
            connection, address = self.server_socket.accept()
            self.clients.append((connection, address))
            threading.Thread(target=self.rcvMessages, args=(connection, address)).start()

     # accept message from client
        # decodes message
        # stores address
        # assign number value to clients
        # multi threading
    def rcvMessages(self, socketConnection, socketAddress):
        """
        receives messages
        """
        while True:
            try:
                message = socketConnection.recv(1024).decode()
                if message:
                    #self.sendMessage(message,socketConnection,socketAddress)
                    self.displayMessage(message)
                    pass
            except Exception:
                print("Failed receiving message from client.")
                self.clients.remove((socketConnection, socketAddress))
                socketConnection.close()
                break
    
    def sendMessage(self, messageToSend, socketConnection, socketAddress):
        """
        send messages to clients
        """
        for client in self.clients:
            if client != socketConnection:
                try:
                    client.send(messageToSend.encode())
                except Exception:
                    self.clients.remove((socketConnection, socketAddress))
                    continue
            
    def displayMessage(self, messageToDisplay):
        """
        displays message on gui
        """
        self.chatMessage.insert(END, messageToDisplay + '\n')
        

def main(): #Note that the main function is outside the ChatServer class
    window = Tk()
    window.title("Server")
    window.geometry('350x400')

    guiLabel1 = Label(window, text = "Chat Server")
    guiLabel1.config(font =("Courier", 12))
    guiLabel1.pack()
    
    ChatServer(window)
    window.mainloop()
    #May add more or modify, if needed

if __name__ == '__main__': # May be used ONLY for debugging
    main()
 