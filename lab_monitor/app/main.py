import streamlit as st
import plotly.graph_objects as go
from datetime import datetime
import time

from sensors import SensorCVD, SensorConfig
from database import DataBase

st.set_page_config(
    page_title="Monitor Ambiental de Laboratorio",
    layout='wide',
    initial_sidebar_state="expanded"
)

# CSS para estilizar la interfaz
st.markdown("""
    <style>
        .alerta { color: #FF3333; font-size: 1.1em; font-weight: bold; }
        .advertencia { color: #FFA500; font-size: 1.1em; font-weight: bold; }
        .estado-normal { color: #4BB543; font-weight: bold; }
        .estado-bajo { color: #FFA500; font-weight: bold; }
        .estado-alto { color: #FF3333; font-weight: bold; }
        .metricas { padding: 10px; border-radius: 8px; background-color: #0E7EED; }
    </style>
""", unsafe_allow_html=True)

# Configuración de sensores
SENSORES_CONFIG = {
    'particulas': SensorConfig(
        nombre="Niveles de Partículas",
        unidad="µg/m³",
        rango=(0, 500),
        precision=1,
        color="#FFAA00",
        limites_alarma={'bajo': 50, 'alto': 300}
    ),
    'temperatura': SensorConfig(
        nombre="Temperatura Ambiente",
        unidad="°C",
        rango=(0, 50),
        precision=1,
        color="#FF4B4B",
        limites_alarma={'bajo': 15, 'alto': 30}
    ),
    'humedad': SensorConfig(
        nombre="Humedad Relativa",
        unidad="%",
        rango=(0, 100),
        precision=1,
        color="#4BFF4B",
        limites_alarma={'bajo': 20, 'alto': 70}
    ),
    'COV': SensorConfig(
        nombre="Niveles de COV",
        unidad="ppm",
        rango=(0, 800),
        precision=1,
        color="#FF4BAA",
        limites_alarma={'bajo': 50, 'alto': 300}
    )
}

class MonitorAmbiental:
    def __init__(self):
        self.db = DataBase('data/sensor_data.db')
        self.sensores = {
            nombre: SensorCVD(config)
            for nombre, config in SENSORES_CONFIG.items()
        }
        self.contenedores_graficas = {}

    def ejecutar(self):
        st.title("🌡️ Monitor Ambiental de Laboratorio")
        st.markdown("### Monitoreo de parámetros críticos para un ambiente seguro")

        with st.sidebar:
            intervalo = st.slider("Intervalo de actualización (s)", 1, 10, 2)
            modo_demo = st.checkbox("Modo Demo", True)
            st.markdown("**Configuración del Sistema**")
            st.divider()
            st.markdown("""
                Este sistema monitorea parámetros ambientales críticos en el laboratorio de electrónica,
                ayudando a proteger la salud del personal y asegurando un entorno seguro.
            """)

        # Contenedores para los indicadores de estado y alertas
        col1, col2, col3, col4 = st.columns(4)
        contenedores = {
            'particulas': col1.empty(),
            'temperatura': col2.empty(),
            'humedad': col3.empty(),
            'COV': col4.empty()
        }
        
        # Contenedor de alertas y gráficos
        contenedor_alertas = st.empty()
        
        with st.container():
            self.contenedores_graficas['particulas'] = st.empty()
            self.contenedores_graficas['temperatura'] = st.empty()
            self.contenedores_graficas['humedad'] = st.empty()
            self.contenedores_graficas['COV'] = st.empty()

        while modo_demo:
            alertas_actuales = []  # Lista para almacenar las alertas activas en cada ciclo

            for nombre, sensor in self.sensores.items():
                valor = sensor.leer()
                estado = sensor.verificar_alarma(valor)
                
                # Guardar en la base de datos
                self.db.guardar_lectura(nombre, valor, estado)

                config = SENSORES_CONFIG[nombre]
                estado_color = "estado-normal" if estado == 'normal' else (
                    "estado-bajo" if estado == 'bajo' else "estado-alto"
                )

                # Mostrar métrica con estilo
                with contenedores[nombre]:
                    st.markdown(f"""
                        <div class="metricas">
                            <strong>{config.nombre}:</strong>
                            <span class="{estado_color}">{valor} {config.unidad}</span>
                        </div>
                    """, unsafe_allow_html=True)

                # Alertas
                if estado == 'alto':
                    alertas_actuales.append(
                        f"<div class='alerta'>⚠️ {config.nombre} excedió el límite superior "
                        f"({config.limites_alarma['alto']} {config.unidad}). Valor: {valor} {config.unidad}.</div>"
                    )
                elif estado == 'bajo':
                    alertas_actuales.append(
                        f"<div class='advertencia'>⚠️ {config.nombre} está por debajo del límite inferior "
                        f"({config.limites_alarma['bajo']} {config.unidad}). Valor: {valor} {config.unidad}.</div>"
                    )

            # Actualizar contenedor de alertas
            with contenedor_alertas:
                if alertas_actuales:
                    for alerta in alertas_actuales:
                        st.markdown(alerta, unsafe_allow_html=True)
                else:
                    contenedor_alertas.empty()  # Limpiar alertas si no hay activas

            # Actualizar gráficas
            self.actualizar_graficas()
            time.sleep(intervalo)

    def actualizar_graficas(self):
        for nombre, sensor in self.sensores.items():
            config = SENSORES_CONFIG[nombre]
            datos = self.db.obtener_historico(nombre, 100)

            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=datos['timestamp'],
                y=datos['valor'],
                name=config.nombre,
                line=dict(color=config.color)
            ))

            fig.update_layout(
                title=f"{config.nombre} en Tiempo Real",
                xaxis_title="Tiempo",
                yaxis_title=f"{config.unidad}",
                height=300,
                margin=dict(l=10, r=10, t=30, b=10)
            )

            self.contenedores_graficas[nombre].plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    monitor = MonitorAmbiental()
    monitor.ejecutar()
