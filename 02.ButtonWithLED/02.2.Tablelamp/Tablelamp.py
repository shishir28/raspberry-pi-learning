import RPi.GPIO as GPIO
import time

ledPin = 11    # we are defining ledPin here
buttonPin = 12    # we are defining button here
ledstate = False


def setup():
    GPIO.setmode(GPIO.BOARD)
    # using physical GPIO numbering. it is used to set the serial number of GPIO which is based on physcial location of pin
    # This is GPIO17 amd GPIO18 corresponds to pin 11 and 12
    GPIO.setup(ledPin, GPIO.OUT)  # ledPin to Output mode
    # set buttonPin to PULL UP INPUT mode
    # buttonPin to input moe with pull resistor
    GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def buttonEvent(channel):  # invoked when button is pressed
    global ledstate
    print('buttonEvent GPIO%d' % channel)
    ledstate = not ledstate
    if ledstate: 
        print('led turned on >>')
    else:
        print('led turned off <<<')
    GPIO.output(ledPin, ledstate)


def loop():
    # Following code eliminates jitter , it uses callback function
    GPIO.add_event_detect(buttonPin, GPIO.FALLING,
                          callback=buttonEvent, bouncetime=300)
    while True:
        pass


def destroy():

    GPIO.cleanup()                    # Release GPIO resource


if __name__ == '__main__':
    print('Program is starting...')
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # terminate app on ctrl-c
        destroy()
