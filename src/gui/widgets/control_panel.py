"""
Widget del panel de control de la simulación.
"""

from PyQt6.QtWidgets import (QGroupBox, QGridLayout, QLabel, 
                             QSpinBox, QPushButton)
from PyQt6.QtCore import pyqtSignal
from ...config.settings import (DEFAULT_PROCESSES, MAX_PROCESSES,
                              DEFAULT_QUANTUM, SimulationState)

class PanelControl(QGroupBox):
    """
    Panel de control para la simulación.
    Implementa el patrón Observer para notificar cambios.
    """
    
    # Señales
    simulacion_iniciada = pyqtSignal(int, int)  # (num_procesos, quantum)
    simulacion_detenida = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__("Panel de Control", parent)
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la interfaz del panel de control."""
        layout = QGridLayout()
        
        # Número de procesos
        layout.addWidget(QLabel("Número de Procesos:"), 0, 0)
        self.num_procesos = QSpinBox()
        self.num_procesos.setRange(1, MAX_PROCESSES)
        self.num_procesos.setValue(DEFAULT_PROCESSES)
        layout.addWidget(self.num_procesos, 0, 1)
        
        # Quantum
        layout.addWidget(QLabel("Quantum:"), 0, 2)
        self.quantum = QSpinBox()
        self.quantum.setRange(1, 10)
        self.quantum.setValue(DEFAULT_QUANTUM)
        layout.addWidget(self.quantum, 0, 3)
        
        # Botones de control
        self.boton_iniciar = QPushButton("Iniciar Simulación")
        self.boton_iniciar.clicked.connect(self.iniciar_simulacion)
        layout.addWidget(self.boton_iniciar, 0, 4)
        
        self.boton_detener = QPushButton("Detener Simulación")
        self.boton_detener.clicked.connect(self.detener_simulacion)
        self.boton_detener.setEnabled(False)
        layout.addWidget(self.boton_detener, 0, 5)
        
        self.setLayout(layout)
    
    def iniciar_simulacion(self):
        """Inicia la simulación con los parámetros actuales."""
        self.boton_iniciar.setEnabled(False)
        self.boton_detener.setEnabled(True)
        self.simulacion_iniciada.emit(
            self.num_procesos.value(),
            self.quantum.value()
        )
    
    def detener_simulacion(self):
        """Detiene la simulación actual."""
        self.boton_iniciar.setEnabled(True)
        self.boton_detener.setEnabled(False)
        self.simulacion_detenida.emit()
    
    def actualizar_estado(self, estado: str):
        """
        Actualiza el estado de los botones según el estado de la simulación.
        
        Args:
            estado: Estado actual de la simulación
        """
        if estado == SimulationState.FINISHED:
            self.boton_iniciar.setEnabled(True)
            self.boton_detener.setEnabled(False)
        elif estado == SimulationState.RUNNING:
            self.boton_iniciar.setEnabled(False)
            self.boton_detener.setEnabled(True)
        elif estado == SimulationState.STOPPED:
            self.boton_iniciar.setEnabled(True)
            self.boton_detener.setEnabled(False) 