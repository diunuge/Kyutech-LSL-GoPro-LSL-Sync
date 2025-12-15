#!/bin/bash

set -e

MOUNT_POINT="/mnt/newpi"

echo "======================================="
echo " Raspberry Pi Clone Preparation Script "
echo "======================================="

# Require root
if [ "$EUID" -ne 0 ]; then
  echo "ERROR: Please run as root (use sudo)."
  exit 1
fi

# Ask for device
lsblk -o NAME,SIZE,MODEL
echo ""
read -rp "Enter the NEW SD card device (e.g. sda): " DEV

if [ ! -b "/dev/$DEV" ]; then
  echo "ERROR: /dev/$DEV does not exist."
  exit 1
fi

# Safety check: refuse root filesystem
ROOT_DEV=$(lsblk -no PKNAME "$(df / | tail -1 | awk '{print $1}')" 2>/dev/null)
if [ "$DEV" = "$ROOT_DEV" ]; then
  echo "ERROR: Refusing to modify the running system."
  exit 1
fi

# Mount partitions
echo "Mounting /dev/${DEV}..."
mkdir -p "$MOUNT_POINT"

mount "/dev/${DEV}2" "$MOUNT_POINT"
mount "/dev/${DEV}1" "$MOUNT_POINT/boot"

# Verify Raspberry Pi OS
if [ ! -f "$MOUNT_POINT/etc/os-release" ]; then
  echo "ERROR: This does not look like Raspberry Pi OS."
  umount "$MOUNT_POINT/boot"
  umount "$MOUNT_POINT"
  exit 1
fi

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

# Set hostname persistence in cloud-init (if present)
if [ -f "$MOUNT_POINT/etc/cloud/cloud.cfg" ]; then
    echo "Updating cloud-init configuration..."
    sudo sed -i "s/^\(preserve_hostname:\).*/\1 true/" \
        "$MOUNT_POINT/etc/cloud/cloud.cfg"

    # Ensure manage_etc_hosts: false is present (append if missing)
    grep -q '^manage_etc_hosts:' "$MOUNT_POINT/etc/cloud/cloud.cfg" || \
    echo 'manage_etc_hosts: false' | sudo tee -a "$MOUNT_POINT/etc/cloud/cloud.cfg" >/dev/null

    # If it exists already but as true, flip it:
    sudo sed -i 's/^\(manage_etc_hosts:\).*/\1 false/' \
        "$MOUNT_POINT/etc/cloud/cloud.cfg"
fi

# Reset machine-id (required for unique network identity)
echo "Resetting machine-id..."
sudo rm -f "$MOUNT_POINT/etc/machine-id"
sudo rm -f "$MOUNT_POINT/var/lib/dbus/machine-id"

# 2) Create an empty file so systemd knows to initialize
sudo touch "$MOUNT_POINT/etc/machine-id"
sudo chmod 0444 "$MOUNT_POINT/etc/machine-id"

# Show confirmation
echo ""
echo "✔ Verification:"
cat "$MOUNT_POINT/etc/hostname"

# Unmount cleanly
echo ""
echo "Unmounting SD card..."
umount "$MOUNT_POINT/boot"
umount "$MOUNT_POINT"
sync

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