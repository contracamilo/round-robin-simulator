"""
Widget que muestra el diagrama de Gantt de la simulación.
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea
from PyQt6.QtGui import QPainter, QColor, QPen
from PyQt6.QtCore import Qt, QRect, QSize
from typing import Dict, Any
from ..core.scheduler import ObservadorSimulacion

class DiagramaGanttContenido(QWidget):
    """Widget que contiene el diagrama de Gantt."""
    
    ALTURA_PROCESO = 30
    ANCHO_UNIDAD_TIEMPO = 30
    MARGEN = 50
    
    def __init__(self):
        super().__init__()
        self.historial: Dict[int, Dict[str, str]] = {}
        self.tiempo_maximo = 0
        self.num_procesos = 0
        
        # Colores para los diferentes estados
        self.colores = {
            'E': QColor(46, 204, 113),  # Verde para ejecutando
            'L': QColor(241, 196, 15),  # Amarillo para listo
            'F': QColor(231, 76, 60)    # Rojo para finalizado
        }
        
        self.setMinimumSize(400, 200)
    
    def actualizar(self, datos: Dict[str, Any]) -> None:
        """
        Actualiza el diagrama con nuevos datos.
        
        Args:
            datos: Diccionario con los datos actualizados
        """
        self.historial = datos['historial_estados']
        self.tiempo_maximo = datos['tiempo_actual']
        if self.historial:
            self.num_procesos = len(next(iter(self.historial.values())))
        
        # Actualizar tamaño del widget
        width = self.MARGEN * 2 + (self.tiempo_maximo + 1) * self.ANCHO_UNIDAD_TIEMPO
        height = self.MARGEN * 2 + self.num_procesos * self.ALTURA_PROCESO
        self.setMinimumSize(width, height)
        self.resize(width, height)
        self.update()
    
    def paintEvent(self, event):
        """Dibuja el diagrama de Gantt."""
        if not self.historial:
            return
            
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Dibujar ejes
        self._dibujar_ejes(painter)
        
        # Dibujar las barras del diagrama
        self._dibujar_barras(painter)
        
        # Dibujar etiquetas de tiempo
        self._dibujar_etiquetas_tiempo(painter)
        
        # Dibujar etiquetas de procesos
        self._dibujar_etiquetas_procesos(painter)
    
    def _dibujar_ejes(self, painter: QPainter):
        """Dibuja los ejes del diagrama."""
        pen = QPen(Qt.GlobalColor.black, 2)
        painter.setPen(pen)
        
        # Eje Y
        painter.drawLine(
            self.MARGEN, self.MARGEN,
            self.MARGEN, self.height() - self.MARGEN
        )
        
        # Eje X
        painter.drawLine(
            self.MARGEN, self.height() - self.MARGEN,
            self.width() - self.MARGEN, self.height() - self.MARGEN
        )
    
    def _dibujar_barras(self, painter: QPainter):
        """Dibuja las barras del diagrama para cada proceso."""
        for tiempo in range(self.tiempo_maximo + 1):
            if tiempo not in self.historial:
                continue
                
            estados = self.historial[tiempo]
            for i, (proceso_id, estado) in enumerate(estados.items()):
                if estado not in self.colores:
                    continue
                    
                x = self.MARGEN + tiempo * self.ANCHO_UNIDAD_TIEMPO
                y = self.MARGEN + i * self.ALTURA_PROCESO
                
                rect = QRect(
                    x, y,
                    self.ANCHO_UNIDAD_TIEMPO,
                    self.ALTURA_PROCESO
                )
                
                painter.fillRect(rect, self.colores[estado])
                painter.setPen(QPen(Qt.GlobalColor.black, 1))
                painter.drawRect(rect)
    
    def _dibujar_etiquetas_tiempo(self, painter: QPainter):
        """Dibuja las etiquetas de tiempo en el eje X."""
        painter.setPen(QPen(Qt.GlobalColor.black))
        for t in range(self.tiempo_maximo + 1):
            x = self.MARGEN + t * self.ANCHO_UNIDAD_TIEMPO
            y = self.height() - self.MARGEN + 20
            painter.drawText(x, y, str(t))
    
    def _dibujar_etiquetas_procesos(self, painter: QPainter):
        """Dibuja las etiquetas de procesos en el eje Y."""
        painter.setPen(QPen(Qt.GlobalColor.black))
        for i in range(self.num_procesos):
            x = self.MARGEN - 30
            y = self.MARGEN + i * self.ALTURA_PROCESO + self.ALTURA_PROCESO // 2
            painter.drawText(x, y, f"P{i}")

class DiagramaGantt(QScrollArea):
    """Widget con scroll que contiene el diagrama de Gantt."""
    
    def __init__(self):
        super().__init__()
        self.contenido = DiagramaGanttContenido()
        self.setWidget(self.contenido)
        self.setWidgetResizable(True)
        self.setMinimumSize(400, 200)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
    
    def actualizar(self, datos: Dict[str, Any]) -> None:
        """
        Actualiza el diagrama con nuevos datos.
        
        Args:
            datos: Diccionario con los datos actualizados
        """
        self.contenido.actualizar(datos) 