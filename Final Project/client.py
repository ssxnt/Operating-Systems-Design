# Group#: 4
# Student Names: Katie Goncalves & Sant Sumetpong

# Content of client.py; to complete/implement

from tkinter import *
import socket
import threading
from multiprocessing import current_process  # required for getting the current process name

class ChatClient:
    """
    This class implements the chat client.
    It uses the socket module to create a TCP socket and to connect to the server.
    It uses the tkinter module to create the GUI for the chat client.
    """
    # To implement
    def __init__(self, guiScreen, name=current_process().name):
        """
        Sets up the socket and the GUI

        """
        self.guiScreen = guiScreen #gui window
        self.clientName = name # name of client

        self.socketSetUp() #sets up the socket
        self.guiScreen.title("Client") #creates a title for the gui
        self.clientLabel = Label(self.guiScreen, text=f"{self.clientName} @port#{self.address}", font=("Times New Roman", 12), anchor='w')
        self.clientLabel.pack(fill='x')
        
        # create a frame for more widgets
        self.guiFrame = Frame(self.guiScreen)
        self.guiFrame.pack(fill='x')

        # create label for chat message
        self.chatEntry = Label(self.guiFrame, text="Chat Message:", font=("Times New Roman", 12))
        self.chatEntry.grid(row=0, column=0)

        # create entry box for input
        self.messageEntry = Entry(self.guiFrame, width=30)
        self.messageEntry.grid(row=0, column=1)
        self.messageEntry.bind('<Return>', self.sendMessage) 

        # create chat history label
        self.chatHistoryLabel = Label(self.guiScreen, text="Chat History:", font=("Times New Roman", 12), anchor='w')
        self.chatHistoryLabel.pack(fill='x')

        # create widget to display text
        self.messageHistory = Text(self.guiScreen, state='disabled', font=("Times New Roman", 12))
        self.messageHistory.pack(side='left', fill='both', expand=True)

        # create scrollbar
        self.scroller = Scrollbar(self.guiScreen, command=self.messageHistory.yview)
        self.scroller.pack(side='right', fill='y')
        self.messageHistory['yscrollcommand'] = self.scroller.set

        # close socket if deleting window
        self.guiScreen.protocol("WM_DELETE_WINDOW", self.clientSocket.close)

        # place message in the center for the given client
        self.messageHistory.tag_configure('center', justify='center')

    def socketSetUp(self): 
        """
        Sets up the client socket and connects to server
        """
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #creates a new socket
        self.clientSocket.bind(('localhost', 0)) #bind the socket to the address
        self.connection, self.address = self.clientSocket.getsockname() #return the sockets address
        self.clientSocket.connect((self.connection, 11111)) #connect to a remote socket address
        self.clientRunning = True # set the clientRunning flag high

        threading.Thread(target=self.receiveMessage).start() # start the receive message thread

    def sendMessage(self, event=None):
        """
        Sends a message to the server
        """
        messageEntered = self.messageEntry.get() # get the message from the text entry
        self.messageEntry.delete(0,END) # delete text in box
        messageSending = f'{self.clientName}:{messageEntered}' # reformat message for sending
        self.clientSocket.send(messageSending.encode('utf-8')) # send message by encoding
        self.displayMessage(messageSending, 'center') # display the message in client GUI

    def receiveMessage(self):
        """
        Receives messages from the server and updates the chat message GUI
        """
        while self.clientRunning: #while the client socket is running
            try: 
                messageReceived = self.clientSocket.recv(1024).decode('utf-8') #try to receive and decode ,essage
                self.displayMessage(messageReceived, 'left') #display message
            except(ConnectionError):
                self.clientRunning = False #set clientRunning to False to indicate the socket is not running
                self.clientSocket.close() # close the socket
                self.guiScreen.destroy() # close the GUI screen
                break
        self.clientSocket.close() #close the socket
         
    def displayMessage(self, messageToDisplay, place):
        """
        Displays the chat message on the GUI.
        """
        self.messageHistory.configure(state='normal')
        self.messageHistory.insert(END, messageToDisplay + '\n', place) # write the messaeg in the GUI
        self.messageHistory.configure(state='disabled')

def main(): #Note that the main function is outside the ChatClient class
    window = Tk()
    c = ChatClient(window)
    window.mainloop()
    #May add more or modify, if needed 

if __name__ == '__main__': # May be used ONLY for debugging
    main()
    