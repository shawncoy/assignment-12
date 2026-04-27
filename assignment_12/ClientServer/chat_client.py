from socket import socket, AF_INET, SOCK_STREAM

HOST = "localhost"
PORT = 6000
BUFSIZE = 1024
ADDRESS = (HOST, PORT)
ENCODING = "ascii"

def start_chat_client():
    # Use 'with' to ensure the socket closes even if the user crashes the program
    with socket(AF_INET, SOCK_STREAM) as client:
        client.connect(ADDRESS)
        
        # Receive and decode the initial greeting
        greeting = client.recv(BUFSIZE).decode(ENCODING)
        print(greeting)

        while True:
            # Prompt for user input and send it to the server
            message = input("> ")
            if not message:
                break
            client.send(message.encode(ENCODING))
            
            # Receive response and check for server disconnect
            data = client.recv(BUFSIZE)
            if not data:
                print("Server disconnected")
                break
            
            reply = data.decode(ENCODING)
            print(reply)

if __name__ == "__main__":
    start_chat_client()