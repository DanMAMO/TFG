import pandas as pd
import os
from datetime import datetime
from tkinter import Tk, filedialog

# === NUEVO: Selección visual del archivo
Tk().withdraw()
archivo_txt = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])

# === NUEVO: Ruta raíz del proyecto (para outputs en TFG/)
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# === Leer contenido del informe
with open(archivo_txt, "r", encoding="utf-8") as f:
    lineas = f.readlines()

# === Procesar encabezado
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

# === Resumen del informe
df_resumen = pd.DataFrame([{
    "codigo": resumen.get("codigo del paciente"),
    "fecha": resumen.get("fecha de registro"),
    "nivel": resumen.get("Nivel actual"),
    "aciertos": resumen.get("Aciertos"),
    "errores": resumen.get("Errores"),
    "omisiones": resumen.get("Omision"),
    "puntos": resumen.get("Puntos")
}])

# === Tracking frame a frame
tabla_data = [line.strip() for line in lineas[tabla_inicio:] if line.strip()]
df_tracking = pd.DataFrame([row.split(";") for row in tabla_data], columns=columnas)

# === Generar carpetas de salida (por paciente/año/mes)
codigo = df_resumen.at[0, "codigo"]
fecha_txt = df_resumen.at[0, "fecha"]

# Manejo seguro de fecha
try:
    fecha_parseada = datetime.strptime(fecha_txt.split(", ")[-1], "%d %B %Y %H-%M-%S")
except ValueError:
    fecha_parseada = datetime.now()

anio = str(fecha_parseada.year)
mes = str(fecha_parseada.month).zfill(2)

output_dir = os.path.join(ROOT_DIR, "outputs", "pacientes", codigo, anio, mes)
os.makedirs(output_dir, exist_ok=True)

# === NUEVO: Crear nombres únicos para archivos
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

# Nombre base con hora
nombre_base = os.path.splitext(os.path.basename(archivo_txt))[0]
hora_minuto = fecha_parseada.strftime("%H%M%S")

csv_resumen = os.path.join(output_dir, f"{nombre_base}_resumen_{hora_minuto}.csv")
csv_tracking = os.path.join(output_dir, f"{nombre_base}_tracking_{hora_minuto}.csv")

# === NUEVO: Evitar sobrescritura
csv_resumen = generar_nombre_unico(csv_resumen)
csv_tracking = generar_nombre_unico(csv_tracking)

# === Guardar archivos
df_resumen.to_csv(csv_resumen, index=False)
df_tracking.to_csv(csv_tracking, index=False)

print(f"✅ Archivos generados:\n- {csv_resumen}\n- {csv_tracking}")


