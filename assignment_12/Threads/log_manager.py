import time
import random
from threading import Thread, current_thread, Condition

'''
# TODO Explain what is condition used for? Condition singles out a thread and gives only that thread the ability to access a resource. 
# When that thread is accessing a resource, no other thread can access it until the first thread is done. This is known as a lock. A condition is used to manage the state of the lock and to signal other threads when the lock is available again.
# This is done by using a wait() and notify() method.
# TODO Explain how does is_empty maintain the state management? is_empty is a Boolean variable that is used to tell the generator thread that it is either empty and can generate a log,
# or it is not empty and it needs to wait for the archiver thread to archive the log before it can generate a new log. 
'''
class LogBuffer:
    def __init__(self):
        self.current_log = None
        self.is_empty = True
        self.condition = Condition()

    def write_log(self, log_msg):
        with self.condition:
            # Wait for cell to become writeable again
            while not self.is_empty:
                self.condition.wait()
            

            print(f"{current_thread().name} generated log: {log_msg}")
            self.current_log = log_msg
            self.is_empty = False

            self.condition.notify()  # Notify archiver that a new log is available
        
        pass

    def archive_log(self):
        with self.condition:
            
            while self.is_empty:
                self.condition.wait() # Wait for a log to be available
            
            log_to_archive = self.current_log

            print(f"{current_thread().name} archiving log: {log_to_archive}")
            self.current_log = None
            self.is_empty = True

            self.condition.notify()  # Notify generator that the cell is now empty
            return log_to_archive
        pass



class LogGenerator(Thread):
    def __init__(self, cell, access_count):
        super().__init__(name="LogGenerator")
        self.cell = cell
        self.access_count = access_count

    def run(self):
        for i in range(1, self.access_count + 1):
            time.sleep(random.random())
            log_msg = f"Log entry {i}"
            self.cell.write_log(log_msg)
        print(f"{current_thread().name} finished generating logs.")
        pass

class LogArchiver(Thread):
    def __init__(self, cell, access_count):
        super().__init__(name="LogArchiver")
        self.cell = cell
        self.access_count = access_count

    def run(self):
        for _ in range(self.access_count):  
            time.sleep(random.random())
            self.cell.archive_log()
        print(f"{current_thread().name} finished archiving logs.")
        pass

def main():
    LOG_COUNT = 5
    buffer = LogBuffer()
    
    # Initialize and start threads
    gen = LogGenerator(buffer, LOG_COUNT)
    arc = LogArchiver(buffer, LOG_COUNT)
    
    gen.start()
    arc.start()
    
    gen.join()
    arc.join()
    print("\nLog Maintenance Complete.")

if __name__ == "__main__":
    main()