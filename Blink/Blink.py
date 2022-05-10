import RPi.GPIO as GPIO
import time

ledPin = 11  # we are defining ledPin here


def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(ledPin, GPIO.OUT)
    GPIO.output(ledPin, GPIO.LOW)
    print('using pin%d' % ledPin)


def loop():
    while True:
        GPIO.output(ledPin, GPIO.HIGH)  # turn it on using HIGH as output level
        print('led turned on >>')
        time.sleep(1)
        GPIO.output(ledPin, GPIO.LOW)  # turn it off using LOW as output level
        print('led turned off <<<')
        time.sleep(1)


def destroy():
    GPIO.cleanup()  # release all GPIO


if __name__ == '__main__':
    print('We are starting it up :-) ')
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # terminate app on ctrl-c
        destroy()
