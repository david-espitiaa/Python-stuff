import numpy as np  # Librería para manejar arrays y operaciones matemáticas
import matplotlib.pyplot as plt  # Librería para graficar

# Función para calcular la matriz homogénea de transformación
def matriz_homogenea(theta, d, a, alpha):
    
    """
    Calcula la matriz homogénea de transformación dada por los parámetros DH (Denavit-Hartenberg).

    Parámetros:
    - theta: Ángulo de rotación en torno al eje Z previo.
    - d: Desplazamiento a lo largo del eje Z previo.
    - a: Longitud del eslabón a lo largo del eje X previo.
    - alpha: Ángulo de rotación en torno al eje X previo.

    Retorna:
    - Matriz homogénea 4x4 que combina rotaciones y traslaciones.
    """

    theta = np.deg2rad(theta)  # Convertir ángulo theta de grados a radianes
    alpha = np.deg2rad(alpha)  # Convertir ángulo alpha de grados a radianes
    return np.array([
        [np.cos(theta), -np.sin(theta)*np.cos(alpha), np.sin(theta)*np.sin(alpha), a*np.cos(theta)],
        [np.sin(theta), np.cos(theta)*np.cos(alpha), -np.cos(theta)*np.sin(alpha), a*np.sin(theta)],
        [0, np.sin(alpha), np.cos(alpha), d],
        [0, 0, 0, 1]  # Se añade la fila para mantener la homogeneidad
    ])

# Definición de parámetros para el primer eslabón
# Estos corresponden a los parámetros DH del eslabón 1
theta1, d1, a1, alpha1 = 45, 0, 2, 0  # Ángulo, desplazamiento, longitud del eslabón y ángulo de inclinación

# Definición de parámetros para el segundo eslabón
theta2, d2, a2, alpha2 = 30, 0, 1.5, 0  # Mismo tipo de parámetros para el eslabón 2

# Cálculo de la matriz homogénea para el primer eslabón
T1 = matriz_homogenea(theta1, d1, a1, alpha1)  # Matriz de transformación del eslabón 1

# Cálculo de la matriz homogénea para el segundo eslabón, acumulando la transformación
T2 = T1 @ matriz_homogenea(theta2, d2, a2, alpha2)  # Matriz acumulada de transformación

# Determinación de las posiciones de los puntos clave
origen = np.array([0, 0, 0])  # Punto de origen del sistema de coordenadas
eslabon1 = T1[:3, 3]  # Extraer la posición del extremo del primer eslabón
eslabon2 = T2[:3, 3]  # Extraer la posición del extremo del segundo eslabón

# Graficar las posiciones de los eslabones
fig = plt.figure()  # Crear una nueva figura para la gráfica
ax = fig.add_subplot(111)  # Agregar un subplot en 2D

# Trazar el eslabón 1 desde el origen hasta su extremo
ax.plot([origen[0], eslabon1[0]], [origen[1], eslabon1[1]], label="Eslabón 1", marker='o')

# Trazar el eslabón 2 desde el extremo del eslabón 1 hasta su extremo
ax.plot([eslabon1[0], eslabon2[0]], [eslabon1[1], eslabon2[1]], label="Eslabón 2", marker='o')

# Configuración de etiquetas y título del gráfico
ax.set_xlabel('X')  # Etiqueta del eje X
ax.set_ylabel('Y')  # Etiqueta del eje Y
ax.set_title('Simulación de dos eslabones')  # Título de la gráfica

# Agregar una leyenda para identificar los eslabones
ax.legend()

# Opciones de visualización
plt.grid()  # Activar la cuadrícula
plt.axis('equal')  # Escalar los ejes de forma uniforme
plt.show()  # Mostrar el gráfico
