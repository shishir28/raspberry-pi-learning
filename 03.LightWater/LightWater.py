import RPi.GPIO as GPIO
import time

ledPins = [11, 12, 13, 15, 16, 18, 22, 3, 5, 24]


def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(ledPins, GPIO.OUT)  # All pins to output mode
    GPIO.output(ledPins, GPIO.HIGH)  # All leds pins to ON


def loop():
    while True:
        for ledPin in ledPins:  # Moving  from left to right
            GPIO.output(ledPin, GPIO.LOW)
            time.sleep(0.1)
            GPIO.output(ledPin, GPIO.HIGH)

        for ledPin in ledPins[::-1]:  # moving from right tp left
            GPIO.output(ledPin, GPIO.LOW)
            time.sleep(0.1)
            GPIO.output(ledPin, GPIO.HIGH)


def destroy():
    GPIO.cleanup()                    # Release GPIO resource


if __name__ == '__main__':
    print('Program is starting...')
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # terminate app on ctrl-c
        destroy()
