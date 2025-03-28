# Configuración de la interfaz gráfica
WINDOW_TITLE = "Simulador de Planificación Round Robin"
WINDOW_MIN_WIDTH = 1200
WINDOW_MIN_HEIGHT = 800

# Configuración de la simulación
DEFAULT_QUANTUM = 2
DEFAULT_PROCESSES = 5
MAX_PROCESSES = 20
MAX_EXECUTION_TIME = 10
MAX_ARRIVAL_TIME = 20

# Intervalos de actualización
SIMULATION_INTERVAL = 1000  # milisegundos

# Colores para el diagrama de Gantt
PROCESS_COLORS = [
    '#FF9999',  # Rojo claro
    '#99FF99',  # Verde claro
    '#9999FF',  # Azul claro
    '#FFFF99',  # Amarillo claro
    '#FF99FF',  # Magenta claro
    '#99FFFF',  # Cian claro
    '#FFB366',  # Naranja claro
    '#B366FF',  # Púrpura claro
    '#66FFB3',  # Verde menta
    '#66B3FF',  # Azul cielo
]

# Estados de la simulación
class SimulationState:
    STOPPED = "Detenida"
    RUNNING = "En ejecución"
    PAUSED = "Pausada"
    FINISHED = "Finalizada"

# Configuración de la tabla de procesos
PROCESS_TABLE_COLUMNS = [
    "ID Proceso",
    "Tiempo Llegada",
    "Tiempo Ejecución",
    "Prioridad",
    "Estado",
    "Tiempo Restante",
    "Tiempo Espera",
    "Tiempo Finalización",
    "Tiempo Retorno"
]

# Configuración de métricas
METRICS = [
    "Utilización CPU",
    "Tiempo Espera Promedio",
    "Tiempo Retorno Promedio"
]

# Configuración del informe Excel
EXCEL_HEADERS = [
    "Proceso",
    "T. Ejecución",
    "T. Llegada",
    "Prioridad",
    "T. Comienzo",
    "T. Finalización",
    "T. Retorno",
    "T. Espera"
]

# Estados de proceso para el informe
PROCESS_STATES = {
    'E': 'Ejecutando',
    'L': 'Listo',
    'F': 'Finalizado'
} 