import RPi.GPIO as GPIO
import time

# define the data bit that is transmitted  preferentially in the shiftout function
LSBFIRST = 1
MSBFIRST = 2

# define the pin for 74HC95
dataPin = 11  # DS Pin of 74HC95 (Pin 14)
latchPin = 13  # ST_CP Pin of 74HC95 (Pin 12)
clockPin = 15  # CH_CP Pin of 74HC95 (Pin 11)


def setup():
    GPIO.setmode(GPIO.BOARD)  # physical GPIO Numbering
    GPIO.setup(dataPin, GPIO.OUT)
    GPIO.setup(latchPin, GPIO.OUT)
    GPIO.setup(clockPin, GPIO.OUT)


# shiftOut function, output values with bits in order. Order is high or low
def shiftOut(dPin, cPin, order, val):
    for item in range(0, 8):
        GPIO.output(cPin, GPIO.LOW)
        if(order == LSBFIRST):  # Left to right flow
            GPIO.output(dPin, (0x01 & (val >> item) == 0x01)
                        and GPIO.HIGH or GPIO.LOW)
        elif(order == MSBFIRST):  # right to left flow
            GPIO.output(dPin, (0x80 & (val << item) == 0x80)
                        and GPIO.HIGH or GPIO.LOW)

        GPIO.output(cPin, GPIO.HIGH)

# 74HC595 chip is sued to convert serial data into parallel data. One byte into 8 bits and send to corresponding 8 ports
# hence expands IO ports of Raspberry Pi.


def loop():
    while True:
        x = 0x01
        for item in range(0, 8):
            GPIO.output(latchPin, GPIO.LOW)
            # sending serial data to 74HC595
            shiftOut(dataPin, clockPin, LSBFIRST, x)
            # output high level to latchPin and 74HC595 will update the data to parallel output
            GPIO.output(latchPin, GPIO.HIGH)
            x <<= 1  # move one bit left so that LED move one step in left
            time.sleep(0.1)
        x = 0x80
        for item in range(0, 8):
            GPIO.output(latchPin, GPIO.LOW)
            shiftOut(dataPin, clockPin, LSBFIRST, x)
            GPIO.output(latchPin, GPIO.HIGH)
            x >>= 1  # move one bit right so that LED move one step in right
            time.sleep(0.1)


def destroy():
    GPIO.cleanup()                    # Release GPIO resource


if __name__ == '__main__':
    print('Program is starting...')
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # terminate app on ctrl-c
        destroy()
