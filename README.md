# sonja_puzzlebox
code for sonja wild's puzzlebox

install:
git clone https://github.com/michaelchimento/sonja_puzzlebox.git

in crontab -e:

@reboot sh /home/pi/sonja_puzzlebox/puzzle_launcher.sh >> /home/pi/Desktop/logs 2>&1
0 * * * * sh /home/pi/sonja_puzzlebox/copy_rfid_data.sh >> /home/pi/Desktop/logs 2>&1

don't forget to chmod +x both of the sh files

make sure usb stick named INTENSO is plugged in before boot

also add hdmi_force_hotplug=1 option to /boot/config.txt to make sure usb is automounted when headlessly booted
