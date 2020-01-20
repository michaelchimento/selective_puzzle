import RPi.GPIO as IO
import time
IO.setwarnings(False)
IO.setmode(IO.BCM)

IO.setup(21,IO.IN) #GPIO 14 -> IR sensor as input

IO.setup(20,IO.IN) #GPIO 14 -> IR sensor as input

while 1:

    
    if(IO.input(21)==False): #object is near
        print("Red is open")
    elif(IO.input(20)==False): #object is near
        print("Blue is open")