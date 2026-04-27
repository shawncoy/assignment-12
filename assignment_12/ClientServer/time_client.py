"""
File: time_client.py
Client for obtaining the day and time.
"""
from socket import socket, AF_INET, SOCK_STREAM

HOST = "localhost"
PORT = 6000
BUFSIZE = 1024

def main():
    # Using 'with' ensures the socket closes automatically
    with socket(AF_INET, SOCK_STREAM) as client:
        client.connect((HOST, PORT))
        
        # Receive and decode in one step
        data = client.recv(BUFSIZE).decode("ascii")
        print(data)

if __name__ == "__main__":
    main()