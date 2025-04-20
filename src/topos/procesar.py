# src/topos/procesar.py
import pandas as pd
import os
from base.informe_base import InformeBase
from utils.helpers import (
    extraer_fecha_desde_lineas,
    formatear_fecha_ddmmYYYY,
    guardar_csvs,
    parsear_clave_valor,
    extraer_valores_multilinea
)

class InformeTopos(InformeBase):
    def procesar(self):
        with open(self.path_txt, "r", encoding="utf-8") as f:
            lineas = f.readlines()

        resumen = {}
        posiciones = []
        tabla_inicio = None

        for i, linea in enumerate(lineas):
            linea = linea.strip()

            if linea.startswith("Leyenda:"):
                tabla_inicio = i + 1
                columnas = [col.strip() for col in linea.replace("Leyenda:", "").split(";")]
                break
            elif ":" in linea:
                clave, valor = parsear_clave_valor(linea)
                if clave:
                    resumen[clave] = valor
            elif "Posiciones fijas de los estimulos" in linea:
                contenido_mismo_renglon = linea.replace("Posiciones fijas de los estimulos", "").strip()
                if contenido_mismo_renglon:
                    posiciones += [p.strip() for p in contenido_mismo_renglon.split() if p.strip()]
                posiciones += extraer_valores_multilinea(lineas, i, separador=" ", stopwords=("Leyenda",))

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
            **{f"posicion_{i+1}": posiciones[i] for i in range(len(posiciones))}
        }])

        tabla_data = [line.strip() for line in lineas[tabla_inicio:] if line.strip()]
        columnas = ["tiempo", "estimulo_objetivo", "x", "y"] + [f"matriz_estado_{i+1}" for i in range(len(tabla_data[0].split(";")) - 4)]
        df_tracking = pd.DataFrame([row.split(";") for row in tabla_data], columns=columnas)

        df_tracking["matriz_estado"] = df_tracking[[col for col in df_tracking.columns if col.startswith("matriz_estado_")]].agg("-".join, axis=1)
        df_tracking = df_tracking[["tiempo", "estimulo_objetivo", "x", "y", "matriz_estado"]]

        codigo = df_resumen.at[0, "codigo"]
        return guardar_csvs(df_resumen, df_tracking, codigo, fecha, nombre_base, self.root_dir)
