# sonja_puzzlebox
code for sonja wild's puzzlebox

install:
git clone https://github.com/michaelchimento/sonja_puzzlebox.git

in crontab -e:

@reboot sh /home/pi/sonja_puzzlebox/puzzle_launcher.sh >> /home/pi/Desktop/logs 2>&1
0 * * * * sh /home/pi/sonja_puzzlebox/copy_rfid_data.sh

don't forget to chmod +x the sh files
