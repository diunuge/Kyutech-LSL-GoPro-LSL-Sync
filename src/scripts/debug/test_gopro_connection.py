"""
Test script to verify GoPro connection using goprocam library.
Supports both USB and WiFi connections.

Usage:
    python test_gopro_connection.py --usb               # Test USB connection
    python test_gopro_connection.py --wifi <IP>         # Test WiFi connection (default: 10.5.5.9)
    python test_gopro_connection.py                     # Test WiFi with default IP
    python test_gopro_connection.py --usb --recording   # Test USB with recording start/stop cycle
"""

import sys
import time
import argparse
from datetime import datetime

def log(msg, level="INFO"):
    """Print timestamped log message."""
    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    print(f"[{timestamp}] [{level}] {msg}")

def test_usb_connection():
    """Test GoPro connection via USB."""
    try:
        import goprocam
        
        log("Testing USB connection...", "INFO")
        
        # Initialize GoPro via USB
        gp = goprocam.GoProCamera(goprocam.constants.Connection.USB)
        log("USB connection established", "SUCCESS")
        
        # Get camera status
        log("Fetching camera status...", "INFO")
        status = gp.getStatus(2)  # 0=Power, 1=Charging, 2=Recording
        log(f"Camera status: {status}", "INFO")
        
        # Get camera info
        log("Fetching camera info...", "INFO")
        info = gp.getStatus(3)  # Model info
        log(f"Camera info: {info}", "INFO")
        
        # Get battery level
        log("Fetching battery level...", "INFO")
        battery = gp.getStatus(70)
        log(f"Battery level: {battery}%", "INFO")
        
        log("USB connection test PASSED", "SUCCESS")
        return True
        
    except ImportError as e:
        log(f"goprocam not installed: {e}", "ERROR")
        log("Install with: pip install goprocam", "INFO")
        return False
    except Exception as e:
        log(f"USB connection test FAILED: {e}", "ERROR")
        return False

def test_wifi_connection(ip_address):
    """Test GoPro connection via WiFi."""
    try:
        import goprocam
        
        log(f"Testing WiFi connection to {ip_address}...", "INFO")
        
        # Initialize GoPro via WiFi
        gp = goprocam.GoProCamera(goprocam.constants.Connection.WiFi, ip_address=ip_address)
        log(f"WiFi connection established to {ip_address}", "SUCCESS")
        
        # Get camera status
        log("Fetching camera status...", "INFO")
        status = gp.getStatus(2)  # 0=Power, 1=Charging, 2=Recording
        log(f"Camera status: {status}", "INFO")
        
        # Get camera info
        log("Fetching camera info...", "INFO")
        info = gp.getStatus(3)  # Model info
        log(f"Camera info: {info}", "INFO")
        
        # Get battery level
        log("Fetching battery level...", "INFO")
        battery = gp.getStatus(70)
        log(f"Battery level: {battery}%", "INFO")
        
        log("WiFi connection test PASSED", "SUCCESS")
        return True
        
    except ImportError as e:
        log(f"goprocam not installed: {e}", "ERROR")
        log("Install with: pip install goprocam", "INFO")
        return False
    except Exception as e:
        log(f"WiFi connection test FAILED: {e}", "ERROR")
        return False

def test_recording_cycle(connection_type="wifi", ip_address="10.5.5.9"):
    """Test start/stop recording cycle."""
    try:
        import goprocam
        
        if connection_type == "usb":
            log("Initializing GoPro via USB for recording test...", "INFO")
            gp = goprocam.GoProCamera(goprocam.constants.Connection.USB)
        else:
            log(f"Initializing GoPro via WiFi ({ip_address}) for recording test...", "INFO")
            gp = goprocam.GoProCamera(goprocam.constants.Connection.WiFi, ip_address=ip_address)
        
        # Start recording
        log("Starting recording...", "INFO")
        gp.command("camera", "shutter", "start")
        time.sleep(2)
        
        # Check if recording
        recording_status = gp.getStatus(2)
        log(f"Recording status: {recording_status}", "INFO")
        
        # Record for 5 seconds
        log("Recording for 5 seconds...", "INFO")
        time.sleep(5)
        
        # Stop recording
        log("Stopping recording...", "INFO")
        gp.command("camera", "shutter", "stop")
        time.sleep(2)
        
        recording_status = gp.getStatus(2)
        log(f"Recording status after stop: {recording_status}", "INFO")
        
        log("Recording cycle test PASSED", "SUCCESS")
        return True
        
    except Exception as e:
        log(f"Recording cycle test FAILED: {e}", "ERROR")
        return False

def main():
    parser = argparse.ArgumentParser(
        description="Test GoPro connection using goprocam library",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python test_gopro_connection.py --usb
  python test_gopro_connection.py --wifi 10.5.5.9
  python test_gopro_connection.py --recording --usb
        """
    )
    
    parser.add_argument("--usb", action="store_true", help="Test USB connection")
    parser.add_argument("--wifi", nargs="?", const="10.5.5.9", help="Test WiFi connection (default IP: 10.5.5.9)")
    parser.add_argument("--recording", action="store_true", help="Also test recording start/stop cycle")
    
    args = parser.parse_args()
    
    log("=" * 60, "INFO")
    log("GoPro Connection Test Script", "INFO")
    log("=" * 60, "INFO")
    
    results = {}
    
    # Determine which connection to test
    if args.usb:
        results["USB Connection"] = test_usb_connection()
        if args.recording:
            results["USB Recording"] = test_recording_cycle("usb")
    elif args.wifi is not None:
        results["WiFi Connection"] = test_wifi_connection(args.wifi)
        if args.recording:
            results["WiFi Recording"] = test_recording_cycle("wifi", args.wifi)
    else:
        # Default: test WiFi with default IP
        results["WiFi Connection (Default)"] = test_wifi_connection("10.5.5.9")
    
    # Print summary
    log("=" * 60, "INFO")
    log("Test Summary", "INFO")
    log("=" * 60, "INFO")
    
    for test_name, passed in results.items():
        status = "PASSED" if passed else "FAILED"
        level = "SUCCESS" if passed else "ERROR"
        log(f"{test_name}: {status}", level)
    
    all_passed = all(results.values())
    log("=" * 60, "INFO")
    if all_passed:
        log("All tests PASSED!", "SUCCESS")
        return 0
    else:
        log("Some tests FAILED!", "ERROR")
        return 1

if __name__ == "__main__":
    sys.exit(main())
