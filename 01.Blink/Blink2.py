from gpiozero import LED
from time import sleep

print('Program is starting..')

led = LED(17)

while True:
    led.on()
    print('led turned on >>')
    sleep(1)
    led.off()
    print('led turned off <<<')
    sleep(1)
