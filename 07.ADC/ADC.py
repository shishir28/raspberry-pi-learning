import time
from ADCDevice import *

adc = ADCDevice()


def setup():
    global adc

    if(adc.detectI2C(0x4b)):
        adc = ADS7830()
    else:
        print("No correct I2C address found")
        exit(1)


def loop():
    while True:
        value = adc.analogRead(0)
        voltage = value / 255.0 * 3.3
        print('ADC value : %d, Voltage: $.2f' % (value, voltage))
        time.sleep(0.1)


def destroy():
    adc.close()


if __name__ == '__main__':
    print('Program is starting...')
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # terminate app on ctrl-c
        destroy()
