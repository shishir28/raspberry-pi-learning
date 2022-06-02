import RPi.GPIO as GPIO
import time

# define the data bit that is transmitted  preferentially in the shiftout function
LSBFIRST = 1
MSBFIRST = 2

# define the pin for 74HC95
dataPin = 11  # DS Pin of 74HC95 (Pin 14)
latchPin = 13  # ST_CP Pin of 74HC95 (Pin 12)
clockPin = 15  # CH_CP Pin of 74HC95 (Pin 11)

pic = [0x1c, 0x22, 0x51, 0x45, 0x45, 0x51, 0x22, 0x1c]  # data of smiling face


data = [     # data of "0-F"
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,  # " "
    0x00, 0x00, 0x3E, 0x41, 0x41, 0x3E, 0x00, 0x00,  # "0"
    0x00, 0x00, 0x21, 0x7F, 0x01, 0x00, 0x00, 0x00,  # "1"
    0x00, 0x00, 0x23, 0x45, 0x49, 0x31, 0x00, 0x00,  # "2"
    0x00, 0x00, 0x22, 0x49, 0x49, 0x36, 0x00, 0x00,  # "3"
    0x00, 0x00, 0x0E, 0x32, 0x7F, 0x02, 0x00, 0x00,  # "4"
    0x00, 0x00, 0x79, 0x49, 0x49, 0x46, 0x00, 0x00,  # "5"
    0x00, 0x00, 0x3E, 0x49, 0x49, 0x26, 0x00, 0x00,  # "6"
    0x00, 0x00, 0x60, 0x47, 0x48, 0x70, 0x00, 0x00,  # "7"
    0x00, 0x00, 0x36, 0x49, 0x49, 0x36, 0x00, 0x00,  # "8"
    0x00, 0x00, 0x32, 0x49, 0x49, 0x3E, 0x00, 0x00,  # "9"
    0x00, 0x00, 0x3F, 0x44, 0x44, 0x3F, 0x00, 0x00,  # "A"
    0x00, 0x00, 0x7F, 0x49, 0x49, 0x36, 0x00, 0x00,  # "B"
    0x00, 0x00, 0x3E, 0x41, 0x41, 0x22, 0x00, 0x00,  # "C"
    0x00, 0x00, 0x7F, 0x41, 0x41, 0x3E, 0x00, 0x00,  # "D"
    0x00, 0x00, 0x7F, 0x49, 0x49, 0x41, 0x00, 0x00,  # "E"
    0x00, 0x00, 0x7F, 0x48, 0x48, 0x40, 0x00, 0x00,  # "F"
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,  # " "
]


def setup():
    GPIO.setmode(GPIO.BOARD)  # physical GPIO Numbering
    GPIO.setup(dataPin, GPIO.OUT)
    GPIO.setup(latchPin, GPIO.OUT)
    GPIO.setup(clockPin, GPIO.OUT)


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


def loop():

    while True:
        for j in range(0, 500):
            x = 0x80
            for i in range(0, 8):
                GPIO.output(latchPin, GPIO.LOW)
                # sending serial data to 74HC595
                shiftOut(dataPin, clockPin, MSBFIRST, pic[i])
                shiftOut(dataPin, clockPin, MSBFIRST, ~x)
                # output high level to latchPin and 74HC595 will update the data to parallel output
                GPIO.output(latchPin, GPIO.HIGH)
                time.sleep(0.001)
                x >>= 1

        for k in range(0, len(data)-8):
            for j in range(0, 20):
                x = 0x80
                for i in range(k, k+8):
                    print(i)
                    GPIO.output(latchPin, GPIO.LOW)
                    shiftOut(dataPin, clockPin, MSBFIRST, data[i])
                    shiftOut(dataPin, clockPin, MSBFIRST, ~x)
                    GPIO.output(latchPin, GPIO.HIGH)
                    time.sleep(0.001)
                    x >>= 1


def destroy():
    GPIO.cleanup()                    # Release GPIO resource


if __name__ == '__main__':
    print('Program is starting...')
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # terminate app on ctrl-c
        destroy()
