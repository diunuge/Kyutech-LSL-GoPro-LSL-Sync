import time
import threading
from pylsl import StreamInfo, StreamOutlet
from lib.rebocap_python_sdk_v2 import rebocap_ws_sdk
from src.motion_capture.config import STRAM_NAME

class RebocapLSLSender:
    def __init__(self,
                 stream_name=STRAM_NAME,
                 coordinate_type=rebocap_ws_sdk.CoordinateType.UnityCoordinate,
                 use_global_rotation=True):
        # 24 joints, 4 values each (w,x,y,z) = 96 channels
        self.num_joints = 24
        self.num_channels = self.num_joints * 4

        # LSL stream definition
        info = StreamInfo(stream_name,
                          'MoCap',
                          self.num_channels,
                          60,           # nominal sample rate
                          'float32',
                          'rebocap_uid')
        self.outlet = StreamOutlet(info)

        # Rebocap SDK
        self.sdk = rebocap_ws_sdk.RebocapWsSdk(
            coordinate_type=coordinate_type,
            use_global_rotation=use_global_rotation
        )

        self._running = False
        self._thread = None
        self._lock = threading.Lock()
        self._latest_sample = None  # last [96] float list

        # Register callbacks
        self.sdk.set_pose_msg_callback(self._pose_msg_callback)
        self.sdk.set_exception_close_callback(self._exception_close_callback)

    # ---------- Rebocap callbacks ----------

    def _pose_msg_callback(self,
                           self_sdk: rebocap_ws_sdk.RebocapWsSdk,
                           tran: list,
                           pose24: list,
                           static_index: int,
                           ts: float):
        """
        Called by Rebocap on each new frame.
        tran: root position [x,y,z]
        pose24: list of 24 quaternions [w,x,y,z] for each joint.
        """
        # Flatten pose24 into [w0,x0,y0,z0, w1,x1,y1,z1, ...]
        flat = []
        for i in range(self.num_joints):
            qw, qx, qy, qz = pose24[i]
            flat.extend([qw, qx, qy, qz])

        with self._lock:
            self._latest_sample = flat

    def _exception_close_callback(self, self_sdk: rebocap_ws_sdk.RebocapWsSdk):
        print("Rebocap WebSocket closed unexpectedly.")
        # You could add reconnection logic here.

    # ---------- Public API ----------

    def connect(self, port=7690):
        open_ret = self.sdk.open(port)
        if open_ret == 0:
            print("Rebocap connection successful")
        else:
            print("Rebocap connection failed:", open_ret)
            if open_ret == 1:
                print("Connection status error")
            elif open_ret == 2:
                print("Connection failed")
            elif open_ret == 3:
                print("Authentication failed")
            else:
                print("Unknown error", open_ret)
            raise RuntimeError(f"Rebocap open() failed with code {open_ret}")

    def start(self):
        """Start sending data to LSL in a background thread."""
        if self._thread and self._thread.is_alive():
            return
        self._running = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def stop(self):
        """Stop sending data to LSL."""
        self._running = False
        if self._thread:
            self._thread.join(timeout=1.0)

    def close(self):
        """Close Rebocap connection and cleanup."""
        self.stop()
        self.sdk.close()
        # self.sdk.release()

    # ---------- Internal loop ----------

    def _loop(self):
        """
        Poll latest Rebocap frame via get_last_msg() and push to LSL
        while _running is True.
        """
        while self._running:
            msg = self.sdk.get_last_msg()
            if msg is None:
                # print("no msg")
                # No new frame yet (e.g., before calibration / idle)
                time.sleep(0.005)
                continue
                    
            tran, pose24, static_index, ts = msg
            # print(msg)
            # print("\n\n")
            # Convert to flat quaternion array if callback hasn't done it yet
            flat = []
            for i in range(self.num_joints):
                qw, qx, qy, qz = pose24[i]
                flat.extend([qw, qx, qy, qz])

            # Push to LSL
            self.outlet.push_sample(flat)

            # Optional tiny sleep to avoid busy-wait
            # (Rebocap runs around 60 Hz, so this can stay very small)
            time.sleep(0.0)