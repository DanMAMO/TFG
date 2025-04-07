import pandas as pd
import os

# === CONFIGURACIÓN: Cambiar solo esta ruta ===
#archivo_txt = "ruta/a/tu/informe.txt"  # <-- editá esta línea
archivo_txt = "C:/Users/Daniel M.M/PycharmProjects/TFG/001-Tarea galeria de tiro-jueves, 18 marzo 2021 11-36-06.txt"
# === PROCESAMIENTO ===

# Leer líneas del archivo
with open(archivo_txt, "r", encoding="utf-8") as f:
    lineas = f.readlines()

# Separar encabezado y tabla
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

# Crear DataFrame del resumen
df_resumen = pd.DataFrame([{
    "codigo": resumen.get("codigo del paciente"),
    "fecha": resumen.get("fecha de registro"),
    "nivel": resumen.get("Nivel actual"),
    "aciertos": resumen.get("Aciertos"),
    "errores": resumen.get("Errores"),
    "omisiones": resumen.get("Omision"),
    "puntos": resumen.get("Puntos")
}])

# Leer y estructurar los datos frame a frame
tabla_data = [line.strip() for line in lineas[tabla_inicio:] if line.strip()]
df_tracking = pd.DataFrame([row.split(";") for row in tabla_data], columns=columnas)

# === GUARDAR COMO CSV ===

# Obtener nombre base del archivo
nombre_base = os.path.splitext(os.path.basename(archivo_txt))[0]
csv_resumen = f"{nombre_base}_resumen.csv"
csv_tracking = f"{nombre_base}_tracking.csv"

# Guardar
df_resumen.to_csv(csv_resumen, index=False)
df_tracking.to_csv(csv_tracking, index=False)

print(f"✅ Archivos generados:\n - {csv_resumen}\n - {csv_tracking}")
