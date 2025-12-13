# PC commander (`MQTT_agent`)

This folder contains the MQTT commander agent that publishes MQTT commands to control agents such as motion agent, raspberrry pi agent, ...etc.

---

# Configurations

## Clone Github project
- Use git clone
`git clone https://github.com/diunuge/Kyutech-LSL-GoPro-LSL-Sync.git`
- or download zip file from https://github.com/diunuge/Kyutech-LSL-GoPro-LSL-Sync.git

## Install Python

- Install python 3.12 from https://www.python.org/downloads/
- Add main folder and 'Scripts' folder to the environment variables (optional)
- Check installation in command prompt (optional)
`python --version`

## Install dependencies

- Install everything in "requirements.txt" 

## Install MQTT Broker (mosquitto)

- Find the installer here https://mosquitto.org/download/
- Install it

### Configure firewall
#### In windows
- Open the config file: C:\Program Files\mosquitto\mosquitto.conf
- Add these and save 
    `listener 1883`
    `allow_anonymous true`
- Add inbound rule for firewall 
    - Run this in PowerShell as Admin
    `New-NetFirewallRule -DisplayName "Mosquitto MQTT" -Direction Inbound -Protocol TCP -LocalPort 1883 -Action Allow`
    - Restart mosqutto
    `net stop mosquitto`
    `net start mosquitto`

## Send commands
- Start all (run theese commands from main folder)
    `python -m src.scripts.send_mqtt_broadcast_start`
- Stop all
    `python -m src.scripts.send_mqtt_broadcast_stop`