"""
File: time_server.py
Server for providing the day and time.
"""

from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from time import ctime

HOST = "localhost"
PORT = 6000
ADDRESS = (HOST, PORT)

def main():
    # 'with' acts as a context manager to handle setup/teardown
    with socket(AF_INET, SOCK_STREAM) as server_socket:
        server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        server_socket.bind(ADDRESS)
        server_socket.listen(5)
        print(f"Server listening on {HOST}:{PORT}...")

        while True:
            client, address = server_socket.accept()
            print(f"... connected from: {address}")
            response = f"{ctime()}\nHave a nice day!"
            client.send(response.encode("ascii"))
            client.close()

if __name__ == "__main__":
    main()