import RPi.GPIO as GPIO
import time
import threading

# define the data bit that is transmitted  preferentially in the shiftout function
LSBFIRST = 1
MSBFIRST = 2

# define the pin for 74HC95
dataPin = 18  # DS Pin of 74HC95 (Pin 14)
latchPin = 16  # ST_CP Pin of 74HC95 (Pin 12)
clockPin = 12  # CH_CP Pin of 74HC95 (Pin 11)

# Character 0-9 code of common anode 7-desgment display : following are in a way unsigned charcter num
num = (0xc0, 0xf9, 0xa4, 0xb0, 0x99, 0x92, 0x82, 0xf8, 0x80, 0x90)
digitPin = (11, 13, 15, 19)  # Define 7-Segment display common pin
counter = 0  # this number will be displayed by 7-Segment display
t = 0


def setup():
    GPIO.setmode(GPIO.BOARD)  # physical GPIO Numbering
    GPIO.setup(dataPin, GPIO.OUT)
    GPIO.setup(latchPin, GPIO.OUT)
    GPIO.setup(clockPin, GPIO.OUT)
    for pin in digitPin:
        GPIO.setup(pin, GPIO.OUT)


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


def outData(data):  # function used to output data for
    GPIO.output(latchPin, GPIO.LOW)
    shiftOut(dataPin, clockPin, MSBFIRST, data)
    GPIO.output(latchPin, GPIO.HIGH)


def selectDigit(digit):  # open pne of the 7-segment display and close the remaining
    GPIO.output(digitPin[0], GPIO.LOW if (
        (digit & 0x08) == 0x08) else GPIO.HIGH)
    GPIO.output(digitPin[1], GPIO.LOW if (
        (digit & 0x04) == 0x04) else GPIO.HIGH)
    GPIO.output(digitPin[2], GPIO.LOW if (
        (digit & 0x02) == 0x02) else GPIO.HIGH)
    GPIO.output(digitPin[3], GPIO.LOW if (
        (digit & 0x01) == 0x01) else GPIO.HIGH)


def display(dec):
    outData(0xff)  # eliminate residual display
    selectDigit(0x01)  # select the first and display the single digit
    outData(num[dec % 10])
    time.sleep(0.003)
    outData(0xff)
    selectDigit(0x02)  # select the second  and display the ten digit
    outData(num[dec % 100//10])
    time.sleep(0.003)
    outData(0xff)  # eliminate residual display
    selectDigit(0x04)  # select the third  and display the hundred digit
    outData(num[dec % 10000//100])
    time.sleep(0.003)
    outData(0xff)
    selectDigit(0x08)   # Select the fourth, and display the thousands digit
    outData(num[dec % 10000//1000])
    time.sleep(0.003)


def timer():
    global counter
    global t
    t = threading.Timer(1.0, timer)
    t.start()
    counter += 1
    print("counter : %d" % counter)


def loop():
    global t
    global counter
    t = threading.Timer(1.0, timer)
    t.start()
    while True:
        display(counter)


def destroy():
    global t
    GPIO.cleanup()
    t.Cancel()


if __name__ == '__main__':
    print('Program is starting...')
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # terminate app on ctrl-c
        destroy()
