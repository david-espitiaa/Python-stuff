import random
import time
from PyQt5 import QtWidgets, uic, QtCore
import pyqtgraph as pg

app = QtWidgets.QApplication([])
gui = uic.loadUi("practica2.ui")

start_time = time.time()

# Configuración del primer gráfico (Temperatura)
gui.widget.setBackground('w')  # Fondo blanco
gui.widget.setTitle("Monitoreo de Temperatura", color="r", size="18pt")  # Título en azul
gui.widget.setLabel("left", "Valor Medido (°C)", color="r", size="12pt")  # Etiqueta del eje izquierdo
gui.widget.setLabel("bottom", "Tiempo (s)", color="r", size="12pt")  # Etiqueta del eje inferior
gui.widget.addLegend()
gui.widget.showGrid(x=True, y=True, alpha=0.5)  # Mostrar grilla con transparencia
gui.widget.setYRange(0, 150, padding=0.1)  # Rango ajustado
xdata = []
ydata = []
data_line_temp = gui.widget.plot(xdata, ydata, pen=pg.mkPen(color="r", width=3, style=pg.QtCore.Qt.SolidLine), name="Temperatura")  # Línea sólida y roja

# Configuración del segundo gráfico (Nivel)
gui.widget_2.setBackground('w')  
gui.widget_2.setTitle("Monitoreo de Nivel de Agua", color="b", size="18pt")  
gui.widget_2.setLabel("left", "Valor Medido de Nivel", color="b", size="12pt")  
gui.widget_2.setLabel("bottom", "Tiempo (s)", color="b", size="12pt")  
gui.widget_2.addLegend()
gui.widget_2.showGrid(x=True, y=True, alpha=0.5)  
gui.widget_2.setYRange(0, 50, padding=0.1)  
xdata_2 = []
ydata_2 = []
data_line_pres = gui.widget_2.plot(xdata_2, ydata_2, pen=pg.mkPen(color="b", width=3, style=pg.QtCore.Qt.SolidLine), name="nivel")  


# Configuración del temporizador
timer = QtCore.QTimer()
timer.setInterval(1000)

def update():
    global xdata, ydata, xdata_2, ydata_2
    new_temp = random.randint(0, 100)
    new_niv = random.randint(0, 50)
    tiempo_actual = time.time() - start_time

    # Actualizar datos para el gráfico de temperatura
    xdata.append(tiempo_actual)
    ydata.append(new_temp)
    
    # Actualizar datos para el gráfico de nievl
    xdata_2.append(tiempo_actual)
    ydata_2.append(new_niv)

    # Limitar el número de puntos en el gráfico (por ejemplo, 10 puntos visibles)
    if len(xdata) > 10:
        xdata = xdata[1:]
        ydata = ydata[1:]
    if len(xdata_2) > 10:
        xdata_2 = xdata_2[1:]
        ydata_2 = ydata_2[1:]

    # Activar o desactivar label_4 según la temperatura
    if new_temp < 60:
        gui.label_4.setVisible(True)
    else:
        gui.label_4.setVisible(False)

    # Activar o desactivar label_3 según el nivel
    if new_niv < 35:
        gui.label_3.setVisible(True)
    else:
        gui.label_3.setVisible(False)

    # Actualizar los gráficos
    data_line_temp.setData(xdata, ydata)
    data_line_pres.setData(xdata_2, ydata_2)

def Stop():
    timer.stop()

def Reset():
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
gui.btnStop.clicked.connect(Stop)
gui.btnReset.clicked.connect(Reset)

# Iniciar el temporizador y la actualización de datos
update()
timer.timeout.connect(update)
timer.start()

# Mostrar la GUI
gui.show()
app.exec_()