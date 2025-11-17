# GoPro-LSL-Sync + MQTT Commander + Raspberry Pi Agents

This project provides a unified framework for:

1. **Controlling a GoPro Hero 11 Mini** using HTTP commands  
2. **Streaming time-synchronized LSL markers** for research workflows  
3. **Publishing MQTT commands from a PC** to control multiple Raspberry Pi devices  
4. **Running lightweight command agents on Raspberry Pis** to execute GPIO, sensors, cameras, or other actions  
5. **Coordinated timing across GoPro + Raspberry Pis** using LSL timestamps or MQTT messages

This system is designed for experiments, and multi-device synchronization setups.

---

## 🚀 Features

### 🎥 GoPro Integration
- Start/stop recording over HTTP  
- Send LSL markers: `START`, `STOP`, and periodic labels (`T0001`, `T0002`, …)  
- Timing drift correction for stable marker frequency  
- Compatible with LabRecorder, OpenViBE, MATLAB, etc.

### 🧠 LSL Marker Stream
- High-precision `local_clock()` timestamps  
- Configurable frequency  
- Robust StreamInfo + StreamOutlet wrappers  

### 📡 MQTT Commander (PC)
- Send commands to one or many Raspberry Pi devices  
- JSON-based command protocol  
- Broadcast topics + device-specific topics  
- Useful for synchronized triggering.

### 🍓 Raspberry Pi Agent
- Listens to MQTT commands  
- Executes actions (GPIO, camera, custom Python functions)  
<!-- - Optional heartbeat system  
- Modular device action system -->

---

## 📦 Repository Structure Overview