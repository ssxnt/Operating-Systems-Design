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
        self.clientName = name  # name of client

        self.socketSetUp()  # separate gui and socket setup
        self.guiSetup()

    def socketSetUp(self):
        """
        Sets up the client socket and connects to server
        """
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create client socket
        self.clientSocket.bind(('127.0.0.1 ', 0))
        self.connection, self.address = self.clientSocket.getsockname()
        self.clientSocket.connect((self.connection, 11111))  # connect to server
        self.clientRunning = True

        threading.Thread(target=self.receiveMessage).start()

    def guiSetup(self):
        """
        Sets up the GUI screen and window dimensions.
        """
        self.guiScreen.title(f"{self.clientName}")  # creates a title for the gui

        self.clientLabel = Label(self.guiScreen, text=f"{self.clientName} @port #{self.address}",
                                 font=("Courier", 11), anchor='w')
        self.clientLabel.pack(fill='x')

        self.guiFrame = Frame(self.guiScreen)  # create a frame for more widgets
        self.guiFrame.pack(fill='x')

        # create label for chat message
        self.chatEntry = Label(self.guiFrame, text="Chat Message:", font=("Courier", 11))
        self.chatEntry.grid(row=0, column=0)

        self.messageEntry = Entry(self.guiFrame, width=70)  # create entry box for input
        self.messageEntry.grid(row=0, column=1)
        self.messageEntry.bind('<Return>', self.sendMessage)

        # create chat history label
        self.chatHistoryLabel = Label(self.guiScreen, text="Chat History:", font=("Courier", 11), anchor='w')
        self.chatHistoryLabel.pack(fill='x')

        # create widget to display text
        self.chatHistory = Text(self.guiScreen, state='disabled', font=("Courier", 11))
        self.chatHistory.pack(side='left', fill='both', expand=True)
        self.chatHistory.tag_configure('left', justify='left')

    def sendMessage(self, event=None):
        """
        Sends a message to the server
        """
        messageEntered = self.messageEntry.get()  # get the message from the text entry
        self.messageEntry.delete(0, END)  # delete text in box
        messageSending = f'{self.clientName}: {messageEntered}'  # reformat message for sending
        self.clientSocket.send(messageSending.encode('utf-8'))  # send message by encoding
        self.displayMessage(messageSending, 'center')  # display the message in client GUI

    def receiveMessage(self):
        """
        Receives messages from the server and updates the chat message GUI
        """
        while self.clientRunning:
            try:  # try to receive and decode message
                messageReceived = self.clientSocket.recv(1024).decode('utf-8')
                self.displayMessage(messageReceived, 'left')  # display message
            except(ConnectionError):
                self.clientRunning = False
                self.clientSocket.close()  # close the socket
                self.guiScreen.destroy()  # close the GUI screen
                break
        self.clientSocket.close()

    def displayMessage(self, messageToDisplay, place):
        """
        Displays the chat message on the GUI.
        """
        self.chatHistory.configure(state='normal')
        self.chatHistory.insert(END, messageToDisplay + '\n', place)  # write the message in the GUI
        self.chatHistory.configure(state='disabled')


def main():  # Note that the main function is outside the ChatClient class
    window = Tk()
    c = ChatClient(window)
    window.mainloop()
    # May add more or modify, if needed


if __name__ == '__main__':  # May be used ONLY for debugging
    main()
