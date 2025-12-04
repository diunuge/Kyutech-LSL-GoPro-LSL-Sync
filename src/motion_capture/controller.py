import time
import signal
import sys
from src.motion_capture.rebocap_to_lsl import RebocapLSLSender

class RebocapController:
    def __init__(self, port=7690):
        self.sender = RebocapLSLSender()
        self.port = port
        self.running = False
        
        # Register signal handlers for graceful shutdown
        # signal.signal(signal.SIGINT, self._signal_handler)
        # signal.signal(signal.SIGTERM, self._signal_handler)

    def _signal_handler(self, signum, frame):
        """Handle interrupt/terminate signals gracefully"""
        print(f"\nReceived signal {signum}. Shutting down...")
        self.stop()
        sys.exit(0)

    def start(self):
        """Start streaming from Rebocap to LSL"""
        if self.running:
            print("Rebocap streaming is already running")
            return
        
        try:
            # Connect to Rebocap (ensure the Rebocap app is running, sensors calibrated)
            self.sender.connect(port=self.port)
            
            # Start streaming to LSL
            self.sender.start()
            self.running = True
            print("Streaming started")
        except Exception as e:
            print(f"Error starting streaming: {e}")
            self.close()

    def stop(self):
        """Stop streaming from Rebocap"""
        if not self.running:
            print("Rebocap streaming is not running")
            return
        
        try:
            self.sender.stop()
            self.running = False
            print("Streaming stopped")
        except Exception as e:
            print(f"Error stopping streaming: {e}")

    def close(self):
        """Close connection and cleanup resources"""
        try:
            if self.running:
                self.stop()
            self.sender.close()
            print("Connection closed")
        except Exception as e:
            print(f"Error closing connection: {e}")

    def wait_until_stopped(self):
        """Keep streaming running until interrupted"""
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            pass


def main():
    controller = RebocapController(port=7690)
    controller.start()
    controller.wait_until_stopped()
    controller.close()


if __name__ == "__main__":
    main()