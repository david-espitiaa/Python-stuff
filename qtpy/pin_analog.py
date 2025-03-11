from PyQt5 import QtWidgets, uic
from pyfirmata import Arduino, util
import serial
import time

board = Arduino("COM9")


board.digital[13].write(1)

pin = board.get_pin('a:0:1')
it = util.Iterator(board)
board.analog[0].enable_reporting()
val_analog = board.analog[0].read()

print('el valor analogico: ' + str(val_analog))

while True:
    analog_value = pin.read()
    print(analog_value)
    time.sleep(1)