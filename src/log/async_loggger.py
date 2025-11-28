"""
Asynchronous logger developed for faster and thread safe logging 
"""

import threading
import queue
import datetime
from src.log.config import DEFAULT_FILE

class AsyncLogger:
    def __init__(self, filename: str = DEFAULT_FILE):
        self.log_queue = queue.Queue()
        self.running = True
        self.thread = threading.Thread(target=self._worker, daemon=True)
        self.file = open(filename, "a", buffering=1) #line buffered
        self.thread.start()

    def _worker(self):
        write = self.file.write
        while self.running or not self.log_queue.empty():
            try:
                msg = self.log_queue.get(timeout=0.1)
                write(f"[{datetime.now().strftime("%H:%M:%S.%f")[:-3]}] {msg}" + "\n")
            except queue.Empty:
                pass


    def log(self, msg):
        self.log_queue.put(msg)

    def close(self):
        self.running = False
        self.thread.join()
        self.file.close()
