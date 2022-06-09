import RPi.GPIO as GPIO
import time


class Key(object):
    NO_KEY = '\0'
    IDLE = 0
    PRESSED = 1
    HOLD = 2
    RELEASED = 3
    OPEN = 0
    CLOSED = 1

    def __init__(self):
        self.kchar = self.NO_KEY
        self.kstate = self.IDLE
        self.kcode = -1
        self.stateChanged = False


class Keypad(object):
    NULL = '\0'
    LIST_MAX = 10
    MAPSIZE = 10
    bitMap = [0]*MAPSIZE
    key = [Key()]*LIST_MAX
    holdTime = 500
    holdTimer = 0
    startTime = 0

    def __init__(self, usrKeyMap, row_Pins, col_Pins, num_Rows, num_Cols):
        GPIO.setmode(GPIO.BOARD)
        self.rowPins = row_Pins
        self.colPins = col_Pins
        self.numRows = num_Rows
        self.numCols = num_Cols

        self.keymap = usrKeyMap
        self.setDebounceTime(10)

    def getKey(self):
        single_key = True
        if(self.getKeys() and self.key[0].stateChanged and (self.key[0].kstate == self.key[0].PRESSED)):
            return self.key[0].kchar
        single_key = False
        return self.key[0].NO_KEY

    def getKeys(self):
        keyActivity = False
        if((time.time() - self.startTime) > self.debounceTime*0.001):
            self.scanKeys()
            keyActivity = self.updateList()
            self.startTime = time.time()
        return keyActivity

    def scanKeys(self):
        for pin_r in self.rowPins:
            GPIO.setup(pin_r, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        for pin_c in self.colPins:
            GPIO.setup(pin_c, GPIO.OUT)
            GPIO.output(pin_c, GPIO.LOW)
            for r in self.rowPins:
                self.bitMap[self.rowPins.index(r)] = self.bitWrite(
                    self.bitMap[self.rowPins.index(r)], self.colPins.index(pin_c), not GPIO.input(r))
            GPIO.output(pin_c, GPIO.HIGH)
            GPIO.setup(pin_c, GPIO.IN)

    def updateList(self):
        anyActivity = False
        kk = Key()

        for item in range(self.LIST_MAX):
            if(self.key[item].kstate == kk.IDLE):
                self.key[item].kchar = kk.NO_KEY
                self.key[item].kcode = -1
                self.key[item].statechanged = False

        for r in range(self.numRows):
            for c in range(self.numCols):
                button = self.bitRead(self.bitMap[r], c)
                keyChar = self.keymap[r*self.numCols + c]
                keyCode = r * self.numCols + c
                idx = self.findInList(keyCode)

                if(idx > -1):
                    self.nextKeyState(idx, button)

                if((idx == -1) and button):
                    for i in range(self.LIST_MAX):
                        if(self.key[i].kchar == kk.NO_KEY):
                            self.key[i].kchar = keyChar
                            self.key[i].kcode = keyCode
                            self.key[i].kstate = kk.IDLE
                            self.nextKeyState(i, button)
                            break

        for i in range(self.LIST_MAX):
            if(self.key[i].stateChanged):
                anyActivity = True
        return anyActivity

    def nextKeyState(self, idx, button):
        self.key[idx].stateChanged = False
        kk = Key()
        if(self.key[idx].kstate == kk.IDLE):
            if (button == kk.CLOSED):
                self.transitionTo(idx, kk.PRESSED)
                self.holdTimer = time.time()
        elif (self.key[idx].kstate == kk.PRESSED):
            if((time.time() - self.holdTimer) > self.holdTime*0.001):
                self.transitionTo(idx, kk.HOLD)
            elif (button == kk.OPEN):
                self.transitionTo(idx, kk.RELEASED)
        elif (self.key[idx].kstate == kk.HOLD):
            if (button == kk.OPEN):
                self.transitionTo(idx, kk.RELEASED)
        elif (self.key[idx].kstate == kk.RELEASED):
            self.transitionTo(idx, kk.IDLE)

    def transitionTo(self, idx, nextState):
        self.key[idx].kstate = nextState
        self.key[idx].stateChanged = True

    def findInList(self, keyCode):
        for item in range(self.LIST_MAX):
            if(self.key[item].kcode == keyCode):
                return item
        return -1

    def setDebounceTime(self, ms):
        self.debounceTime = ms

    def setHoldTime(self, ms):
        self.holdTime = ms

    def isPressed(keyChar):
        for i in range(self.LIST_MAX):
            if(self.key[i].kchar == keyChar):
                if(self.key[i].kstate == self.self.key[i].PRESSED and self.key[i].stateChanged):
                    return True
        return False

    def waitForKey():
        kk = key()
        waitKey = kk.NO_KEY
        while(waitKey == kk.NO_KEY):
            waitKey = getKey()
        return waitKey

    def getState():
        return self.key[0].kstate

    def keyStateChanged():
        return self.key[0].stateChanged

    def bitWrite(self, x, n, b):
        if(b):
            x |= (1 << n)
        else:
            x &= (~(1 << n))
        return x

    def bitRead(self, x, n):
        if((x >> n) & 1 == 1):
            return True
        else:
            return False
