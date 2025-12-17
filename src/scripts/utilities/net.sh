#!/bin/bash
# Raspberry Pi 4 / 5 – NetworkManager
#
# USAGE:
#   sudo ./net_ip.sh auto eth0
#   sudo ./net_ip.sh static eth0 192.168.1.50 24 192.168.1.1 8.8.8.8
#   sudo ./net_ip.sh auto wlan0 
#   sudo ./net_ip.sh static wlan0 192.168.1.30 24 192.168.1.1 1.1.1.1

MODE="$1"
IFACE="$2"

if [[ -z "$MODE" || -z "$IFACE" ]]; then
    echo "Usage:"
    echo "  sudo $0 auto <iface>"
    echo "  sudo $0 static <iface> <ip> <prefix> <gateway> <dns>"
    exit 1
fi

# Find connection name
CON_NAME=$(nmcli -t -f NAME,DEVICE con show | grep ":$IFACE$" | cut -d: -f1)

if [[ -z "$CON_NAME" ]]; then
    echo "ERROR: No NetworkManager connection found for $IFACE"
    nmcli dev status
    exit 1
fi

echo "Interface: $IFACE"
echo "Connection: $CON_NAME"

case "$MODE" in
    auto)
        echo "→ Switching to DHCP (automatic)..."

        nmcli con mod "$CON_NAME" ipv4.method auto
        nmcli con mod "$CON_NAME" ipv4.addresses ""
        nmcli con mod "$CON_NAME" ipv4.gateway ""
        nmcli con mod "$CON_NAME" ipv4.dns ""

        ;;

    static)
        IP="$3"
        PREFIX="$4"
        GATEWAY="$5"
        DNS="$6"

        if [[ $# -ne 6 ]]; then
            echo "Usage: sudo $0 static <iface> <ip> <prefix> <gateway> <dns>"
            exit 1
        fi

        echo "→ Setting static IP..."

        nmcli con mod "$CON_NAME" \
            ipv4.method manual \
            ipv4.addresses "$IP/$PREFIX" \
            ipv4.gateway "$GATEWAY" \
            ipv4.dns "$DNS"
        ;;

    *)
        echo "Invalid mode: $MODE"
        echo "Use 'auto' or 'static'"
        exit 1
        ;;
esac

# Apply changes
nmcli con down "$CON_NAME"
nmcli con up "$CON_NAME"

echo "✔ Network updated"
ip addr show "$IFACE"