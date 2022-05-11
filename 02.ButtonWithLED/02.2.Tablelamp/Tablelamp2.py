from gpiozero import LED, Button
from signal import pause

print('Program is starting..')

led = LED(17)  # using BCM numbering
button = Button(18)   # using BCM numbering


def onButtonPressed():

    led.toggle()
    if led.is_lit:
        print('Led turned on >>')
    else:
        print('Led turned off <<')


button.when_pressed = onButtonPressed

pause()
