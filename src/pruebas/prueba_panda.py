import json
import pandas as pd
import os

# === CONFIGURACIÓN ===
# Ruta al archivo del paciente (puede cambiar por cada uso)
# archivo_entrada = "../Paciente0.txt"
# archivo_entrada = "/Users/danielmm/PycharmProjects/TFG/Paciente0.txt"

# === CARGAR DATOS JSON ===
with open(archivo_entrada, "r")  as f:
    datos = json.load(f)

# === EXTRAER DATOS RELEVANTES ===
fila = {
    "nombre": datos["nombre"],
    "codigo": datos["codigo"],
    "esZurdo": datos["esZurdo"],
    "ultimoNivelTopos": datos["ultimoNivelDesbloqueadoTareaTopos"],
    "ultimoNivelMemory": datos["ultimoNivelDesbloqueadoTareaMemory"],
    "ultimoNivelGaleriaTiro": datos["ultimoNivelDesbloqueadoTareaGaleriaTiro"],
    "ultimoNivelAventuras": datos["ultimoNivelDesbloqueadoTareaAventuras"],
    "puntuacionTopos": datos["puntuacionTareaTopos"],
    "puntuacionMemory": datos["puntuacionTareaMemory"],
    "puntuacionGaleriaTiro": datos["puntuacionTareaGaleriaTiro"],
    "puntuacionAventuras": datos["puntuacionTareaAventuras"],
    "nivelesRecord": sum(datos["nivelesConRecordTareaMemory"]),
    "medallasTotales": sum(datos["medallasTareaMemory"]),
    "multiplicadorVelocidad": datos["multiplicadorVelocidad"]
}

# === CREAR DATAFRAME Y GUARDAR CSV ===
df = pd.DataFrame([fila])

# Usar nombre o código para nombrar el archivo de salida
#nombre_archivo = f"{datos['nombre']}.csv"  # O: f"{datos['codigo']}.csv"
nombre_archivo = f"/Users/danielmm/PycharmProjects/TFG/{datos['nombre']}.csv"
df.to_csv(nombre_archivo, index=False)

print(f"Archivo '{nombre_archivo}' generado correctamente.")
