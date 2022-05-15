import RPi.GPIO as GPIO
import time

ledPin = 12  # we are defining ledPin here


def setup():
    global p
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(ledPin, GPIO.OUT)
    GPIO.output(ledPin, GPIO.LOW)
    p = GPIO.PWM(ledPin, 500)  # settimg the frequency 500Hz
    p.start(0)  # starting PWM with initial Duty Cycle of 0


def loop():
    while True:
        for dc in range(0, 101, 1):
            # in each step making it more bighter.
            # Longer PWM duty cycle is, higher the outout of power will be
            p.ChangeDutyCycle(dc)
            time.sleep(0.1)
        time.sleep(1)
        for dc in range(100, -1, -1):
            p.ChangeDutyCycle(dc)  # in each step making it more darker
            time.sleep(0.1)
        time.sleep(1)


def destroy():
    p.stop()  # stop PWM
    GPIO.cleanup()  # release all GPIO


if __name__ == '__main__':
    print('We are starting it up :-)')
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # terminate app on ctrl-c
        destroy()
