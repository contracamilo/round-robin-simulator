from enum import Enum
from dataclasses import dataclass
from typing import Optional
import random

class EstadoProceso(Enum):
    NUEVO = 0
    LISTO = 1
    EJECUTANDO = 2
    FINALIZADO = 3

@dataclass
class Proceso:
    """
    Representa un proceso en el sistema.
    
        id: Identificador único del proceso
        tiempo_llegada: Momento en que el proceso llega al sistema
        tiempo_ejecucion: Tiempo total de CPU que necesita el proceso
        prioridad: Nivel de prioridad del proceso (opcional)
        estado: Estado actual del proceso
        tiempo_restante: Tiempo restante de ejecución
        tiempo_espera: Tiempo total en cola
        tiempo_respuesta: Tiempo hasta la primera asignación de CPU
        tiempo_finalizacion: Momento en que el proceso termina
        tiempo_comienzo: Momento en que el proceso comienza su primera ejecución
    """
    id: int
    tiempo_llegada: int
    tiempo_ejecucion: int
    prioridad: Optional[int] = None
    estado: EstadoProceso = EstadoProceso.NUEVO
    tiempo_restante: int = 0
    tiempo_espera: int = 0
    tiempo_respuesta: Optional[int] = None
    tiempo_finalizacion: Optional[int] = None
    tiempo_comienzo: Optional[int] = None
    
    def __post_init__(self):
        """Inicializa el tiempo restante igual al tiempo de ejecución."""
        self.tiempo_restante = self.tiempo_ejecucion
    
    @property
    def tiempo_retorno(self) -> Optional[int]:
        """
        Calcula el tiempo de retorno del proceso.
        Tiempo de retorno = Tiempo de espera + Tiempo de ejecución
        
        Returns:
            Tiempo total desde la llegada hasta la finalización
        """
        if self.tiempo_finalizacion is None:
            return None
        return self.tiempo_finalizacion - self.tiempo_llegada
    
    def __str__(self) -> str:
        """Representación en string del proceso."""
        return f"P{self.id} (LL:{self.tiempo_llegada}, TE:{self.tiempo_ejecucion})"

class FabricaProcesos:
    """Fábrica para crear procesos con diferentes características."""
    
    _next_id = 1
    
    def __init__(self):
        """Inicializa la fábrica de procesos."""
        self.min_llegada = 0
        self.max_llegada = 10
        self.min_duracion = 2
        self.max_duracion = 10
    
    def crear_proceso_aleatorio(self) -> Proceso:
        """
        Crea un proceso con tiempo de llegada y duración aleatorios.
        
        Returns:
            Un nuevo proceso con características aleatorias
        """
        id_proceso = FabricaProcesos._next_id
        FabricaProcesos._next_id += 1
        
        tiempo_llegada = random.randint(self.min_llegada, self.max_llegada)
        tiempo_ejecucion = random.randint(self.min_duracion, self.max_duracion)
        
        return Proceso(
            id=id_proceso,
            tiempo_llegada=tiempo_llegada,
            tiempo_ejecucion=tiempo_ejecucion
        )

    @staticmethod
    def crear_proceso(id: int, tiempo_llegada: int, tiempo_ejecucion: int, 
                     prioridad: Optional[int] = None) -> Proceso:
        """
        Crea un nuevo proceso con los parámetros especificados.
        
        Args:
            id: Identificador del proceso
            tiempo_llegada: Tiempo de llegada al sistema
            tiempo_ejecucion: Tiempo de ejecución requerido
            prioridad: Nivel de prioridad (opcional)
            
        Returns:
            Una nueva instancia de Proceso
        """
        return Proceso(id, tiempo_llegada, tiempo_ejecucion, prioridad)
    
    @staticmethod
    def crear_procesos_aleatorios(num_procesos: int, 
                                 max_ejecucion: int = 10, 
                                 max_llegada: int = 20) -> list[Proceso]:
        """
        Crea un conjunto de procesos con tiempos aleatorios.
        
        Args:
            num_procesos: Número de procesos a crear
            max_ejecucion: Tiempo máximo de ejecución
            max_llegada: Tiempo máximo de llegada
            
        Returns:
            Lista de procesos creados
        """
        procesos = []
        for i in range(num_procesos):
            tiempo_llegada = random.randint(0, max_llegada)
            tiempo_ejecucion = random.randint(1, max_ejecucion)
            proceso = FabricaProcesos.crear_proceso(i + 1, tiempo_llegada, tiempo_ejecucion)
            procesos.append(proceso)
        return procesos 