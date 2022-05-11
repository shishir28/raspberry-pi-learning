from gpiozero import LED, Button
from signal import pause

print('Program is starting..')

led = LED(17)  # using BCM numbering
button = Button(18)   # using BCM numbering


def onButtonPressed():
    led.on()
    print('Button is pressed , led turned on >>')


def onButtonReleased():
    led.off()
    print('Button is released , led turned off <<')


button.when_pressed = onButtonPressed
button.when_released = onButtonReleased

pause()
