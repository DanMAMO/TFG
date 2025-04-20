# src/galeria/procesador.py
import pandas as pd
import os
from base.informe_base import InformeBase
from utils.helpers import extraer_fecha_desde_lineas, formatear_fecha_ddmmYYYY, guardar_csvs, parsear_clave_valor


class InformeGaleria(InformeBase):
    def procesar(self):
        with open(self.path_txt, "r", encoding="utf-8") as f:
            lineas = f.readlines()

        resumen = {}
        tabla_inicio = None
        for i, linea in enumerate(lineas):
            linea = linea.strip()
            if linea.startswith("Leyenda:"):
                tabla_inicio = i + 1
                columnas = [col.strip() for col in linea.replace("Leyenda:", "").split(";")]
                break
            clave, valor = parsear_clave_valor(linea)
            if clave:
                resumen[clave] = valor

        nombre_base = os.path.splitext(os.path.basename(self.path_txt))[0]
        fecha = extraer_fecha_desde_lineas(lineas, nombre_base)
        fecha_formateada = formatear_fecha_ddmmYYYY(fecha)

        df_resumen = pd.DataFrame([{
            "codigo": resumen.get("codigo del paciente"),
            "fecha": resumen.get("fecha de registro"),
            "fecha_num": fecha_formateada,
            "nivel": resumen.get("nivel actual"),
            "aciertos": resumen.get("aciertos"),
            "errores": resumen.get("errores"),
            "omisiones": resumen.get("omision"),
            "puntos": resumen.get("puntos")
        }])

        tabla_data = [line.strip() for line in lineas[tabla_inicio:] if line.strip()]
        df_tracking = pd.DataFrame([row.split(";") for row in tabla_data], columns=columnas)

        codigo = df_resumen.at[0, "codigo"]

        return guardar_csvs(df_resumen, df_tracking, codigo, fecha, nombre_base, self.root_dir)
