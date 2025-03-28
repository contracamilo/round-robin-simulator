"""
Módulo para exportar los resultados de la simulación a Excel.
"""

import pandas as pd
from typing import List, Dict
from datetime import datetime
from ..core.process import Proceso
from ..config.settings import EXCEL_HEADERS, PROCESS_STATES

class ExportadorExcel:
    """Clase para exportar los resultados de la simulación a Excel."""
    
    @staticmethod
    def exportar_informe(procesos: List[Proceso], quantum: int, 
                        metricas: Dict, historial_estados: Dict) -> str:
        """
        Exporta los resultados de la simulación a un archivo Excel.
        
        Args:
            procesos: Lista de procesos simulados
            quantum: Quantum utilizado en la simulación
            metricas: Diccionario con las métricas finales
            historial_estados: Diccionario con el historial de estados por tiempo
            
        Returns:
            Ruta del archivo Excel generado
        """
        # Crear el nombre del archivo con timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"informe_simulacion_{timestamp}.xlsx"
        
        # Crear un escritor de Excel
        with pd.ExcelWriter(filename, engine='xlsxwriter') as writer:
            # Hoja 1: Información de procesos
            df_procesos = pd.DataFrame([{
                "Proceso": f"P{p.id}",
                "T. Ejecución": p.tiempo_ejecucion,
                "T. Llegada": p.tiempo_llegada,
                "Prioridad": p.prioridad or "-",
                "T. Comienzo": p.tiempo_comienzo,
                "T. Finalización": p.tiempo_finalizacion,
                "T. Retorno": p.tiempo_retorno,
                "T. Espera": p.tiempo_espera
            } for p in procesos])
            
            df_procesos = df_procesos.reindex(columns=EXCEL_HEADERS)
            df_procesos.to_excel(writer, sheet_name='Procesos', index=False)
            
            # Hoja 2: Diagrama de estados
            max_tiempo = max(historial_estados.keys())
            df_estados = pd.DataFrame(index=range(max_tiempo + 1))
            
            for proceso in procesos:
                estados = []
                for t in range(max_tiempo + 1):
                    estado = historial_estados.get(t, {}).get(f"P{proceso.id}", "")
                    estados.append(estado)
                df_estados[f"P{proceso.id}"] = estados
            
            df_estados.to_excel(writer, sheet_name='Diagrama de Estados')
            
            # Hoja 3: Métricas y configuración
            df_metricas = pd.DataFrame([{
                "Métrica": "Quantum",
                "Valor": quantum
            }, {
                "Métrica": "Utilización CPU",
                "Valor": f"{metricas['utilizacion_cpu']:.1f}%"
            }, {
                "Métrica": "Tiempo Espera Promedio",
                "Valor": f"{metricas['tiempo_espera_promedio']:.1f}"
            }, {
                "Métrica": "Tiempo Retorno Promedio",
                "Valor": f"{metricas['tiempo_retorno_promedio']:.1f}"
            }])
            
            df_metricas.to_excel(writer, sheet_name='Métricas', index=False)
            
            # Dar formato a las hojas
            workbook = writer.book
            
            # Formato para encabezados
            header_format = workbook.add_format({
                'bold': True,
                'bg_color': '#D9D9D9',
                'border': 1
            })
            
            # Formato para celdas de datos
            cell_format = workbook.add_format({
                'border': 1
            })
            
            # Aplicar formatos a cada hoja
            for sheet_name in writer.sheets:
                worksheet = writer.sheets[sheet_name]
                for col_num, value in enumerate(df_procesos.columns.values):
                    worksheet.write(0, col_num, value, header_format)
                
                # Ajustar ancho de columnas
                worksheet.set_column(0, len(df_procesos.columns) - 1, 15)
        
        return filename 