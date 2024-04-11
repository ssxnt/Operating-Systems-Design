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
        self.guiScreen = guiScreen
        self.clientName = name

        self.socketSetUp()
        self.guiSetup()

    def socketSetUp(self):
        """
        Sets up the client socket and connects to server
        """
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientSocket.bind(('localhost', 0))
        self.connection, self.address = self.clientSocket.getsockname()
        self.clientSocket.connect((self.connection, 11111))
        self.clientRunning = True

        threading.Thread(target=self.receiveMessage).start()

    def guiSetup(self):
        self.guiScreen.title(f"{self.clientName}")

        self.clientLabel = Label(self.guiScreen, text=f"{self.clientName} @port #{self.address}",
                                 font=("Courier", 11), anchor='w')
        self.clientLabel.pack(fill='x')

        self.guiFrame = Frame(self.guiScreen)
        self.guiFrame.pack(fill='x')

        self.chatEntry = Label(self.guiFrame, text="Chat Message:", font=("Courier", 11))
        self.chatEntry.grid(row=0, column=0)

        self.messageEntry = Entry(self.guiFrame, width=70)
        self.messageEntry.grid(row=0, column=1)
        self.messageEntry.bind('<Return>', self.sendMessage)

        self.chatHistoryLabel = Label(self.guiScreen, text="Chat History:", font=("Courier", 11), anchor='w')
        self.chatHistoryLabel.pack(fill='x')

        self.chatHistory = Text(self.guiScreen, state='disabled', font=("Courier", 11))
        self.chatHistory.pack(side='left', fill='both', expand=True)
        self.chatHistory.tag_configure('left', justify='left')

    def sendMessage(self, event=None):
        """
        Sends a message to the server
        """
        messageEntered = self.messageEntry.get()
        self.messageEntry.delete(0, END)
        messageSending = f'{self.clientName}: {messageEntered}'
        self.clientSocket.send(messageSending.encode('utf-8'))
        self.displayMessage(messageSending, 'center')

    def receiveMessage(self):
        """
        Receives messages from the server and updates the chat message GUI
        """
        while self.clientRunning:
            try:
                messageReceived = self.clientSocket.recv(1024).decode('utf-8')
                self.displayMessage(messageReceived, 'left')
            except(ConnectionError):
                self.clientRunning = False
                self.clientSocket.close()
                self.guiScreen.destroy()
                break
        self.clientSocket.close()

    def displayMessage(self, messageToDisplay, place):
        """
        Displays the chat message on the GUI.
        """
        self.chatHistory.configure(state='normal')
        self.chatHistory.insert(END, messageToDisplay + '\n', place)
        self.chatHistory.configure(state='disabled')


def main():  # Note that the main function is outside the ChatClient class
    window = Tk()
    c = ChatClient(window)
    window.mainloop()
    # May add more or modify, if needed


if __name__ == '__main__':  # May be used ONLY for debugging
    main()
