"""
Widget del diagrama de Gantt.
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import QObject
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from ...config.settings import PROCESS_COLORS
from ...core.scheduler import ObservadorSimulacion

class DiagramaGantt(QWidget, ObservadorSimulacion):
    """
    Widget que muestra el diagrama de Gantt de la simulación.
    Implementa el patrón Observer para actualizar la vista.
    """
    
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        ObservadorSimulacion.__init__(self)
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la interfaz del diagrama."""
        # Crear layout
        layout = QVBoxLayout(self)
        
        # Crear figura y canvas
        self.figure, self.ax = plt.subplots(figsize=(10, 2))
        self.canvas = FigureCanvas(self.figure)
        
        # Agregar canvas al layout
        layout.addWidget(self.canvas)
    
    def obtener_color_proceso(self, id_proceso: int) -> str:
        """
        Obtiene el color correspondiente a un proceso.
        
        Args:
            id_proceso: ID del proceso
            
        Returns:
            Color en formato hexadecimal
        """
        return PROCESS_COLORS[(id_proceso - 1) % len(PROCESS_COLORS)]
    
    def actualizar(self, datos: dict) -> None:
        """
        Actualiza el diagrama de Gantt con los datos de la simulación.
        
        Args:
            datos: Diccionario con los datos actualizados
        """
        self.ax.clear()
        
        # Obtener datos
        proceso_actual = datos.get('proceso_actual')
        procesos_finalizados = datos.get('procesos_finalizados', [])
        tiempo_actual = datos.get('tiempo_actual', 0)
        
        # Dibujar proceso actual
        if proceso_actual:
            color = self.obtener_color_proceso(proceso_actual.id)
            self.ax.barh(0, 1, left=tiempo_actual,
                        color=color, alpha=0.8)
            self.ax.text(tiempo_actual + 0.5, 0,
                        f"P{proceso_actual.id}",
                        va='center', ha='center')
        
        # Dibujar procesos finalizados
        for proceso in procesos_finalizados:
            color = self.obtener_color_proceso(proceso.id)
            self.ax.barh(0, proceso.tiempo_rafaga,
                        left=proceso.tiempo_finalizacion - proceso.tiempo_rafaga,
                        color=color, alpha=0.8)
            self.ax.text(proceso.tiempo_finalizacion - proceso.tiempo_rafaga + 
                        proceso.tiempo_rafaga/2, 0,
                        f"P{proceso.id}", va='center', ha='center')
        
        # Configurar ejes
        self.ax.set_xlim(0, max(tiempo_actual + 1, 40))  # Mínimo 40 unidades de tiempo
        self.ax.set_ylim(-0.5, 0.5)
        self.ax.set_yticks([])
        self.ax.set_xlabel("Tiempo")
        self.ax.set_title("Diagrama de Gantt")
        self.ax.grid(True, axis='x', linestyle='--', alpha=0.3)
        
        # Actualizar canvas
        self.canvas.draw() 