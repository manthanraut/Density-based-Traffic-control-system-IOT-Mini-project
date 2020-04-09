import RPi.GPIO as GPIO
import time
import signal
import sys
GPIO.setwarnings(False)
# use Raspberry Pi board pin numbers
GPIO.setmode(GPIO.BCM)

# set GPIO Pins

#FOR LANE A ultrasonic and LEDs
pinTrigger1 = 26
pinEcho1 = 13
RedLED1=17
GreenLED1=16
A=[26,13,17,16]
#FOR LANE B ultrasonic and LEDs 
pinTrigger2 = 19
pinEcho2 = 6
RedLED2=27
GreenLED2=20
B=[19,6,27,20]
com={'A':[26,13],'B':[19,6]}

def close(signal, frame):
    print("\nTurning off system...\n")
    GPIO.output(17,0)
    GPIO.output(16,0)
    GPIO.output(27,0)
    GPIO.output(20,0)
    GPIO.cleanup() 
    sys.exit(0)

signal.signal(signal.SIGINT, close)

# set GPIO input and output channels
GPIO.setup(pinTrigger1, GPIO.OUT)
GPIO.setup(pinEcho1, GPIO.IN)
GPIO.setup(RedLED1, GPIO.OUT)
GPIO.setup(GreenLED1, GPIO.OUT)

GPIO.setup(pinTrigger2, GPIO.OUT)
GPIO.setup(pinEcho2, GPIO.IN)
GPIO.setup(RedLED2, GPIO.OUT)
GPIO.setup(GreenLED2, GPIO.OUT)

GPIO.setup

minimum=[5.9,6.0,6.1,6.2,6.3]
maximum=[6.3,6.4,6.5,6.6]
while True:
    density=[]
    # set Trigger to HIGH
    for i,j in com.items():
        GPIO.output(j[0], True)
        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(j[0], False)
    
        startTime = time.time()
        stopTime = time.time()
        
    # save start time
        while 0 == GPIO.input(j[1]):
            startTime = time.time()
            
    # save time of arrival
        while 1 == GPIO.input(j[1]):
            stopTime = time.time()
        
    # time difference between start and arrival
        TimeElapsed = stopTime - startTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
        distance = (TimeElapsed * 34300) / 2
        
        print ("Distance on lane %s: %.1f cm"%(i,distance))
        density.append(round(distance,1))
        
    mini,maxi=min(density),max(density)
    if ((mini in minimum) and (maxi in maximum)):
        GPIO.output(17,1)
        GPIO.output(16,0)
        GPIO.output(27,0)
        GPIO.output(20,1)
        time.sleep(5)
        GPIO.output(17,0)
        GPIO.output(16,1)
        GPIO.output(27,1)
        GPIO.output(20,0)
        time.sleep(5)
    else:
        mini=min(density)
        print("Heavy Traffic is on road A" if density.index(mini)==0 else "Heavy Traffic is on road B")
        index=density.index(mini)
        if index==1:
            print("RED signal on A     GREEN signal on B")
            GPIO.output(17,1)
            GPIO.output(16,0)
            GPIO.output(27,0)
            GPIO.output(20,1)
            time.sleep(10)
        else:
            print("RED signal on B     GREEN signal on A")
            GPIO.output(17,0)
            GPIO.output(16,1)
            GPIO.output(27,1)
            GPIO.output(20,0)
            time.sleep(10)
            
    time.sleep(1)
    
