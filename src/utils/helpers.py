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

def extraer_fecha_desde_lineas(lineas, nombre_archivo=None):
    meses = {
        "enero": "01", "febrero": "02", "marzo": "03", "abril": "04",
        "mayo": "05", "junio": "06", "julio": "07", "agosto": "08",
        "septiembre": "09", "octubre": "10", "noviembre": "11", "diciembre": "12"
    }
    for linea in lineas:
        if "fecha de registro" in linea.lower():
            match = re.search(r"(\d{1,2}) (\w+) (\d{4}) (\d{2})-(\d{2})-(\d{2})", linea)
            if match:
                dia, mes_nombre, anio, hora, minuto, segundo = match.groups()
                mes = meses.get(mes_nombre.lower())
                if mes:
                    fecha_str = f"{anio}-{mes}-{dia} {hora}:{minuto}:{segundo}"
                    try:
                        return datetime.strptime(fecha_str, "%Y-%m-%d %H:%M:%S")
                    except ValueError:
                        break
    # Fallback: intentar desde nombre del archivo
    if nombre_archivo:
        match = re.search(r"(\d{1,2}) (\w+) (\d{4}) (\d{2})-(\d{2})-(\d{2})", nombre_archivo)
        if match:
            dia, mes_nombre, anio, hora, minuto, segundo = match.groups()
            mes = meses.get(mes_nombre.lower())
            if mes:
                fecha_str = f"{anio}-{mes}-{dia} {hora}:{minuto}:{segundo}"
                try:
                    return datetime.strptime(fecha_str, "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    pass
    return datetime.now()

def guardar_csvs(df_resumen, df_tracking, codigo, fecha, nombre_base, root_dir):
    anio = str(fecha.year)
    mes = str(fecha.month).zfill(2)

    output_dir = os.path.join(root_dir, "outputs", "pacientes", codigo, anio, mes)
    os.makedirs(output_dir, exist_ok=True)

    resumen_path = os.path.join(output_dir, f"{nombre_base}_resumen.csv")
    tracking_path = os.path.join(output_dir, f"{nombre_base}_tracking.csv")

    resumen_path = generar_nombre_unico(resumen_path)
    tracking_path = generar_nombre_unico(tracking_path)

    df_resumen.to_csv(resumen_path, index=False, sep=";")
    df_tracking.to_csv(tracking_path, index=False, sep=";")

    return resumen_path, tracking_path
