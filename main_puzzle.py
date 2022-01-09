#!/usr/bin/python3
import time
import os
from datetime import datetime
import serial
import threading
import datetime as dt
import csv
import RPi.GPIO as GPIO
from tag_selection import right_list, left_list, both_list, puzzlebox_name


speed = 1 ###time in seconds fod closing the door
            ### Min speed 0.2sec

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
    
# Set pin 11 as an output, and define as servo1 as PWM pin
GPIO.setup(17,GPIO.OUT) #BLUE
servo1 = GPIO.PWM(17,50) # pin 11 for servo1, pulse 50Hz

# Set pin 11 as an output, and define as servo1 as PWM pin
GPIO.setup(18,GPIO.OUT) ## RED
servo2 = GPIO.PWM(18,50) # pin 11 for servo1, pulse 50Hz

# Start PWM running, with value of 0 (pulse off)
servo1.start(0)
servo2.start(0)
servo1.ChangeDutyCycle(7)
servo2.ChangeDutyCycle(5)
time.sleep(0.3)
servo1.ChangeDutyCycle(0)
servo2.ChangeDutyCycle(0)


#enable IR sensors
GPIO.setup(20,GPIO.IN) #GPIO 38 -> IR sensor RED
GPIO.setup(21, GPIO.IN) #GPIO 40 -> IR sensor BLUE


global id_tag
id_tag = ""
global tag_present
tag_present=0

class doorThread(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.state = 0
        self.displacement_flag = 0
        self.door_opened = 0

    def zero(self):
        #print(self.state)
        global csv_flag
        if csv_flag == 1 and dt.datetime.now().minute != 30:
            csv_flag = 0
            
        if csv_flag == 0 and dt.datetime.now().minute == 30:
            create_new_csv()
            csv_flag = 1
            

        global tag_present
        if tag_present:
            self.state=1
            
        elif(GPIO.input(21)==True):
            self.door_opened = 1
            time_stamp = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f').split()
            to_write_list = "{},{},{},{},{}".format("sensor error","right",time_stamp[0],time_stamp[1], puzzlebox_name)
            write_csv(to_write_list,file_name)
            print("sensor error right")
            self.state=4
        
        elif(GPIO.input(20)==True):
            self.door_opened = 1
            time_stamp = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S').split()
            to_write_list = "{},{},{},{},{}".format("sensor error","left",time_stamp[0],time_stamp[1], puzzlebox_name)
            write_csv(to_write_list,file_name)
            print("sensor error left")
            self.state=4
                
        else: 
            self.state =0        
        
    def one(self):
        print(self.state)
        global tag_present
        global id_tag

        if self.displacement_flag:
            print("reset flag")
        
        if not tag_present:
            self.displacement_flag = 0
            self.state=0
        else:
            print("checking lists")
            print(id_tag)
            if id_tag in both_list:
                ### Open Both servos
                servo1.ChangeDutyCycle(7)
                servo2.ChangeDutyCycle(5)
                time.sleep(0.3)
                servo1.ChangeDutyCycle(0)
                servo2.ChangeDutyCycle(0)
                self.displacement_flag = 0

                self.state = 2            
            elif id_tag in left_list:
                #open left servo
                servo1.ChangeDutyCycle(7)
                servo2.ChangeDutyCycle(10)
                time.sleep(0.3)
                servo1.ChangeDutyCycle(0)
                servo2.ChangeDutyCycle(0)
                self.displacement_flag = 0
                self.state=2
            
            elif id_tag in right_list:
                #open right
                servo1.ChangeDutyCycle(2)
                servo2.ChangeDutyCycle(5)
                time.sleep(0.3)
                servo1.ChangeDutyCycle(0)
                servo2.ChangeDutyCycle(0)
                self.displacement_flag = 0
                self.state=2
            else:
                print("Bird not in lists")
                if self.displacement_flag:
                    close_door(speed)
                    self.displacement_flag = 0
                self.state=2
#                 for i in range(1,48):
#                     servo1.ChangeDutyCycle(8-i/8)
#                     servo2.ChangeDutyCycle(2+i/8)
#                     time.sleep(0.02)
#                 servo1.ChangeDutyCycle(0)
#                 servo2.ChangeDutyCycle(0)
#                 self.state=1
                

    
    def two(self):
        global tag_present
        global id_tag
        if self.displacement_flag:
            print("displacement_flag {}".format(self.displacement_flag))
            self.state=1
            pass
        if not tag_present:
            self.state = 0
             ## Close door slowly
            close_door(speed)

        else:        
            if(GPIO.input(21)==True):
                time_stamp = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f').split()
                to_write_list = "{},{},{},{},{}".format(id_tag,"right",time_stamp[0],time_stamp[1],puzzlebox_name)
                write_csv(to_write_list,file_name)
                print("solve right")
                self.state = 3
        
            elif(GPIO.input(20)==True):
                time_stamp = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f').split()
                to_write_list = "{},{},{},{},{}".format(id_tag,"left",time_stamp[0],time_stamp[1],puzzlebox_name)
                write_csv(to_write_list,file_name)
                print("solve left")
                self.state = 3
            
     
    def three(self):
        global tag_present
        global id_tag
        
        #wait 1 second, close door.
        time.sleep(3)
        close_door(speed)
        self.state=0
        
    def four(self):
        if self.door_opened==1 and GPIO.input(21)==True or GPIO.input(20)==True:
            self.door_opened = 0
            self.state=0
            close_door(speed)
            time.sleep(10)

        else:
            self.state=0
    
    def state_switcher(self, i):
        switcher = {
            0:self.zero,
            1:self.one,
            2:self.two,
            3:self.three,
            4:self.four
            }
        func=switcher.get(i, lambda:"Invalid")
        return func()

    def thread_action(self):
        self.state_switcher(self.state)

    def run(self):
        print("Starting " + self.name)
        while 1:
            self.thread_action()
        print("Exiting " + self.name)

def close_door(speed):
    steps = int(speed/0.02) 
    servo1.ChangeDutyCycle(7)
    servo2.ChangeDutyCycle(5)
    time.sleep(0.3)    
    for i in range(1,steps):
        servo1.ChangeDutyCycle(7-i/(speed*10))
        servo2.ChangeDutyCycle(5+i/(speed*10))
        
        time.sleep(0.02)
        servo1.ChangeDutyCycle(0)
        servo2.ChangeDutyCycle(0)
    servo1.ChangeDutyCycle(0)
    servo2.ChangeDutyCycle(0)

close_door(speed)




def close_door3():
    servo1.ChangeDutyCycle(7)
    servo2.ChangeDutyCycle(5)
    time.sleep(0.3)    
    for i in range(1,5):
        servo1.ChangeDutyCycle(7-i)
        servo2.ChangeDutyCycle(5+i)
        
        time.sleep(0.02)
        servo1.ChangeDutyCycle(0)
        servo2.ChangeDutyCycle(0)
    servo1.ChangeDutyCycle(0)
    servo2.ChangeDutyCycle(0)

def close_door2():
    for i in range(1,100):
        servo1.ChangeDutyCycle(7-i/20)
        servo2.ChangeDutyCycle(5+i/20)
        time.sleep(0.02)
    servo1.ChangeDutyCycle(0)
    servo2.ChangeDutyCycle(0)

def write_csv(to_write_list,file_name):
    with open(file_name, "a") as savefile:
        savefile.write(to_write_list+"\n")

def mof_read(ser):
    ser.write("MOF\r".encode())
    print("MOF")
    time.sleep(2.5)
    while True:
        if ser.inWaiting() > 0:
            data = ser.read_until("\r".encode())[0:-1]
            print(data)
            return
        
def sd0_send(ser):
    ser.write("SD0\r".encode())
    print("SD0")
    time.sleep(2.5)
    while True:
        if ser.inWaiting() > 0:
            data = ser.read_until("\r".encode())[0:-1]
            print(data)
            return

def arrival_check(ser):
    global id_tag
    global tag_present
    global file_name
    while tag_present==0:
        if ser.inWaiting() > 0:
            id_tag = ser.read_until("\r".encode())[0:-1]
            id_tag = id_tag.decode("latin-1")
            print(id_tag)
            
            print (len(id_tag))
            if len(id_tag)==10:
                time_stamp = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f').split()
                print("{} arrived".format(id_tag[-10:]))
                write_csv("{},{},{},{},{}".format(id_tag,"arrived",time_stamp[0],time_stamp[1],puzzlebox_name),file_name)
                tag_present = 1
            else:
                pass
                print("bird left perch")
                    
    return tag_present, id_tag

def depart(ser):
    global id_tag
    global tag_present
    global file_name
    tolerance_limit = 0
    
    while tag_present==1:
        ser.write("RSD\r".encode())
        time.sleep(0.2)
        if ser.inWaiting() > 0:
            data = ser.read_until("\r".encode())[0:-1]
            data = data.decode("latin-1")
            print(data)
            if (data == "?1" or len(data) != 10):
                tolerance_limit +=1
                if tolerance_limit >= 10:
                    print("{} left".format(id_tag))
                    tag_present=0
                    time_stamp = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f').split()
                    write_csv("{},{},{},{},{}".format(id_tag,"departed",time_stamp[0],time_stamp[1],puzzlebox_name),file_name)
                    id_tag=""
                    
            elif(data[-10:] != id_tag and id_tag[-4:] not in data):
                print("displacement")
                time_stamp = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f').split()
                write_csv("{},{},{},{},{}".format(id_tag,"departed",time_stamp[0],time_stamp[1],puzzlebox_name),file_name)
                write_csv("{},{},{},{},{}".format(data[-10:],"displacement",time_stamp[0],time_stamp[1],puzzlebox_name),file_name)
                id_tag = data
                door_thread.displacement_flag = 1
                #
            
            else:
                tolerance_limit = 0
            
    return tag_present, id_tag

try:
    ser = serial.Serial('/dev/ttyAMA0', baudrate=9600,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,  
                        bytesize=serial.EIGHTBITS
                        )
except:
    print("error setting up serial port")

sd0_send(ser)
mof_read(ser)



#set up csv
if not os.path.exists("/home/pi/sonja_puzzlebox/data/"):
    os.makedirs("/home/pi/sonja_puzzlebox/data/")

#set file_name and timestamp for start of csv
global file_name
def create_new_csv():
    global file_name
    time_stamp = dt.datetime.now().strftime('%Y-%m-%d %H_%M_%S')
    file_name = "/home/pi/sonja_puzzlebox/data/{}_{}_RFID.txt".format(puzzlebox_name,time_stamp)

    with open(file_name, "a") as savefile:
        header = "ID, Event, YMD, Timestamp, Puzzle_name\n"
        #savefile.write("#{} start time: {} \n".format(puzzlebox_name,time_stamp))
        savefile.write(header)

create_new_csv()
global csv_flag
csv_flag = 0

#begin running solenoid and reed switch state machine for doors
door_thread = doorThread(1, "Door-Thread")
door_thread.start()



try:
    while True:
        if tag_present:
            print("tp: {}".format(tag_present))            
            tag_present, id_tag = depart(ser)            
            
        else:
            print("tp: {}".format(tag_present))
            tag_present, id_tag = arrival_check(ser)

except Exception as e:
    timestamp = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')    
    #print("an error has occurred during main execution at {}".format(timestamp)) 
    print(e)

finally:
    servo1.ChangeDutyCycle(0)
    servo2.ChangeDutyCycle(0)
    ser.close()
    GPIO.cleanup()
