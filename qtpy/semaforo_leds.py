#Paso 1 - Importar librerías    
import pyfirmata as fir
from PyQt5 import QtWidgets, uic, QtGui
import time

#Paso 2 - Iniciar App y Configuración
app = QtWidgets.QApplication([])
gui1 = uic.loadUi('semaforo.ui')
global a
a=fir.Arduino('COM9')

#Paso 3 - Funciones de Apoyo
def btnon():
    global a
    for i in range(10):
        a.digital[10].write(0)
        a.digital[6].write(1)
        time.sleep(1)
        a.digital[6].write(0)
        a.digital[7].write(1)
        time.sleep(1)
        a.digital[7].write(0)
        a.digital[10].write(1)
        time.sleep(1)

def btnoff():
    global a
    x = 1
    a.digital[6].write(0)
    a.digital[7].write(0)
    a.digital[10].write(0)

def btnexit():
    global a
    a.close()
    gui1.destroy()
    exit()

# Paso 4 - Acciones
gui1.btnon.clicked.connect(btnon)
gui1.btnoff.clicked.connect(btnoff)
gui1.btnexit.clicked.connect(btnexit)

gui1.show()
app.exec()