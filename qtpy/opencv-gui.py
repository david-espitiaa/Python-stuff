import cv2
import numpy as np
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QTimer, QThread, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap

app = QtWidgets.QApplication([])
gui = uic.loadUi("cam-filters.ui")
cap = cv2.VideoCapture(0)
proceso = 'normal'

def display_image(img, label):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    h, w, ch = img.shape
    bytes_per_lane = ch * w
    qimg = QImage(img.data, w, h, bytes_per_lane, QImage.Format_RGB888)
    pixmap = QPixmap.fromImage(qimg)
    label.setPixmap(pixmap)
    label.setScaledContents(True)

def detect_edges(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

def apply_filter(frame):
    return cv2.GaussianBlur(frame, (15,15), 0)

# Filtros de color y escala de grises
def red_channel(frame):
    red = frame.copy()
    red = red[:, :, 0]
    return red

def green_channel(frame):
    green = frame.copy()
    green = green[:, :, 1] 
    return green

def blue_channel(frame):
    blue = frame.copy()
    blue = blue[:, :, 2] 
    return blue

def grayscale(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

def binary(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, binary_img = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    return cv2.cvtColor(binary_img, cv2.COLOR_GRAY2BGR)

# Modos de filtro
def set_edge_detection_mode():
    global proceso
    proceso = 'bordes'

def set_filter_mode():
    global proceso
    proceso = 'filtro'

def set_normal_mode():
    global proceso
    proceso = 'normal'

def set_red_channel_mode():
    global proceso
    proceso = 'rojo'

def set_green_channel_mode():
    global proceso
    proceso = 'verde'

def set_blue_channel_mode():
    global proceso
    proceso = 'azul'

def set_grayscale_mode():
    global proceso
    proceso = 'grises'

def set_binary_mode():
    global proceso
    proceso = 'binario'

def stop_video():
    worker.stop()
    cap.release()
    gui.destroy()

class videoThread(QThread):
    changePixmapOriginal = pyqtSignal(np.ndarray)
    changePixmapProcesada = pyqtSignal(np.ndarray)

    def run(self):
        global proceso
        while True:
            ret, frame = cap.read()
            self.changePixmapOriginal.emit(frame)
            if ret:
                if proceso == 'bordes':
                    processed_frame = detect_edges(frame)
                elif proceso == 'filtro':
                    processed_frame = apply_filter(frame)
                elif proceso == 'rojo':
                    processed_frame = red_channel(frame)
                elif proceso == 'verde':
                    processed_frame = green_channel(frame)
                elif proceso == 'azul':
                    processed_frame = blue_channel(frame)
                elif proceso == 'grises':
                    processed_frame = grayscale(frame)
                elif proceso == 'binario':
                    processed_frame = binary(frame)
                else:
                    processed_frame = frame

                self.changePixmapProcesada.emit(processed_frame)

    def stop(self):
        self.terminate()

worker = videoThread()

worker.changePixmapOriginal.connect(lambda frame: display_image(frame, gui.label))
worker.changePixmapProcesada.connect(lambda frame: display_image(frame, gui.label2))

# Conectar botones a las funciones
gui.btnNormal.clicked.connect(set_normal_mode)
gui.btnGauss.clicked.connect(set_filter_mode)
gui.btnBordes.clicked.connect(set_edge_detection_mode)
gui.btnRed.clicked.connect(set_red_channel_mode)
gui.btnGreen.clicked.connect(set_green_channel_mode)
gui.btnBlue.clicked.connect(set_blue_channel_mode)
gui.btnGris.clicked.connect(set_grayscale_mode)
gui.btnBinarizar.clicked.connect(set_binary_mode)

gui.btnStop.clicked.connect(stop_video)

worker.start()
gui.show()
app.exec()
