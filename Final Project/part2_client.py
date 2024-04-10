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
    def __init__(self, guiScreen, clientName=current_process().name):
        self.guiScreen = guiScreen
        self.clientName = clientName
        self.clientRunning = True

        self.socketSetUp()
        self.guiSetup()

        self.guiScreen.protocol("WM_DELETE_WINDOW", self.terminateConnection)
        
    def socketSetUp(self):
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientSocket.bind(('127.0.0.1', 0))
        self.address = self.clientSocket.getsockname()
        self.clientSocket.connect(('127.0.0.1', 11111))

        threading.Thread(target=self.rcvMessage, daemon=True).start()

    def guiSetup(self):
        self.guiScreen.title(f"Chat {self.clientName}")
        
        self.guiFrame = Frame(self.guiScreen)
        self.guiFrame.pack(fill='x')

        self.chatEntry = Label(self.guiFrame, text="Message", font=("Courier", 11))
        self.chatEntry.grid(row=0, column=0)

        self.chatEntry = Entry(self.guiFrame, width=50)
        self.chatEntry.grid(row=0, column=1)
        self.chatEntry.bind('<Return>', self.sendMessage)

        self.chatHistoryLabel = Label(self.guiScreen, text="Chat Window:", font=("Courier", 11))
        self.chatHistoryLabel.pack(fill='x')

        self.chatHistory = Text(self.guiScreen, state='disabled', font=("Courier", 11))
        self.chatHistory.pack(side='left', fill='both', expand=True)

        self.chatHistory.tag_configure('center', justify='center')

    def sendMessage(self, event=None):
        msg = self.chatEntry.get()
        if msg:
            self.clientSocket.sendall(msg.encode('utf-8'))
            self.chatEntry.delete(0, END)
            self.displayMessage(f"You: {msg}", 'center')

    def rcvMessage(self):
        while self.clientRunning:
            try:
                msg = self.clientSocket.recv(1024).decode('utf-8')
                if msg:
                    self.displayMessage(msg, 'left')
            except Exception:
                print(f"Connection closed by server due to {Exception}")
                self.terminateConnection()

    def displayMessage(self, msg, align):
        self.chatHistory.config(state=NORMAL)
        self.chatHistory.insert('end', msg + '\n', align)
        self.chatHistory.config(state=DISABLED)
        self.chatHistory.yview(END)

    def terminateConnection(self):
        self.clientRunning = False
        try:
            self.clientSocket.close()
        except Exception:
            print(f"Error closing socket: {Exception}")
        self.guiScreen.destroy()

def main(): #Note that the main function is outside the ChatClient class
    window = Tk()
    c = ChatClient(window)
    window.mainloop()
    #May add more or modify, if needed 

if __name__ == '__main__': # May be used ONLY for debugging
    main()
    