# Raspberry Pi Agent (`rpi_agent`)

This folder contains the Raspberry Pi agent that subscribes to MQTT commands from a PC commander and executes actions such as controlling cameras, GPIO devices, or motors. It also optionally sends periodic heartbeat messages to indicate it is online.

---
# Raspberry Pi Agent Configurations

## connect to GO Pro wifi

- Enable camera WiFi
- Connect to WiFi
`sudo nmcli device wifi connect "<SSID>" password "<password>"`

## configure MQTT

```bash
sudo apt update
sudo apt install mosquitto mosquitto-clients
sudo systemctl enable mosquitto
sudo systemctl start mosquitto
systemctl status mosquitto
```

## install remote desktop (optional)

```bash
sudo apt install xrdp
sudo systemctl status xrdp
# sudo systemctl enable xrdp
# sudo systemctl start xrdp
```

## clone github project
`git clone https://github.com/diunuge/Kyutech-LSL-GoPro-LSL-Sync.git`

## configure python environment

- Execute commands from project folder
`cd Kyutech-LSL-GoPro-LSL-Sync`
`sudo apt install python3-venv`

- create virtual environment 
`python3 -m venv venv`
- activate virtual environment
`source venv/bin/activate`

- install requirements
```bash
pip install pylsl
pip install requests
pip install paho-mqtt
```

- download liblsll https://github.com/sccn/liblsl/releases/download/v1.16.2/liblsl-1.16.2-bookworm_arm64.deb
- Extract it
- Copy liblsl.so into pylsl’s folder
lib/liblsl.so LSL/Program/venv/lib/python3.13/site-packages/pylsl/lib/
- set MQTT broker ip address, device id, ...etc in config.py
- run start_agent_with_heartbeat.py script from main folder
`python -m src.scripts.start_agent_with_heartbeat`

## deactivate when done
`deavtivate`

## Folder Structure
