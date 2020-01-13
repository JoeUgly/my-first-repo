
# Select the correct USB port and give to usbreset


# Get the mouse bus number
hub=$(lsusb | grep "Optical Wheel Mouse" | cut -d ':' -f1 | grep -Eo [0-9]{3} | head -n 1)

# Get the mouse device number
port=$(lsusb | grep "Optical Wheel Mouse" | cut -d ':' -f1 | grep -Eo [0-9]{3} | tail -n 1)


# Run usbreset script with mouse info
sudo ~/code/usbreset /dev/bus/usb/$hub/$port



