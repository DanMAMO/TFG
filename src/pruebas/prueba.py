import json
import csv

# Leer el archivo JSON
with open(".txt", "r") as archivo:
    datos = json.load(archivo)

# Extraer solo los datos planos (no listas largas)
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

# Escribir el CSV
with open("paciente.csv", "w", newline="") as archivo_csv:
    escritor = csv.DictWriter(archivo_csv, fieldnames=fila.keys())
    escritor.writeheader()
    escritor.writerow(fila)

print("Archivo 'paciente.csv' creado correctamente.")
