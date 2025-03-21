import matplotlib.pyplot as plt
import numpy as np

"""
Examen 1° Parcial - Rootica - Ejercico 22q

Este programa calcula la configuración de un mecanismo de dos eslabones utilizando cinemática inversa 
y lo visualiza en un gráfico.

Procedimiento:

1. **Definición de parámetros**:
   - Se establecen las longitudes de los eslabones (L1 y L2).
   - Se definen las coordenadas del punto objetivo P(x, y).

2. **Cálculo de los ángulos mediante cinemática inversa**:
   - Se usa la ecuación de la ley de los cosenos para calcular el ángulo θ₂:
     cos(θ₂) = (Px² + Py² - L1² - L2²) / (2 * L1 * L2)
   - Se obtiene el ángulo θ₂ aplicando la función arccos.

   - Para calcular el ángulo θ₁, se usa la función atan2 para evitar ambigüedades:
     θ₁ = atan2(Py, Px) - atan2(L2 * sin(θ₂), L1 + L2 * cos(θ₂))

3. **Conversión de unidades**:
   - Se convierten los ángulos de radianes a grados para facilitar la interpretación.

4. **Cálculo de posiciones de las articulaciones**:
   - Se determinan las coordenadas de los puntos intermedios del mecanismo.

5. **Visualización gráfica**:
   - Se grafica el sistema de eslabones junto con el punto objetivo.
   - Se establecen límites de los ejes y se ajusta la escala para una representación clara.

"""


# Longitudes de los eslabones del mecanismo en milímetros
L1 = 240  # Longitud del primer eslabón
L2 = 190  # Longitud del segundo eslabón

# Coordenadas del punto final del mecanismo (punto P)
Px = 249.447  # Coordenada X en mm
Py = 300.579  # Coordenada Y en mm

# Aplicación de cinemática inversa para calcular los ángulos de las articulaciones
cos_theta2 = (Px**2 + Py**2 - L1**2 - L2**2) / (2 * L1 * L2)  # Cálculo del coseno de theta2
theta2 = np.arccos(cos_theta2)  # Obtención del ángulo theta2 en radianes

# Cálculo del ángulo theta1 usando la función atan2 para evitar ambigüedades
theta1 = np.arctan2(Py, Px) - np.arctan2(L2 * np.sin(theta2), L1 + L2 * np.cos(theta2))

# Conversión de los ángulos de radianes a grados
theta1_deg = np.degrees(theta1)
theta2_deg = np.degrees(theta2)

# Imprimir los ángulos calculados
print(f"Ángulo theta1: {theta1_deg:.2f} grados")
print(f"Ángulo theta2: {theta2_deg:.2f} grados")

# Cálculo de las posiciones de los puntos intermedios del mecanismo
x0, y0 = 0, 0  # Punto de origen del mecanismo
x1, y1 = L1 * np.cos(theta1), L1 * np.sin(theta1)  # Posición del primer eslabón
x2, y2 = x1 + L2 * np.cos(theta1 + theta2), y1 + L2 * np.sin(theta1 + theta2)  # Posición del extremo del segundo eslabón

# Graficar la configuración del sistema de eslabones
plt.figure()
plt.plot([x0, x1], [y0, y1], 'r-o', label='Eslabón 1')  # Eslabón 1 en rojo
plt.plot([x1, x2], [y1, y2], 'b-o', label='Eslabón 2')  # Eslabón 2 en azul
plt.plot(Px, Py, 'go', label='Punto P')  # Punto objetivo en verde

# Ajustes visuales de la gráfica
plt.xlim(-L1-L2, L1+L2)  # Límites del eje X
plt.ylim(-L1-L2, L1+L2)  # Límites del eje Y
plt.axhline(0, color='black', linewidth=0.5)  # Línea horizontal en el eje X
plt.axvline(0, color='black', linewidth=0.5)  # Línea vertical en el eje Y
plt.grid()  # Activar la cuadrícula
plt.legend()  # Mostrar leyenda
plt.title('Configuración del sistema de eslabones')  # Título del gráfico
plt.xlabel('X (mm)')  # Etiqueta del eje X
plt.ylabel('Y (mm)')  # Etiqueta del eje Y
plt.gca().set_aspect('equal', adjustable='box')  # Mantener proporciones iguales en los ejes
plt.show()  # Mostrar la gráfica
