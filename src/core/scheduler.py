# Módulo que implementa el planificador de procesos. (Strategy & Observer)

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from collections import deque
from PyQt6.QtCore import QObject, QMetaObject
from .process import Proceso, EstadoProceso, FabricaProcesos

class ABCQObjectMeta(type(QObject), type(ABC)):
    """Metaclase que combina QObject y ABC."""
    pass

class ObservadorSimulacion(QObject, ABC, metaclass=ABCQObjectMeta):
    """Interfaz para los observadores de la simulación."""
    
    @abstractmethod
    def actualizar(self, datos: Dict[str, Any]) -> None:
        """
        Actualiza al observador con nuevos datos de la simulación.
        
        datos: Diccionario con los datos actualizados
        """
        pass

class PlanificadorBase(ABC):
    """Clase base abstracta para planificadores de procesos."""
    
    def __init__(self):
        self.procesos: List[Proceso] = []
        self.proceso_actual: Optional[Proceso] = None
        self.tiempo_actual = 0
        self.tiempo_cpu_ocupada = 0
        self.procesos_finalizados: List[Proceso] = []
        self.observadores: List[ObservadorSimulacion] = []
        self.historial_estados: Dict[int, Dict[str, str]] = {}
    
    def agregar_proceso(self, proceso: Proceso) -> None:
        """Agrega un proceso al planificador."""
        self.procesos.append(proceso)
    
    def agregar_observador(self, observador: ObservadorSimulacion) -> None:
        """Agrega un observador al planificador."""
        self.observadores.append(observador)
    
    def registrar_estado_proceso(self, proceso: Proceso) -> None:
        """
        Registra el estado de un proceso en el historial.
        
        Args:
            proceso: Proceso cuyo estado se va a registrar
        """
        if self.tiempo_actual not in self.historial_estados:
            self.historial_estados[self.tiempo_actual] = {}
        
        estado = ''
        if proceso.estado == EstadoProceso.EJECUTANDO:
            estado = 'E'
        elif proceso.estado == EstadoProceso.LISTO:
            estado = 'L'
        elif proceso.estado == EstadoProceso.FINALIZADO:
            estado = 'F'
            
        self.historial_estados[self.tiempo_actual][f"P{proceso.id}"] = estado
    
    def notificar_observadores(self) -> None:
        """Notifica a todos los observadores con el estado actual."""
        datos = {
            'procesos': self.procesos,
            'proceso_actual': self.proceso_actual,
            'tiempo_actual': self.tiempo_actual,
            'tiempo_cpu_ocupada': self.tiempo_cpu_ocupada,
            'procesos_finalizados': self.procesos_finalizados,
            'metricas': self.obtener_metricas(),
            'historial_estados': self.historial_estados
        }
        for observador in self.observadores:
            observador.actualizar(datos)
    
    @abstractmethod
    def tick(self) -> bool:
        """
        Ejecuta un tick de la simulación.
        
        Es True si la simulación debe continuar, False si ha terminado
        """
        pass
    
    def obtener_metricas(self) -> Dict[str, float]:
        """
        Calcula y retorna las métricas de la simulación.
        
        Returns:
            Diccionario con las métricas calculadas
        """
        if not self.procesos_finalizados:
            return {}
            
        tiempo_espera_total = sum(p.tiempo_espera for p in self.procesos_finalizados)
        tiempo_retorno_total = sum(p.tiempo_retorno for p in self.procesos_finalizados)
        tiempo_espera_promedio = tiempo_espera_total / len(self.procesos_finalizados)
        tiempo_retorno_promedio = tiempo_retorno_total / len(self.procesos_finalizados)
        utilizacion_cpu = (self.tiempo_cpu_ocupada / self.tiempo_actual * 100 
                          if self.tiempo_actual > 0 else 0)
        
        return {
            "tiempo_total": self.tiempo_actual,
            "utilizacion_cpu": utilizacion_cpu,
            "tiempo_espera_promedio": tiempo_espera_promedio,
            "tiempo_retorno_promedio": tiempo_retorno_promedio,
            "total_procesos": len(self.procesos),
            "procesos_finalizados": len(self.procesos_finalizados)
        }

class PlanificadorRoundRobin(PlanificadorBase):
    """
    Implementación del algoritmo Round Robin.
    Implementa el patrón Strategy.
    """
    
    def __init__(self, quantum: int):
        super().__init__()
        self.quantum = quantum
        self.cola_listos: deque[Proceso] = deque()
    
    def tick(self) -> bool:
        """
        Ejecuta un tick de la simulación Round Robin.
        
        Es True si la simulación debe continuar, False si ha terminado
        """
        # Agregar nuevos procesos que han llegado
        for proceso in self.procesos:
            if (proceso.estado == EstadoProceso.NUEVO and 
                proceso.tiempo_llegada <= self.tiempo_actual):
                proceso.estado = EstadoProceso.LISTO
                self.cola_listos.append(proceso)
                if proceso.tiempo_respuesta is None:
                    proceso.tiempo_respuesta = self.tiempo_actual - proceso.tiempo_llegada
            
            # Actualizar tiempo de espera para procesos en estado LISTO
            if proceso.estado == EstadoProceso.LISTO:
                proceso.tiempo_espera += 1
                
            self.registrar_estado_proceso(proceso)
        
        # Manejar proceso actual
        if self.proceso_actual is None:
            if not self.cola_listos:
                self.tiempo_actual += 1
                self.notificar_observadores()
                return len(self.procesos_finalizados) < len(self.procesos)
            
            self.proceso_actual = self.cola_listos.popleft()
            self.proceso_actual.estado = EstadoProceso.EJECUTANDO
            if self.proceso_actual.tiempo_comienzo is None:
                self.proceso_actual.tiempo_comienzo = self.tiempo_actual
        
        # Ejecutar proceso actual
        self.proceso_actual.tiempo_restante -= 1
        self.tiempo_cpu_ocupada += 1
        self.registrar_estado_proceso(self.proceso_actual)
        
        # Verificar si el proceso terminó o expiró el quantum
        if self.proceso_actual.tiempo_restante == 0:
            self.proceso_actual.estado = EstadoProceso.FINALIZADO
            self.proceso_actual.tiempo_finalizacion = self.tiempo_actual + 1
            self.procesos_finalizados.append(self.proceso_actual)
            self.proceso_actual = None
        elif (self.tiempo_actual + 1) % self.quantum == 0:
            self.proceso_actual.estado = EstadoProceso.LISTO
            self.cola_listos.append(self.proceso_actual)
            self.proceso_actual = None
        
        self.tiempo_actual += 1
        self.notificar_observadores()
        return len(self.procesos_finalizados) < len(self.procesos) 