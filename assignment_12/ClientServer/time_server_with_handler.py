from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from time_client_handler import TimeClientHandler

HOST = "localhost"
PORT = 6000
ADDRESS = (HOST, PORT)

def start_multithreaded_server():
    # Context manager for the main listening socket
    with socket(AF_INET, SOCK_STREAM) as server:
        server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        server.bind(ADDRESS)
        server.listen(5)
        print(f"Multithreaded server listening on {PORT}...")

        while True:
            client, address = server.accept()
            print(f"... connected from: {address}")
            
            # Create the handler and set as daemon so it 
            # exits when the main server stops.
            handler = TimeClientHandler(client)
            handler.daemon = True
            handler.start()

if __name__ == "__main__":
    start_multithreaded_server()