from threading import Thread
from socket import socket, AF_INET, SOCK_STREAM

HOST = "localhost"
PORT = 6000
BUFSIZE = 1024
NUM_CLIENTS = 10  # Number of simultaneous clients to simulate

def request_time(client_id):
    """Function for a single client thread to request time from the server."""
    with socket(AF_INET, SOCK_STREAM) as client:
        client.connect((HOST, PORT))
        
        # Receive the data from the server
        data = client.recv(BUFSIZE).decode("ascii")
        print(f"Client {client_id} received: {data.strip()}")

def main():
    threads = []

    print(f"Starting {NUM_CLIENTS} simultaneous client requests...")

    # Create and start threads
    for i in range(NUM_CLIENTS):
        t = Thread(target=request_time, args=(i,))
        threads.append(t)
        t.start()

    # Wait for all threads to complete
    for t in threads:
        t.join()

    print("All client requests completed.")

if __name__ == "__main__":
    main()