"""
Script: run_gopro_recording.py
Runs a full GoPro recording session with LSL markers.
"""

import argparse
import sys
from src.gopro_lsl.recorder import record_session
from src.gopro_lsl.config import DEFAULT_RECORDING_DURATION, MARKER_START, MARKER_STOP

def main():
    parser = argparse.ArgumentParser(
        description="Run a GoPro recording session with LSL markers."
    )

    parser.add_argument(
        "--duration",
        type=int,
        default=DEFAULT_RECORDING_DURATION,
        help=f"Recording duration in seconds (default: {DEFAULT_RECORDING_DURATION})"
    )

    parser.add_argument(
        "--marker_start",
        type=str,
        default=MARKER_START,
        help=f"Marker to send at start (default: {MARKER_START})"
    )

    parser.add_argument(
        "--marker_stop",
        type=str,
        default=MARKER_STOP,
        help=f"Marker to send at stop (default: {MARKER_STOP})"
    )

    args = parser.parse_args()

    print("--------- GoPro Recording Session ---------")
    print(f"Duration: {args.duration} sec")
    print(f"Start Marker: '{args.marker_start}'")
    print("-------------------------------------------")

    try:
        record_session(duration_sec=args.duration, marker_start=args.marker_start, marker_stop=args.marker_stop)
    except Exception as e:
        print(f"Error during session: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
