# Group#: 4
# Student Names: Katie Goncalves & Sant Sumetpong

# Content of client.py; to complete/implement

from tkinter import *
import socket
import threading
from multiprocessing import current_process  # only needed for getting the current process name

class ChatClient:
    """
    This class implements the chat client.
    It uses the socket module to create a TCP socket and to connect to the server.
    It uses the tkinter module to create the GUI for the chat client.
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
        sets up client socket 
        """
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))
        threading.Thread(target=self.rcvMessages).start()
        
    def sendMessage(self, messageToSend):
        """
        sends a message to server.
        """
        msg = messageToSend
        self.client_socket.sendall(msg.encode('utf-8'))
        
    def rcvMessages(self):
        """
        receives messages from server.
        """
        while True:
            message = self.client_socket.recv(1024).decode('utf-8')
            self.displayMessage(message)
            
    def displayMessage(self, messageToDisplay):
        """
        displays message on gui
        """
        self.chatMessage.insert(END, messageToDisplay + '\n')


def main(): #Note that the main function is outside the ChatClient class
    window = Tk()
    c = ChatClient(window)
    window.mainloop()
    #May add more or modify, if needed 

if __name__ == '__main__': # May be used ONLY for debugging
    main()