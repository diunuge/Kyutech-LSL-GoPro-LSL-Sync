"""
LSL marker stream module.
Provides a MarkerSender class with optional heartbeat markers.

When receives "camera_start":

✔ Start GoPro recording
✔ Send START LSL marker
✔ Begin heartbeat markers

When Pi receives "camera_stop":

✔ Send STOP LSL marker
✔ Stop GoPro recording
✔ Stop heartbeat
"""

import time
import threading
from pylsl import StreamInfo, StreamOutlet, local_clock


class MarkerSender:
    def __init__(self, stream_name="GOPRO_MARKERS",
                 stream_type="Markers",
                 channel_count=1,
                 heartbeat_hz=1.0,
                 source_id="gopro_rpi_agent"):

        self.info = StreamInfo(
            name=stream_name,
            type=stream_type,
            channel_count=channel_count,
            channel_format='string',
            source_id=source_id
        )

        self.outlet = StreamOutlet(self.info)
        self.heartbeat_hz = heartbeat_hz
        self._heartbeat_thread = None
        self._running = False

    def send_marker(self, marker: str):
        """Send a single LSL event marker."""
        self.outlet.push_sample([marker], local_clock())
        print(f"[LSL] Sent marker: {marker}")

    # ------------ HEARTBEAT THREAD ------------ #

    def _heartbeat_loop(self):
        next_time = time.perf_counter()
        interval = 1.0 / self.heartbeat_hz

        while self._running:
            next_time += interval
            label = f"HB_{int(time.time())}"  # Heartbeat marker
            self.send_marker(label)

            sleep_time = next_time - time.perf_counter()
            if sleep_time > 0:
                time.sleep(sleep_time)

    def start_heartbeat(self):
        """Start the background periodic heartbeat marker."""
        if self._running:
            print("[LSL] Heartbeat already running.")
            return

        print("[LSL] Starting heartbeat...")
        self._running = True
        self._heartbeat_thread = threading.Thread(
            target=self._heartbeat_loop, daemon=True
        )
        self._heartbeat_thread.start()

    def stop_heartbeat(self):
        """Stop the heartbeat."""
        if not self._running:
            print("[LSL] Heartbeat was not running.")
            return

        print("[LSL] Stopping heartbeat...")
        self._running = False

        if self._heartbeat_thread:
            self._heartbeat_thread.join(timeout=1.0)
            self._heartbeat_thread = None