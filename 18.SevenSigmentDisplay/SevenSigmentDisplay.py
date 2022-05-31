import RPi.GPIO as GPIO
import time

# define the data bit that is transmitted  preferentially in the shiftout function
LSBFIRST = 1
MSBFIRST = 2

# define the pin for 74HC95
dataPin = 11  # DS Pin of 74HC95 (Pin 14)
latchPin = 13  # ST_CP Pin of 74HC95 (Pin 12)
clockPin = 15  # CH_CP Pin of 74HC95 (Pin 11)

num = [0xc0, 0xf9, 0xa4, 0xb0, 0x99, 0x92, 0x82,
       0xf8, 0x90, 0x88, 0x83, 0xc6, 0xa1, 0x86, 0x8e]


def setup():
    GPIO.setmode(GPIO.BOARD)  # physical GPIO Numbering
    GPIO.setup(dataPin, GPIO.OUT)
    GPIO.setup(latchPin, GPIO.OUT)
    GPIO.setup(clockPin, GPIO.OUT)

# shiftOut function, output values with bits in order. Order is high or low


def shiftOut(dPin, cPin, order, val):
    --print(val)
    for item in range(0, 8):
        GPIO.output(cPin, GPIO.LOW)
        if(order == LSBFIRST):  # Left to right flow
            GPIO.output(dPin, (0x01 & (val >> item) == 0x01)
                        and GPIO.HIGH or GPIO.LOW)
        elif(order == MSBFIRST):  # right to left flow
            GPIO.output(dPin, (0x80 & (val << item) == 0x80)
                        and GPIO.HIGH or GPIO.LOW)

        GPIO.output(cPin, GPIO.HIGH)


def loop():

    while True:
        for item in range(0, len(num)):
            GPIO.output(latchPin, GPIO.LOW)
            # sending serial data to 74HC595
            shiftOut(dataPin, clockPin, MSBFIRST, num[item])
            # output high level to latchPin and 74HC595 will update the data to parallel output
            GPIO.output(latchPin, GPIO.HIGH)
            time.sleep(0.5)

        for item in range(0, len(num)):
            GPIO.output(latchPin, GPIO.LOW)
            shiftOut(dataPin, clockPin, MSBFIRST, num[item] & 0x7f)
            GPIO.output(latchPin, GPIO.HIGH)
            time.sleep(0.5)


def destroy():
    GPIO.cleanup()                    # Release GPIO resource


if __name__ == '__main__':
    print('Program is starting...')
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # terminate app on ctrl-c
        destroy()
