import cv2
import numpy as np

# Cargar el video
cap = cv2.VideoCapture(0)  # Reemplaza 'ruta_del_video.mp4' por el archivo de video o cámara

# Definir las coordenadas de los cinco lugares de estacionamiento
# Cada elemento es una lista con las coordenadas de cada lugar [x, y, width, height]
parking_spots = [
    [50, 100, 80, 40],
    [150, 100, 80, 40],
    [250, 100, 80, 40],
    [350, 100, 80, 40],
    [450, 100, 80, 40]
]

# Parámetros de detección de movimiento
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
fgbg = cv2.createBackgroundSubtractorMOG2(detectShadows=True)

while True:
    ret, frame = cap.read()
    if not ret:
        print("no jala viejo")
        break

    # Aplicar sustracción de fondo para detectar movimiento
    fgmask = fgbg.apply(frame)
    thresh = cv2.threshold(fgmask, 200, 255, cv2.THRESH_BINARY)[1]
    dilated = cv2.dilate(thresh, kernel, iterations=2)

    # Verificar cada lugar de estacionamiento
    for i, (x, y, w, h) in enumerate(parking_spots):
        # Extraer el área del lugar de estacionamiento
        spot = dilated[y:y+h, x:x+w]

        # Contar los píxeles blancos en el área para determinar si hay un vehículo
        white_pixels = cv2.countNonZero(spot)
        spot_occupied = white_pixels > (w * h * 0.2)  # Umbral de ocupación (ajustable)

        # Cambiar el color según el estado (rojo si está ocupado, verde si está libre)
        color = (0, 0, 255) if spot_occupied else (0, 255, 0)
        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)

        # Mostrar el estado en el marco
        text = 'Ocupado' if spot_occupied else 'Libre'
        cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

    # Mostrar el frame con los lugares de estacionamiento
    cv2.imshow('Estacionamiento', frame)

    # Salir al presionar la tecla 'q'
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
