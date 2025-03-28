"""
Widget de la tabla de procesos.
"""

from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt6.QtCore import QObject
from ...config.settings import PROCESS_TABLE_COLUMNS
from ...core.scheduler import ObservadorSimulacion

class TablaProcesos(QTableWidget, ObservadorSimulacion):
    """
    Tabla que muestra información detallada de los procesos.
    Implementa el patrón Observer para actualizar la vista.
    """
    
    def __init__(self, parent=None):
        QTableWidget.__init__(self, parent)
        ObservadorSimulacion.__init__(self)
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la interfaz de la tabla."""
        self.setColumnCount(len(PROCESS_TABLE_COLUMNS))
        self.setHorizontalHeaderLabels(PROCESS_TABLE_COLUMNS)
        self.horizontalHeader().setStretchLastSection(True)
    
    def actualizar(self, datos: dict) -> None:
        """
        Actualiza la tabla con los datos de los procesos.
        
        Args:
            datos: Diccionario con los datos actualizados
        """
        procesos = datos.get('procesos', [])
        self.setRowCount(len(procesos))
        
        for i, proceso in enumerate(procesos):
            self.setItem(i, 0, QTableWidgetItem(str(proceso.id)))
            self.setItem(i, 1, QTableWidgetItem(str(proceso.tiempo_llegada)))
            self.setItem(i, 2, QTableWidgetItem(str(proceso.tiempo_rafaga)))
            self.setItem(i, 3, QTableWidgetItem(str(proceso.prioridad or "-")))
            self.setItem(i, 4, QTableWidgetItem(proceso.estado.value))
            self.setItem(i, 5, QTableWidgetItem(str(proceso.tiempo_restante)))
            self.setItem(i, 6, QTableWidgetItem(str(proceso.tiempo_espera)))
            self.setItem(i, 7, QTableWidgetItem(str(proceso.tiempo_finalizacion or "-"))) 