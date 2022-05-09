import RPi.GPIO as GPIO
import time

ledPin = 11


def setup():
    GPIO.setmode(GPIO.BOARD)  # use PHYSICAL GPIO numbering
    GPIO.setup(ledPin, GPIO.OUT)
    GPIO.output(ledPin, GPIO.LOW)
    print('using pin%d' % ledPin)


def loop():
    while True:
        GPIO.output(ledPin, GPIO.HIGH)
        print('Led Turned on >>>')
        time.sleep(1)
        GPIO.output(ledPin, GPIO.LOW)
        print('Led Turned Off <<<')
        time.sleep(1)


def destroy():
    GPIO.cleanup()


if __name__ == '__main__':
    print('Program is starting ...\n')
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # press ctrl-c to terminate the program
        destroy()
