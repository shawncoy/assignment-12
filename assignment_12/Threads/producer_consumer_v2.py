import time
import random
from threading import Thread, current_thread, Condition

class SharedCell:
    """Shared data that sequences writing before reading using a Condition."""
    def __init__(self):
        self.data = -1
        self.writeable = True
        self.condition = Condition()

    def set_data(self, data):
        """Producer's method to write to shared data."""
        with self.condition:
            # Wait while the cell is not writeable (consumer hasn't read yet)
            while not self.writeable:
                self.condition.wait()
            
            # Modern f-string replaces % formatting
            print(f"{current_thread().name} setting data to {data}")
            self.data = data
            self.writeable = False
            
            # Notify the consumer that data is ready
            self.condition.notify()

    def get_data(self):
        """Consumer's method to read from shared data."""
        with self.condition:
            # Wait while the cell is writeable (producer hasn't written yet)
            while self.writeable:
                self.condition.wait()
            
            print(f"{current_thread().name} accessing data {self.data}")
            self.writeable = True
            
            # Notify the producer that the cell is clear
            self.condition.notify()
            return self.data

class Producer(Thread):
    def __init__(self, cell, access_count):
        super().__init__(name="Producer")
        self.cell = cell
        self.access_count = access_count

    def run(self):
        for i in range(1, self.access_count + 1):
            time.sleep(random.random())
            self.cell.set_data(i)

class Consumer(Thread):
    def __init__(self, cell, access_count):
        super().__init__(name="Consumer")
        self.cell = cell
        self.access_count = access_count


    def run(self):
        for _ in range(self.access_count):
            time.sleep(random.random())
            self.cell.get_data()

def main():
    count = int(input("Enter the number of accesses: "))
    cell = SharedCell()
    
    # Modern initialization using list comprehension
    threads = [Producer(cell, count), Consumer(cell, count)]
    
    for t in threads:
        t.start()
            
if __name__ == "__main__":
    main()