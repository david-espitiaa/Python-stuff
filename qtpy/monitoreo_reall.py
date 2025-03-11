import random
import time
from PyQt5 import QtWidgets, uic, QtCore
import pyqtgraph as pg


app = QtWidgets.QApplication([])
gui = uic.loadUi("tony.ui")


start_time = time.time()

# Configuración del primer gráfico (Temperatura)
gui.widget.setBackground('w')
gui.widget.setTitle("Monitoreo de temperatura", color="r", size="15pt")
gui.widget.setLabel("left", "Valor medido", color="r", size=10)
gui.widget.setLabel("bottom", "Tiempo", color="r", size=10)
gui.widget.addLegend()
gui.widget.showGrid(x=True, y=True)
gui.widget.setYRange(0, 100, padding=0.1)
xdata = []
ydata = []
data_line_temp = gui.widget.plot(xdata, ydata, pen=pg.mkPen(color="g", width=2), name="Valor de temperatura")

# Configuración del segundo gráfico (Presión)
gui.widget_2.setBackground('b')
gui.widget_2.setTitle("Monitoreo de presión", color="r", size="15pt")
gui.widget_2.setLabel("left", "Valor medido", color="r", size=10)
gui.widget_2.setLabel("bottom", "Tiempo", color="r", size=10)
gui.widget_2.addLegend()
gui.widget_2.showGrid(x=True, y=True)
gui.widget_2.setYRange(0, 100, padding=0.1)
xdata_2 = []
ydata_2 = []
data_line_pres = gui.widget_2.plot(xdata_2, ydata_2, pen=pg.mkPen(color="g", width=2), name="Valor de presión")

# Configuración del temporizador
timer = QtCore.QTimer()
timer.setInterval(1000)

def update():
    global xdata, ydata, xdata_2, ydata_2
    new_temp = random.randint(30, 100)
    new_pres = random.randint(40, 100)
    tiempo_actual = time.time() - start_time

    # Actualizar datos para el gráfico de temperatura
    xdata.append(tiempo_actual)
    ydata.append(new_temp)
    
    # Actualizar datos para el gráfico de presión
    xdata_2.append(tiempo_actual)
    ydata_2.append(new_pres)

    # Limitar el número de puntos en el gráfico (por ejemplo, 10 puntos visibles)
    if len(xdata) > 10:
        xdata = xdata[1:]
        ydata = ydata[1:]
    if len(xdata_2) > 10:
        xdata_2 = xdata_2[1:]
        ydata_2 = ydata_2[1:]

    # Actualizar los gráficos
    data_line_temp.setData(xdata, ydata)
    data_line_pres.setData(xdata_2, ydata_2)

     # Alertas de temperatura y presión
    

def stopp():
    timer.stop()

def reset():
    global xdata, ydata, xdata_2, ydata_2, start_time
    xdata = []
    ydata = []
    xdata_2 = []
    ydata_2 = []
    data_line_temp.clear()
    data_line_pres.clear()
    start_time = time.time()
    timer.start()

# Conectar los botones de la interfaz
gui.stop.clicked.connect(stopp)
gui.reiniciar.clicked.connect(reset)

# Iniciar el temporizador y la actualización de datos
update()
timer.timeout.connect(update)
timer.start()

# Mostrar la GUI
gui.show()
app.exec_()


