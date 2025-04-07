import pandas as pd
import os
from datetime import datetime
from tkinter import Tk, filedialog

from src.pruebas.galeria_de_tiro import nombre_base

# === Selección visual del archivo .txt ===
Tk().withdraw()
archivo_txt = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])

# === Ruta raíz del proyecto (2 niveles arriba de este script)
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# === Leer líneas del archivo seleccionado ===
with open(archivo_txt, "r", encoding="utf-8") as f:
    lineas = f.readlines()

# === Extraer encabezado y columnas ===
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

# === Crear DataFrame del resumen ===
df_resumen = pd.DataFrame([{
    "codigo": resumen.get("codigo del paciente"),
    "fecha": resumen.get("fecha de registro"),
    "nivel": resumen.get("Nivel actual"),
    "aciertos": resumen.get("Aciertos"),
    "errores": resumen.get("Errores"),
    "omisiones": resumen.get("Omision"),
    "puntos": resumen.get("Puntos")
}])

# === Crear DataFrame del tracking ===
tabla_data = [line.strip() for line in lineas[tabla_inicio:] if line.strip()]
df_tracking = pd.DataFrame([row.split(";") for row in tabla_data], columns=columnas)

# === Generar carpeta de salida: outputs/pacientes/{codigo}/{año}/{mes}/ ===
codigo = df_resumen.at[0, "codigo"]
fecha_txt = df_resumen.at[0, "fecha"]

try:
    fecha_parseada = datetime.strptime(fecha_txt.split(", ")[-1], "%d %B %Y %H-%M-%S")
except ValueError:
    fecha_parseada = datetime(2021, 3, 18, 11, 36, 6)  # fallback en caso de error

anio = str(fecha_parseada.year)
mes = str(fecha_parseada.month).zfill(2)

# Ruta de salida completa
output_dir = os.path.join(ROOT_DIR, "outputs", "pacientes", codigo, anio, mes)
os.makedirs(output_dir, exist_ok=True)

# Obtener nombre base del archivo
nombre_base = os.path.splitext(os.path.basename(archivo_txt))[0]

# Generar ruta completa con nombre personalizado
csv_resumen = os.path.join(output_dir, f"{nombre_base}_resumen.csv")
csv_tracking = os.path.join(output_dir, f"{nombre_base}_tracking.csv")

# Guardar CSVs
df_resumen.to_csv(csv_resumen, index=False)
df_tracking.to_csv(csv_tracking, index=False)

