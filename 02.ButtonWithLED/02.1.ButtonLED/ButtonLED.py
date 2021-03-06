import RPi.GPIO as GPIO
import time

ledPin = 11    # we are defining ledPin here
buttonPin = 12    # we are defining button here


def setup():
    GPIO.setmode(GPIO.BOARD)
    # using physical GPIO numbering. it is used to set the serial number of GPIO which is based on physcial location of pin
    # This is GPIO17 amd GPIO18 corresponds to pin 11 and 12
    GPIO.setup(ledPin, GPIO.OUT)  # ledPin to Output mode
    # set buttonPin to PULL UP INPUT mode
    # buttonPin to input moe with pull resistor
    GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def loop():
    while True:
        if GPIO.input(buttonPin) == GPIO.LOW:  # if button is pressed
            # turn it on using HIGH as output level
            GPIO.output(ledPin, GPIO.HIGH)
            print('led turned on >>')
        else:  # if button is relessed
            # turn it off using LOW as output level
            GPIO.output(ledPin, GPIO.LOW)
            print('led turned off <<<')


def destroy():
    GPIO.output(ledPin, GPIO.LOW)     # turn off led at the end of program
    GPIO.cleanup()                    # Release GPIO resource


if __name__ == '__main__':
    print('Program is starting...')
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # terminate app on ctrl-c
        destroy()
