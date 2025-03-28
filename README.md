# Simulador de Planificación Round Robin

Este proyecto implementa un simulador visual del algoritmo de planificación Round Robin para sistemas operativos, con una interfaz gráfica interactiva desarrollada en PyQt6.

## Características

- **Simulación en Tiempo Real**
  - Visualización del estado de los procesos
  - Control de velocidad de simulación (1 segundo por tick)
  - Opciones de Pausar/Reanudar
  - Quantum configurable (1-10 unidades de tiempo)
  - Número variable de procesos (1-10)

- **Visualización Avanzada**
  - Diagrama de Gantt interactivo con scroll
  - Tabla detallada de procesos
  - Métricas en tiempo real
  - Estados de procesos codificados por colores:
    - Verde: Proceso en ejecución
    - Amarillo: Proceso listo
    - Rojo: Proceso finalizado

- **Métricas del Sistema**
  - Tiempo total de simulación
  - Porcentaje de utilización de CPU
  - Tiempo promedio de espera
  - Tiempo promedio de retorno
  - Historial completo de estados

- **Exportación de Reportes**
  - Generación de reportes en Excel
  - Incluye todas las métricas y estadísticas
  - Formato profesional con estilos
  - Nombrado automático con fecha y hora

## Requisitos

- Python 3.8 o superior
- PyQt6 6.6.1
- openpyxl 3.1.2

## Instalación

1. Clonar el repositorio:
```bash
git clone git@github.com:contracamilo/round-robin-simulator.git
cd round-robin-simulator
```

2. Crear y activar entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Linux/Mac
venv\Scripts\activate     # En Windows
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Uso

1. Ejecutar el simulador:
```bash
python src/main.py
```

2. Configurar la simulación:
   - Ajustar el quantum (1-10)
   - Establecer número de procesos (1-10)
   - Hacer clic en "Iniciar"

3. Durante la simulación:
   - Usar "Pausar/Reanudar" para controlar la ejecución
   - Observar el diagrama de Gantt y la tabla de procesos
   - Monitorear las métricas en tiempo real

4. Al finalizar:
   - Exportar reporte en Excel con el botón "Exportar Reporte"
   - Revisar las estadísticas finales

## Estructura del Proyecto

```
simulador-round-robin/
├── src/
│   ├── core/
│   │   ├── process.py      # Implementación de procesos
│   │   └── scheduler.py    # Planificador Round Robin
│   ├── gui/
│   │   ├── main_window.py  # Ventana principal
│   │   └── gantt_widget.py # Widget del diagrama de Gantt
│   └── main.py            # Punto de entrada
├── requirements.txt       # Dependencias
└── README.md             # Este archivo
```

## Detalles de Implementación

### Procesos
- Identificador único
- Tiempo de llegada aleatorio
- Tiempo de ejecución configurable
- Estados: NUEVO, LISTO, EJECUTANDO, FINALIZADO
- Métricas individuales:
  - Tiempo de espera
  - Tiempo de retorno
  - Tiempo de respuesta

### Planificador
- Implementación del algoritmo Round Robin
- Quantum configurable
- Cola de procesos listos
- Manejo de cambios de contexto
- Cálculo de métricas en tiempo real

### Interfaz Gráfica
- Diseño moderno y responsive
- Diagrama de Gantt con scroll automático
- Tabla de procesos actualizada en tiempo real
- Panel de métricas con estadísticas
- Controles intuitivos

### Reportes
- Formato Excel profesional
- Secciones:
  - Parámetros de simulación
  - Métricas generales
  - Detalle de procesos
  - Estadísticas finales
- Estilos y formato automático

## Patrones de Diseño

- **Observer**: Para actualización en tiempo real de la interfaz
- **Strategy**: En la implementación del planificador
- **Factory**: Para la creación de procesos
- **MVC**: Separación de la lógica y la interfaz

## Contribuir

1. Fork el proyecto
2. Crear rama para nueva característica (`git checkout -b feature/nueva-caracteristica`)
3. Commit cambios (`git commit -am 'Agregar nueva característica'`)
4. Push a la rama (`git push origin feature/nueva-caracteristica`)
5. Crear Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles. 