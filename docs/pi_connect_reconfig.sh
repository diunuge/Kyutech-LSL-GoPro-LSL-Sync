#!/bin/bash

set -e

# reconfigure rpi-connect on a cloned Raspberry Pi OS SD card
rpi-connect status
rpi-connect off
rpi-connect signoff

rpi-connect on
rpi-connect signin
api-connect status
