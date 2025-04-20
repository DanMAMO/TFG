# src/caminos/procesar.py
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

class InformeCaminos(InformeBase):
    def procesar(self):
        with open(self.path_txt, "r", encoding="utf-8") as f:
            lineas = f.readlines()

        resumen = {}
        posiciones = []
        tabla_inicio = None

        for i, linea in enumerate(lineas):
            linea = linea.strip()
            if linea.startswith("0,") or linea.startswith("0."):
                tabla_inicio = i
                break
            elif ":" in linea:
                clave, valor = parsear_clave_valor(linea)
                if clave:
                    resumen[clave] = valor
            elif "Posiciones fijas de las tarjetas" in linea:
                contenido_mismo_renglon = linea.replace("Posiciones fijas de las tarjetas", "").strip()
                if contenido_mismo_renglon:
                    posiciones += [p.strip() for p in contenido_mismo_renglon.split() if p.strip()]
                posiciones += extraer_valores_multilinea(lineas, i, separador=" ", stopwords=("0,", "0.",))

        nombre_base = os.path.splitext(os.path.basename(self.path_txt))[0]
        fecha = extraer_fecha_desde_lineas(lineas, nombre_base)
        fecha_formateada = formatear_fecha_ddmmYYYY(fecha)

        df_resumen = pd.DataFrame([{
            "codigo": resumen.get("codigo del paciente"),
            "fecha": resumen.get("fecha de registro"),
            "fecha_num": fecha_formateada,
            "nivel": resumen.get("nivel actual"),
            "dimensiones": resumen.get("dimensiones matriz"),
            "repeticiones": resumen.get("repeticiones")
        }])

        tabla_data = [line.strip() for line in lineas[tabla_inicio:] if line.strip() and ";" in line]
        df_tracking = pd.DataFrame([row.split(";") for row in tabla_data], columns=["tiempo", "x", "y"])

        for i, pos in enumerate(posiciones):
            df_tracking[f"posicion_{i+1}"] = pos

        codigo = df_resumen.at[0, "codigo"]
        return guardar_csvs(df_resumen, df_tracking, codigo, fecha, nombre_base, self.root_dir)
