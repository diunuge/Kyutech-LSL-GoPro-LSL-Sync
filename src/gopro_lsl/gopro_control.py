"""
GoPro control module.
Provides functions to start and stop recording and query camera status.
"""

import requests
import time
from datetime import datetime
from src.gopro_lsl.config import GOPRO_IP, GOPRO_SERIAL, DEFAULT_TIMEOUT, DEFAULT_POLL_INTERVAL
from src.log.logger import logger

import requests
import time
import argparse

from pylsl import StreamInfo, StreamOutlet

# =====================================
# ここで複数カメラを設定
# name: 自分がわかりやすいラベル
# serial_last3: カメラのシリアル番号の下3桁
# =====================================
# CAMERAS = [
#     {"name": "big1", "serial_last3": "794"},
#     # 必要に応じて追加
# ]

# =====================================
# GoPro制御クラス
# =====================================
class GoProCamera:
    def __init__(self, name: str, serial_last3: str = GOPRO_SERIAL):
        self.name = name
        self.serial_last3 = serial_last3
        x = serial_last3[0]
        yz = serial_last3[1:]
        camera_ip = f"172.2{x}.1{yz}.51"
        self.base_url = f"http://{camera_ip}:8080"

        self.enable_wired_usb_control()

    def __repr__(self):
        return f"<GoProCamera name={self.name}, serial_last3={self.serial_last3}, base_url={self.base_url}>"

    def enable_wired_usb_control(self):
        """
        有線USB制御を有効化
        GET /gopro/camera/control/wired_usb?p=1

        一部ファームでは 404 の可能性があるので、その場合は警告だけ出して続行。
        """
        url = f"{self.base_url}/gopro/camera/control/wired_usb"
        try:
            r = requests.get(url, params={"p": 1}, timeout=3)
            r.raise_for_status()
            print(f"[{self.name}] ✔ wired USB control enabled")
        except requests.exceptions.HTTPError as e:
            if e.response is not None and e.response.status_code == 404:
                print(f"[{self.name}] ⚠ wired_usb endpoint 404: このファームでは不要/未対応なのでスキップ")
            else:
                print(f"[{self.name}] ✖ HTTPError in enable_wired_usb_control: {e}")
        except requests.exceptions.RequestException as e:
            print(f"[{self.name}] ✖ Request error in enable_wired_usb_control: {e}")

    def keep_alive(self):
        """
        スリープ防止用の keep-alive
        GET /gopro/camera/keep_alive
        """
        url = f"{self.base_url}/gopro/camera/keep_alive"
        try:
            r = requests.get(url, timeout=3)
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"[{self.name}] ⚠ keep_alive failed: {e}")

    def get_status(self):
        """Query GoPro camera status."""
        try:
            print("Getting GoPro status...")
            url = f"{self.base_url}/gp/gpControl/status"
            response = requests.get(url, timeout=2)
            print(f"response: {response.json()}")
            if response.status_code == 200:
                return response.json()
            else:
                print("Failed to get GoPro status")
                return None
        except Exception as e:
            print(f"Error getting GoPro status: {e}")
            return None

    def is_recording(self):
        """
        Returns True if the GoPro Hero11 Mini is actively recording.
        Uses encoding state ('10') as primary key for accuracy.
        """

        status = self.get_status()
        if not status:
            return False
        
        print(status.get("status", {}).get("10"))
        
        if status.get("status", {}).get("10") == 1:
            return True

        return False

    def shutter(self, mode: str, timeout=DEFAULT_TIMEOUT, poll_interval=DEFAULT_POLL_INTERVAL):
        """
        録画開始/停止
        GET /gopro/camera/shutter/start or /stop
        mode: "start" or "stop"
        """
        assert mode in ("start", "stop")
        url = f"{self.base_url}/gopro/camera/shutter/{mode}"
        try:
            r = requests.get(url, timeout=3)
            r.raise_for_status()
            print(f"[{self.name}] ✔ shutter {mode}")

            # Wait for encoder state to turn OFF
            deadline = time.time() + timeout

            while time.time() < deadline:
                if mode == "stop" and self.is_recording() is False:
                    # print("GoPro recording start confirmed.")
                    logger.log("GoPro recording stop confirmed.")
                    return True
                
                elif mode == "start" and self.is_recording() is True:
                    # log("GoPro recording stop confirmed.")
                    logger.log("GoPro recording stop confirmed.")
                    return True
                time.sleep(poll_interval)

            print("Timeout: GoPro did not stop recording.")
            # logger.log("Timeout: GoPro did not stop recording.")
            return False

        except requests.exceptions.RequestException as e:
            print(f"[{self.name}] ✖ shutter {mode} failed: {e}")

    def start_recording(self):
        return self.shutter("start")

    def stop_recording(self):
        return self.shutter("stop")
