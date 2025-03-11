#parte 1 importar bibliotecas
import pyfirmata as fir
import time
from PyQt5 import QtWidgets, uic

#parte 2 - configurar
a = fir.Arduino('COM9')


#parte 3 - funciones de apoyo
def LED():
    for i in range(5):
        a.digital[13].write(1)
        time.sleep(2)
        a.digital[13].write(0)
        time.sleep(2)

#parte 4 - ejecucuion 
if __name__ == "__main__":
    LED()