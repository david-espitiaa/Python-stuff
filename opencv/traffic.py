# Importar bibliotecas necesarias
import cv2
from ultralytics import YOLO
import numpy as np

# Sección 1: Configuración del modelo YOLO
# Cargar el modelo YOLOv8 preentrenado para detección de vehículos
model = YOLO("yolov8n.pt")

# Sección 2: Parámetros de configuración para el monitoreo de tráfico
TRAFFIC_THRESHOLD = 10     # Mínimo número de vehículos para considerar tráfico alto
CONGESTION_FRAMES = 5      # Cuadros consecutivos necesarios para confirmar congestión
STILL_THRESHOLD = 5        # Distancia mínima para considerar un vehículo "detenido"

# Sección 3: Inicialización de captura de video
# Cargar el video desde archivo o dispositivo de captura
cap = cv2.VideoCapture("Cars Stuck In Traffic.mp4")

# Variables para rastrear el tráfico en el tiempo
previous_positions = []     # Guarda posiciones anteriores de vehículos
still_frame_count = 0       # Contador de cuadros con vehículos "detenidos"

# Sección 4: Procesamiento de cada cuadro de video en tiempo real
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:  # Finaliza si no se obtienen más cuadros
        break

    # Sección 4.1: Detección de vehículos usando el modelo YOLO
    # Realizar la predicción sobre el cuadro actual
    results = model(frame)
    
    # Variables para conteo y posiciones actuales de vehículos
    vehicle_count = 0
    current_positions = []

    # Sección 4.2: Análisis de resultados y extracción de datos de vehículos
    for result in results:
        for box in result.boxes:
            # Filtrar solo clases de vehículos (ID COCO: coche, autobús, camión, motocicleta)
            if box.cls in [2, 5, 7, 3]:
                vehicle_count += 1
                # Extraer y calcular el centro del cuadro delimitador (bounding box)
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                current_positions.append(((x1 + x2) // 2, (y1 + y2) // 2))
                
                # Mostrar cuadro y etiqueta del vehículo en la imagen
                label = model.names[int(box.cls)]
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Sección 4.3: Detección de congestión por inmovilidad de vehículos
    if previous_positions:
        still_count = 0  # Contador de vehículos sin movimiento en el cuadro actual
        for i in range(min(len(current_positions), len(previous_positions))):
            # Verificar si la distancia entre posiciones consecutivas es menor al umbral de inmovilidad
            if np.linalg.norm(np.array(current_positions[i]) - np.array(previous_positions[i])) < STILL_THRESHOLD:
                still_count += 1

        # Actualizar el contador de cuadros inmóviles si la mayoría de los vehículos están detenidos
        if still_count >= vehicle_count * 0.5:
            still_frame_count += 1
        else:
            still_frame_count = 0  # Reiniciar contador si hay movimiento

    # Sección 4.4: Evaluación del estado del tráfico
    # Determinar si hay mucho o poco tráfico según el conteo de vehículos
    if vehicle_count > TRAFFIC_THRESHOLD:
        traffic_status = "Mucho trafico"
    else:
        traffic_status = "Poco trafico"

    # Verificar si la congestión es detectada por cuadros consecutivos sin movimiento
    if still_frame_count >= CONGESTION_FRAMES:
        traffic_status = "Congestion detectada"
        color = (0, 0, 255)  # Rojo para congestión
    else:
        color = (0, 255, 0) if traffic_status == "Poco trafico" else (0, 165, 255)  # Verde o naranja

    # Sección 4.5: Visualización de resultados en tiempo real
    cv2.putText(frame, f"Vehiculos detectados: {vehicle_count}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
    cv2.putText(frame, traffic_status, (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
    cv2.imshow("Detección de Trafico", frame)

    # Actualizar posiciones anteriores de los vehículos
    previous_positions = current_positions

    # Salir del bucle si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Sección 5: Liberación de recursos
cap.release()
cv2.destroyAllWindows()