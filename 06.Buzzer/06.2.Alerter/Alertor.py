import RPi.GPIO as GPIO
import time
import math

buzzerPin = 11
buttonPin = 12


def setup():
    global p
    GPIO.setmode(GPIO.BOARD)
    # using physical GPIO numbering. it is used to set the serial number of GPIO which is based on physcial location of pin
    # This is GPIO17 amd GPIO18 corresponds to pin 11 and 12
    GPIO.setup(buzzerPin, GPIO.OUT)  # buzzerPin to Output mode
    # set buttonPin to PULL UP INPUT mode
    # buttonPin to input moe with pull resistor
    GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    p = GPIO.PWM(buzzerPin, 1)
    p.start(0)


def loop():
    while True:
        if GPIO.input(buttonPin) == GPIO.LOW:  # if button is pressed
            alertor()
            print('alertor turned on >>')
        else:  # if button is relessed
            # turn it off using LOW as output level
            stopAlertor()
            print('alertor turned off <<<')


def alertor():
    p.start(50)
    for x in range(0, 361):
        sinVal = math.sin(x*(math.pi/180.0))
        toneVal = 2000 + sinVal*500
        p.ChangeFrequency(toneVal)
        time.sleep(0.001)


def stopAlertor():
    p.stop()
    time.sleep(0.2)


def destroy():
    GPIO.output(buzzerPin, GPIO.LOW)
    GPIO.cleanup()                    # Release GPIO resource


if __name__ == '__main__':
    print('Program is starting...')
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # terminate app on ctrl-c
        destroy()
