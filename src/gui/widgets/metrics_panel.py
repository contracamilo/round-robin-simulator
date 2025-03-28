"""
Widget del panel de métricas.
"""

from PyQt6.QtWidgets import QGroupBox, QGridLayout, QLabel
from PyQt6.QtCore import QObject
from ...config.settings import METRICS
from ...core.scheduler import ObservadorSimulacion

class PanelMetricas(QGroupBox, ObservadorSimulacion):
    """
    Panel que muestra las métricas de la simulación.
    Implementa el patrón Observer para actualizar la vista.
    """
    
    def __init__(self, parent=None):
        QGroupBox.__init__(self, "Métricas", parent)
        ObservadorSimulacion.__init__(self)
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la interfaz del panel."""
        layout = QGridLayout()
        
        # Crear etiquetas para cada métrica
        self.etiquetas = {}
        for i, metrica in enumerate(METRICS):
            layout.addWidget(QLabel(f"{metrica}:"), i, 0)
            self.etiquetas[metrica] = QLabel("0")
            layout.addWidget(self.etiquetas[metrica], i, 1)
        
        self.setLayout(layout)
    
    def actualizar(self, datos: dict) -> None:
        """
        Actualiza las métricas con los datos de la simulación.
        
        Args:
            datos: Diccionario con los datos actualizados
        """
        metricas = datos.get('metricas', {})
        if metricas:
            self.etiquetas["Utilización CPU"].setText(f"{metricas['utilizacion_cpu']:.1f}%")
            self.etiquetas["Tiempo Espera Promedio"].setText(f"{metricas['tiempo_espera_promedio']:.1f}")
            self.etiquetas["Tiempo Retorno Promedio"].setText(f"{metricas['tiempo_retorno_promedio']:.1f}") 