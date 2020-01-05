import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Reed Blue
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #Reed Red

while True:
    if(GPIO.input(21)==True):
        print("solve red")
    elif(GPIO.input(25)==True):
        print("solve blue")