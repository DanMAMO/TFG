# src/galeria/procesador.py
import pandas as pd
import os
from utils.helpers import extraer_fecha_desde_nombre, guardar_csvs

def procesar_archivo_galeria(path_txt, root_dir):
    with open(path_txt, "r", encoding="utf-8") as f:
        lineas = f.readlines()

    resumen = {}
    tabla_inicio = None
    for i, linea in enumerate(lineas):
        linea = linea.strip()
        if linea.startswith("Leyenda:"):
            tabla_inicio = i + 1
            columnas = [col.strip() for col in linea.replace("Leyenda:", "").split(";")]
            break
        elif ":" in linea:
            clave, valor = linea.split(":", 1)
            resumen[clave.strip()] = valor.strip()

    df_resumen = pd.DataFrame([{
        "codigo": resumen.get("codigo del paciente"),
        "fecha": resumen.get("fecha de registro"),
        "nivel": resumen.get("Nivel actual"),
        "aciertos": resumen.get("Aciertos"),
        "errores": resumen.get("Errores"),
        "omisiones": resumen.get("Omision"),
        "puntos": resumen.get("Puntos")
    }])

    tabla_data = [line.strip() for line in lineas[tabla_inicio:] if line.strip()]
    df_tracking = pd.DataFrame([row.split(";") for row in tabla_data], columns=columnas)

    nombre_base = os.path.splitext(os.path.basename(path_txt))[0]
    fecha = extraer_fecha_desde_nombre(nombre_base)
    codigo = df_resumen.at[0, "codigo"]

    return guardar_csvs(df_resumen, df_tracking, codigo, fecha, nombre_base, root_dir)

