# utils/helpers.py
import os
import re
from datetime import datetime

def generar_nombre_unico(base_path):
    if not os.path.exists(base_path):
        return base_path
    nombre, extension = os.path.splitext(base_path)
    contador = 2
    nuevo_path = f"{nombre}_v{contador}{extension}"
    while os.path.exists(nuevo_path):
        contador += 1
        nuevo_path = f"{nombre}_v{contador}{extension}"
    return nuevo_path

def extraer_fecha_desde_nombre(nombre_archivo):
    match = re.search(r"\d{1,2} \w+ \d{4} \d{2}-\d{2}-\d{2}", nombre_archivo)
    if match:
        texto_fecha = match.group().replace("-", ":")
        try:
            return datetime.strptime(texto_fecha, "%d %B %Y %H:%M:%S")
        except ValueError:
            pass
    return datetime.now()

def guardar_csvs(df_resumen, df_tracking, codigo, fecha, nombre_base, root_dir):
    anio = str(fecha.year)
    mes = str(fecha.month).zfill(2)

    output_dir = os.path.join(root_dir, "outputs", "pacientes", codigo, anio, mes)
    os.makedirs(output_dir, exist_ok=True)

    hora_minuto = fecha.strftime("%H%M%S")
    resumen_path = os.path.join(output_dir, f"{nombre_base}_resumen_{hora_minuto}.csv")
    tracking_path = os.path.join(output_dir, f"{nombre_base}_tracking_{hora_minuto}.csv")

    resumen_path = generar_nombre_unico(resumen_path)
    tracking_path = generar_nombre_unico(tracking_path)

    df_resumen.to_csv(resumen_path, index=False)
    df_tracking.to_csv(tracking_path, index=False)

    return resumen_path, tracking_path