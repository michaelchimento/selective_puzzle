#!/bin/sh
# launches correct python scripts with directory management

cd /home/pi/selective_puzzle/
sleep 15
python3 -u main_puzzle.py >> log.txt&
exit 0
