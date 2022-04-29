#!/usr/bin/python3

import csv

#allows csvreader to ignore commented lines, marked with a hash
def decomment(csvfile):
    for row in csvfile:
        raw = row.split('#')[0].strip()
        if raw: yield raw

#IMPORTANT: make sure you change this file path to wherever you're keeping the tag list
with open('/media/pi/INTENSO/tags.txt') as csvfile:
    data= csv.reader(decomment(csvfile), delimiter='\t')
    bird_data_table = [row for row in data]
    print(bird_data_table)

#create dictionary with (key,value) = (PITcode, door_access)
bird_dict = dict(bird_data_table)

#create lists to be imported into sonja_puzzle_rev2
right_list = [key  for (key, value) in bird_dict.items() if value == "right"]
left_list = [key  for (key, value) in bird_dict.items() if value == "left"]
both_list = [key  for (key, value) in bird_dict.items() if value == "both"]

#use this to set puzzle location, will be used in data filename
puzzlebox_name = "Test_Puzzle"

