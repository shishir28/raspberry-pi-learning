import RPi.GPIO as GPIO
import time
import random

pins = [11, 12, 13]  # we are defining pin here R:11,G:12 and B:13


def setup():
    global pwmRed, pwmGreen, pwmBlue
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pins, GPIO.OUT)
    GPIO.output(pins, GPIO.HIGH)
    # setting pwmRed for R:11 with frequency 2000 Hz
    pwmRed = GPIO.PWM(pins[0], 2000)
    pwmGreen = GPIO.PWM(pins[1], 2000)  # setting pwmGreen for R:12
    pwmBlue = GPIO.PWM(pins[2], 2000)
    pwmRed.start(0)  # setting initial duty cycle
    pwmGreen.start(0)
    pwmBlue.start(0)


def setColor(r_val, g_val, b_val):
    pwmRed.ChangeDutyCycle(r_val)
    pwmGreen.ChangeDutyCycle(g_val)
    pwmBlue.ChangeDutyCycle(b_val)


def loop():
    while True:
        r = random.randint(0, 100)
        g = random.randint(0, 100)
        b = random.randint(0, 100)
        setColor(r, g, b)

        print('r=%d, g=%d, b=%d', r, g, b)
        time.sleep(1)


def destroy():
    pwmRed.stop()  # stop PWM
    pwmGreen.stop()  # stop PWM
    pwmBlue.stop()  # stop PWM
    GPIO.cleanup()  # release all GPIO


if __name__ == '__main__':
    print('We are starting it up :-)')
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # terminate app on ctrl-c
        destroy()
