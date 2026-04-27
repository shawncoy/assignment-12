from threading import Thread, current_thread
from time import ctime

class TimeClientHandler(Thread):
    def __init__(self, client):
        super().__init__()
        self.client = client

    def run(self):
        thread_name = current_thread().name
        print(f"[{thread_name}] is processing the request...")
        # Using 'with' here ensures the client socket closes 
        # as soon as the thread finishes its task.
        with self.client:
            message = ctime()
            self.client.send(message.encode("ascii"))