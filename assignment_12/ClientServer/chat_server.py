from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR

HOST = "localhost" 
PORT = 6000
ADDRESS = (HOST, PORT)
BUFSIZE = 1024
ENCODING = "ascii"

def start_chat_server():
    # Context manager handles the primary server socket
    with socket(AF_INET, SOCK_STREAM) as server:
        server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        server.bind(ADDRESS)
        server.listen(5)
        
        while True:
            print("Waiting for connection . . .")
            client, address = server.accept()
            
            # Using another 'with' for the specific client connection
            with client:
                print(f"... connected from: {address}")
                client.send("Welcome to my chat room!".encode(ENCODING))

                while True:
                    data = client.recv(BUFSIZE)
                    if not data:
                        print("Client disconnected")
                        break
                    
                    message = data.decode(ENCODING)
                    print(message) 
                    
                    # Prompting for user input and encoding immediately
                    reply = input('> ')
                    client.send(reply.encode(ENCODING))

if __name__ == "__main__":
    start_chat_server()