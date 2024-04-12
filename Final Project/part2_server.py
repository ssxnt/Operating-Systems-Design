# Group#: 4
# Student Names: Katie Goncalves & Sant Sumetpong

#Content of server.py; To complete/implement

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
    def __init__(self, window):
        self.window = window
        self.clients = []
        self.guiSetup()  # set up the gui and server socket
        self.socketSetup()
        
    def socketSetup(self, host='127.0.0.1', port=11111):
        self.host = host  # get host and port from args
        self.port = port
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create server socket
        self.serverSocket.bind((self.host, self.port))  # assign IP address and a port number to socket instance
        self.serverSocket.listen(5)  # listen/get ready for connections
        threading.Thread(target=self.acceptConnections).start()

    def guiSetup(self):
        self.window.title("Chat Server")  # title the chat server
        
        self.chatLabel = Label(self.window, text="Chat Log", font=("Courier", 11))  # create label for chat log
        self.chatLabel.pack(fill='x')
        
        self.chatHistory = Text(self.window, state='disabled')
        self.chatHistory.pack(side='left', fill='both')
    
    def acceptConnections(self):
        print(f"The server is ready to connect on {self.host}:{self.port}...")
        
        while True:
            try:
                connection, address = self.serverSocket.accept()  # wait for an incoming connection
                self.clients.append(connection)  # append connection once created
                print(f"Connection from {address}")
                threading.Thread(target=self.rcvMessages, args=(connection,)).start()
            except Exception:
                print(f"Server failed to connect: {Exception}")
                break

    def rcvMessages(self, client):
        """
        Receives messages from the clients
        """
        
        def sendMessages(message):
            """
            Sends messages to the clients
            """
            for conn in self.clients:  # check if the current connection is not the client who sent the message
                if conn != client:
                    try:  # send the message in utf-8 form to the clients
                        conn.send(message.encode('utf-8'))
                    except Exception:
                        print(f"Error sending message: {Exception}")
                        self.clients.remove(conn)
                        conn.close()
                        
        def showchatHistory():
            """
            Displays chat history on window screen
            """
            self.chatHistory.configure(state='normal')  # enable text widget to allow modifications
            self.chatHistory.insert('end', msg + '\n')  # insert new message into chat history text widget
            self.chatHistory.configure(state='disabled')  # disable text widget to prevent further modifications
                
        while True:
            try:
                msg = client.recv(1024).decode('utf-8')  # decode received message from client
                if msg:  # check if any message has been received; if so, refer above inner functions
                    print(f"Message received: {msg}")
                    showchatHistory()
                    sendMessages(msg)
            except Exception as e:
                print(f"Client disconnected: {e}")
                self.clients.remove(client)
                client.close()
                break
            
def main():
    window = Tk()
    ChatServer(window)
    window.mainloop()
    #May add more or modify, if needed

if __name__ == '__main__':  # May be used ONLY for debugging
    main()
