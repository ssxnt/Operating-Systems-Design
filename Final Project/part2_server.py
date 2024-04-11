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
        self.guiSetup()
        self.socketSetup()
        
    def socketSetup(self, host='127.0.0.1', port=11111):
        self.host = host
        self.port = port
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.bind((self.host, self.port))
        self.serverSocket.listen(5)
        threading.Thread(target=self.acceptConnections).start()

    def guiSetup(self):
        self.window.title("Chat Server")
        
        self.chatLabel = Label(self.window, text="Chat Log", font=("Courier", 11))
        self.chatLabel.pack(fill='x')
        
        self.chatHistory = Text(self.window, state='disabled')
        self.chatHistory.pack(side='left', fill='both')
    
    def acceptConnections(self):
        print(f"The server is ready to connect on {self.host}:{self.port}...")
        
        while True:
            try:
                connection, address = self.serverSocket.accept()
                self.clients.append(connection)
                print(f"Connection from {address}")
                threading.Thread(target=self.rcvMessages, args=(connection,)).start()
            except Exception:
                print(f"Server failed to connect: {Exception}")
                break

    def rcvMessages(self, client):
        
        def sendMessages(message):
            for conn in self.clients:
                if conn != client:
                    try:
                        conn.send(message.encode('utf-8'))
                    except Exception:
                        print(f"Error sending message: {Exception}")
                        self.clients.remove(conn)
                        conn.close()
                        
        def showchatHistory():
            self.chatHistory.configure(state='normal')
            self.chatHistory.insert('end', msg + '\n')
            self.chatHistory.configure(state='disabled')
                
        while True:
            try:
                msg = client.recv(1024).decode('utf-8')
                if msg:
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
