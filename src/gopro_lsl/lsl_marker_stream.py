"""
LSL marker stream module.
Sends event markers to Lab Streaming Layer for synchronization.
"""

from pylsl import StreamInfo, StreamOutlet
import time

# Create an LSL outlet for markers
info = StreamInfo(name='GOPRO_MARKERS', type='Markers', channel_count=1,
                  channel_format='string', source_id='gopro_1')
outlet = StreamOutlet(info)

def send_marker(marker: str):
    """
    Send a single marker to the LSL stream.
    
    Args:
        marker (str): The label or event to send.
    """
    outlet.push_sample([marker])
    print(f"Sent LSL marker: {marker}")