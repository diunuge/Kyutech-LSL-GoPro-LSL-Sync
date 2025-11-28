Raspberry PI

connect to wifi

sudo nmcli device wifi connect "HERO 11 Black Mini 1" password "zqk-FQK-Xnt"

configure python

sudo apt update

sudo apt install mosquitto mosquitto-clients
sudo systemctl enable mosquitto
sudo systemctl start mosquitto
systemctl status mosquitto # make sure it is enabled


sudo apt install python3-venv
#create virtual environment 
mkdir ../LSL
cd ../LSL
python3 -m venv venv
#activate virtual environment
source venv/bin/activate

pip install pylsl

download liblsll https://github.com/sccn/liblsl/releases/download/v1.16.2/liblsl-1.16.2-bookworm_arm64.deb
Extract it
Copy liblsl.so into pylsl’s folder
lib/liblsl.so LSL/Program/venv/lib/python3.13/site-packages/pylsl/lib/

#deactivate when done
deavtivate

sudo apt install jq
curl -s http://10.5.5.9/gp/gpControl/status | jq '.status["10"] == 1'
python3 -c "import requests,sys; print(requests.get('http://10.5.5.9/gp/gpControl/status').json()['status']['10']==1)"


