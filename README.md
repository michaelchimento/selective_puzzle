# Manipulating actions: a selective two-option device for cognitive experiments in wild animals
**Authors**: *Sonja Wild, Gustavo Alarcon Nieto, Michael Chimento, Lucy M. Aplin*

## Abstract
1. Advances in biologging technologies have significantly improved our abilities to track individual animals' behaviour in their natural environment. Beyond observations, automation of data collection has revolutionised cognitive experiments in the wild. For example, radio-frequency identification (RFID) antennae embedded in 'puzzle-box' devices have allowed for large-scale cognitive experiments where individuals tagged with passive integrated transponder (PIT) tags interact with puzzle-boxes to gain a food reward, with devices logging both the identity and solving action of visitors.  
2. Here, we extended the scope of wild cognitive experiments by developing a fully automated selective two-option foraging device to specifically control which actions lead to a food reward and which remain unrewarded. Selective devices were based on a sliding-door foraging puzzle, and build using commercially available low-cost electronics.
3. We tested it on two free-ranging PIT-tagged sub-populations of great tits (Parus major) as a proof of concept. We conducted a cultural diffusion experiment where birds learned from trained demonstrators to get a food reward by sliding the door either to the left or right. We then restricted access of knowledgeable birds to their less preferred side and calculated the latency until birds produced solutions as a measure of behavioural flexibility.   
4. A total of 22 out of 23 knowledgeable birds produced at least one solution on their less preferred side after being restricted, with higher-frequency solvers being faster at doing so. In addition, 18 out of the 23 birds reached their solving rate from prior to the restriction on their less preferred side, with birds with stronger prior side preference taking longer to do so. 
5. We therefore introduce and successfully tested a new selective two-option puzzle-box, providing detailed instructions and freely available software that allows reproducibility. It extends the functionality of existing systems by allowing fine-scale manipulations of individuals' actions and opens a large range of possibilities to study cognitive processes in wild animal populations.

## Description
This repository contains the python code that controls the selective puzzlebox as described in the paper. This code is intended to run on Raspberry Pi 4 micro-computers.

### Files
| File      | Description |
| --- | --- |
| copy_rfid_data.sh | Shell script that copies the output csvs to the USB drive. This runs regularly as defined by the users crontab. |
| main_puzzle.py | Python script that contains the main code used to control the puzzle box. It is run automatically after boot. |
| puzzle_launcher.sh | Shell script that takes care of launching main_puzzle.py |
| tag_selection.py | Reads tags.csv and returns lists of IDs which can access one solution or the other, or both. |
| tags.csv | List of IDs and their respective access, with a tab separator. |

## Installation
From the terminal, run the following:
```
git clone https://github.com/michaelchimento/selective_puzzle.git
crontab -e:
#add the following cronjobs
@reboot sh /home/pi/selective_puzzle/puzzle_launcher.sh >> /home/pi/Desktop/logs 2>&1
0 * * * * sh /home/pi/selective_puzzle/copy_rfid_data.sh >> /home/pi/Desktop/logs 2>&1
```
Save the crontab and use chmod to make the shell files executable.
```
chmod +x /home/pi/selective_puzzle/puzzle_launcher.sh
chmod +x /home/pi/selective_puzzle/copy_rfid_data.sh
```
Rename your usb stick to INTENSO, or directly edit the code to accommodate a custom name. The stick must be plugged in before booting up the raspberry pi when running the code.

Finally, edit the boot config file by running
```
sudo nano /boot/config.txt
```
Add the following option
```
hdmi_force_hotplug=1
```
and save the file.

Reboot the raspberry pi and the main_puzzle.py should automatically begin. You can check this by running
```
pgrep -af python
```
