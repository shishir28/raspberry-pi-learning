import RPi.GPIO as GPIO
import time
OFFSET_DUTY = 0.5        # lastig time 0.5ms to 2.5 ms of signal cycle
# define pulse duty cycle for minimum angle of servo
SERVO_MIN_DUTY = 2.5 + OFFSET_DUTY
# define pulse duty cycle for maximum angle of servo
SERVO_MAX_DUTY = 12.5 + OFFSET_DUTY
SERVO_DELAY_SEC = 0.001
servoPin = 12


def setup():
    global p
    GPIO.setmode(GPIO.BOARD)  # physical GPIO Numbering
    GPIO.setup(servoPin, GPIO.OUT)
    GPIO.output(servoPin, GPIO.LOW)

    p = GPIO.PWM(servoPin, 50)
    p.start(0)


def servoWrite(angle):
    if (angle < 0):
        angle = 0
    elif (angle > 180):
        angle = 180

    dc = SERVO_MIN_DUTY + (SERVO_MAX_DUTY - SERVO_MIN_DUTY) * \
        angle / 180.0  # map the angle to duty cycle
    p.ChangeDutyCycle(dc)


def loop():
    while True:
        for angle in range(0, 181, 1):  # from 0 to 180 degree
            servoWrite(angle)
            time.sleep(SERVO_DELAY_SEC)
        time.sleep(0.5)
        for angle in range(180, -1, -1):  # from 180 to 0 degree
            servoWrite(angle)
            time.sleep(SERVO_DELAY_SEC)
        time.sleep(0.5)


def destroy():
    p.stop()
    GPIO.cleanup()                    # Release GPIO resource


if __name__ == '__main__':
    print('Program is starting...')
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # terminate app on ctrl-c
        destroy()
