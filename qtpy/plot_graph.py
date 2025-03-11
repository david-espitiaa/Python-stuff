#parte 1
import numpy as np
from PyQt5 import QtWidgets, uic
import pyqtgraph as pg

#parte 2
app = QtWidgets.QApplication([])
gui = uic.loadUi('graph.ui')

data = np.array([0])


#parte 3
def update_plot():
    global data 
    new_val = gui.dial.value()
    data = np.append(data, new_val)
    gui.lcd.display(new_val)
    plot()

def plot():
    gui.graph.plot(data, pen='g')

#parte 4
gui.dial.valueChanged.connect(update_plot)
gui.show()
app.exec()