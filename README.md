# sonja_puzzlebox
code for sonja wild's puzzlebox


in crontab -e:

@reboot sh /home/pi/Desktop/sonja_puzzle_rev2/puzzle_launcher.sh >> /home/pi/Desktop/logs 2>&1
0 * * * * sh /home/pi/Desktop/sonja_puzzle_rev2/copy_rfid_data.sh

don't forget to chmod +x the sh files
