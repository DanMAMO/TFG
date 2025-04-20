import pandas as pd
import os
from base.informe_base import InformeBase
from utils.helpers import extraer_fecha_desde_lineas, formatear_fecha_ddmmYYYY, guardar_csvs

class InformeAventuras(InformeBase):
    def procesar(self):
        with open(self.path_txt, "r", encoding="utf-8") as f:
            lineas = f.readlines()

        resumen = {}
        tabla_inicio = None
        for i, linea in enumerate(lineas):
            linea = linea.strip()
            if linea.startswith("Leyenda:"):
                tabla_inicio = i + 1
                break
            elif ":" in linea:
                clave, valor = linea.split(":", 1)
                resumen[clave.strip().lower()] = valor.strip()

        # === Resumen ===
        fecha = extraer_fecha_desde_lineas(lineas, os.path.basename(self.path_txt))
        resumen_data = {
            "codigo": resumen.get("codigo del paciente"),
            "fecha": resumen.get("fecha de registro"),
            "fecha_formateada": formatear_fecha_ddmmYYYY(fecha),
            "nivel": resumen.get("nivel"),
            "puntuacion": resumen.get("puntuacion"),
        }
        df_resumen = pd.DataFrame([resumen_data])

        # === Tracking ===
        tabla_data = [l.strip() for l in lineas[tabla_inicio:] if l.strip()]
        registros = []
        max_items = 0
        max_peligros = 0

        for fila in tabla_data:
            partes = fila.split(";")
            tiempo = partes[0]
            mirando_x = partes[1]
            mirando_y = partes[2]

            resto = partes[3:]
            mitad = len(resto) // 2
            items = resto[:mitad]
            peligros = resto[mitad:]

            # Agrupar x, y en tuplas
            items_pares = [f"{items[i]}:{items[i+1]}" for i in range(0, len(items)-1, 2)]
            peligros_pares = [f"{peligros[i]}:{peligros[i+1]}" for i in range(0, len(peligros)-1, 2)]

            max_items = max(max_items, len(items_pares))
            max_peligros = max(max_peligros, len(peligros_pares))

            registro = {
                "tiempo": tiempo,
                "mirando_x": mirando_x,
                "mirando_y": mirando_y
            }

            for idx, val in enumerate(items_pares, start=1):
                registro[f"item_{idx}"] = val
            for idx, val in enumerate(peligros_pares, start=1):
                registro[f"peligro_{idx}"] = val

            registros.append(registro)

        # Completar columnas faltantes (para filas con menos items o peligros)
        columnas_base = ["tiempo", "mirando_x", "mirando_y"]
        columnas_items = [f"item_{i+1}" for i in range(max_items)]
        columnas_peligros = [f"peligro_{i+1}" for i in range(max_peligros)]
        columnas_finales = columnas_base + columnas_items + columnas_peligros

        df_tracking = pd.DataFrame(registros, columns=columnas_finales)

        # === Guardar ===
        nombre_base = os.path.splitext(os.path.basename(self.path_txt))[0]
        codigo = df_resumen.at[0, "codigo"]

        return guardar_csvs(df_resumen, df_tracking, codigo, fecha, nombre_base, self.root_dir)
