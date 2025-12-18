"""
Configuration file for GoPro + LSL integration.
"""

# === Connection mode ===
# "wifi" (old behavior) or "usb"
GOPRO_CONNECTION_MODE = "wifi"

# Wi-Fi GoPro IP (unchanged)
GOPRO_WIFI_IP = "10.5.5.9"

# USB-Ethernet GoPro IP (RNDIS/ECM)
# Example: 172.20.10.51, 172.21.11.51, etc.
GOPRO_USB_IP = "172.20.10.51"

# HTTP port
GOPRO_HTTP_PORT = 80     # Wi-Fi
GOPRO_USB_PORT = 8080   # USB-Ethernet

# GoPro IP address (update if using multiple cameras or different network)
GOPRO_IP = "10.5.5.9"

# Start LSL marker label
MARKER_START = "START"

# Stop LSL marker label
MARKER_STOP = "STOP"

# Recording default duration (seconds)
DEFAULT_RECORDING_DURATION = 10

# Default timeout for status checking (seconds)
DEFAULT_TIMEOUT = 5.0

# Default poll interval for status checking (seconds)
DEFAULT_POLL_INTERVAL = 0.2

GOPRO_SERIAL = "794"  # TODO
