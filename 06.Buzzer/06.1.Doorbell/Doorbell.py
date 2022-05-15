import RPi.GPIO as GPIO

buzzerPin = 11
buttonPin = 12


def setup():
    GPIO.setmode(GPIO.BOARD)
    # using physical GPIO numbering. it is used to set the serial number of GPIO which is based on physcial location of pin
    # This is GPIO17 amd GPIO18 corresponds to pin 11 and 12
    GPIO.setup(buzzerPin, GPIO.OUT)  # buzzerPin to Output mode
    # set buttonPin to PULL UP INPUT mode
    # buttonPin to input moe with pull resistor
    GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def loop():
    while True:
        if GPIO.input(buttonPin) == GPIO.LOW:  # if button is pressed
            # turn it on using HIGH as output level
            GPIO.output(buzzerPin, GPIO.HIGH)
            print('buzzer turned on >>')
        else:  # if button is relessed
            # turn it off using LOW as output level
            GPIO.output(buzzerPin, GPIO.LOW)
            print('buzzer turned off <<<')


def destroy():
    GPIO.cleanup()                    # Release GPIO resource


if __name__ == '__main__':
    print('Program is starting...')
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # terminate app on ctrl-c
        destroy()
