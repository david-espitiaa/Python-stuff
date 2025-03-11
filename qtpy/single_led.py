#Paso 1 - Importar librerías    
import pyfirmata as fir
from PyQt5 import QtWidgets, uic, QtGui

#Paso 2 - Iniciar App y Configuración
app = QtWidgets.QApplication([])
gui1 = uic.loadUi('single_led.ui')
global a
a=fir.Arduino('COM9')
a.digital[10].mode = fir.PWM

#Paso 3 - Funciones de Apoyo

def btnon():
    global a
    a.digital[6].write(1)

def btnoff():
    global a
    a.digital[6].write(0)

def btnexit():
    global a
    a.close()
    gui1.destroy()
    exit()

def slider():
    global a
    val =  gui1.slider.value()
    val = float(val/10)
    print(val)
    a.digital[10].write(val)

# Paso 4 - Acciones
gui1.btnon.clicked.connect(btnon)
gui1.btnoff.clicked.connect(btnoff)
gui1.btnexit.clicked.connect(btnexit)
gui1.slider.valueChanged.connect(slider)

gui1.show()
app.exec()

