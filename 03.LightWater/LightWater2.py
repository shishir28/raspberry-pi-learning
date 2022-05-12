from gpiozero import LEDBoard
from time import sleep
from signal import pause

print('Program is starting..')

ledPins = ["J8:11", "J8:12", "J8:13", "J8:15",
           "J8:16", "J8:18", "J8:22", "J8:3", "J8:5", "J8:24"]

leds = LEDBoard(*ledPins, active_high=False)

while True:
    for index in range(0, len(ledPins), 1):
        leds.on(index)
        sleep(0.1)
        leds.off(index)

    for index in range(len(ledPins)-1, -1, -1):
        leds.on(index)
        sleep(0.1)
        leds.off(index)
