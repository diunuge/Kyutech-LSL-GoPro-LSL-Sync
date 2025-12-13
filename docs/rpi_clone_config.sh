#!/bin/bash

set -e

MOUNT_POINT="/mnt/newpi"

echo "======================================="
echo " Raspberry Pi Clone Preparation Script "
echo "======================================="

# Check mount
if [ ! -d "$MOUNT_POINT/etc" ]; then
    echo "ERROR: $MOUNT_POINT does not look like a mounted Raspberry Pi OS root filesystem."
    echo "Make sure the new SD card is mounted at $MOUNT_POINT"
    exit 1
fi

# Ask for hostname
read -rp "Enter new hostname (e.g. rsp2): " NEW_HOSTNAME

if [[ -z "$NEW_HOSTNAME" ]]; then
    echo "ERROR: Hostname cannot be empty."
    exit 1
fi

echo ""
echo "Setting hostname to: $NEW_HOSTNAME"

# Set hostname
echo "$NEW_HOSTNAME" | sudo tee "$MOUNT_POINT/etc/hostname" > /dev/null

# Update /etc/hosts
sudo sed -i "s/^127.0.1.1.*/127.0.1.1\t$NEW_HOSTNAME/" \
    "$MOUNT_POINT/etc/hosts"

# Reset machine-id (required for unique network identity)
echo "Resetting machine-id..."
sudo rm -f "$MOUNT_POINT/etc/machine-id"
sudo rm -f "$MOUNT_POINT/var/lib/dbus/machine-id"

# Remove SSH host keys (login credentials remain unchanged)
echo "Removing SSH host keys..."
sudo rm -f "$MOUNT_POINT/etc/ssh/ssh_host_"*

echo ""
echo "✔ Clone preparation complete"
echo ""
echo "What will happen on first boot:"
echo " - Hostname will be: $NEW_HOSTNAME"
echo " - machine-id regenerated automatically"
echo " - SSH host keys regenerated automatically"
echo " - Username & password unchanged"
echo " - Raspberry Pi Connect unchanged"
echo ""
echo "You may now safely unmount the SD card."