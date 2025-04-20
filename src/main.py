# src/main.py
import os
import glob
import sys
from galeria.procesar import InformeGaleria
from memory.procesar import InformeMemory
from topos.procesar import InformeTopos
from caminos.procesar import InformeCaminos
from aventuras.procesar import InformeAventuras
from usuario.procesar import ResumenUsuario



ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# === Modo manual ===
def seleccionar_archivo():
    from tkinter import Tk, filedialog
    Tk().withdraw()
    return filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])

modo_manual = "--manual" in sys.argv

# === Asignar clase según carpeta o contenido ===
def obtener_informe(path):
    nombre_archivo = os.path.basename(path).lower()
    if "galeria" in path.lower():
        return InformeGaleria(path, ROOT_DIR)
    elif "memory" in path.lower():
        return InformeMemory(path, ROOT_DIR)
    elif "topos" in path.lower():
        return InformeTopos(path, ROOT_DIR)
    elif "caminos" in path.lower():
        return InformeCaminos(path, ROOT_DIR)
    elif "aventuras" in path.lower():
        return InformeAventuras(path, ROOT_DIR)
    elif nombre_archivo.startswith("paciente") and nombre_archivo.endswith(".txt"):
        return ResumenUsuario(path, ROOT_DIR)

    with open(path, "r", encoding="utf-8") as f:
        contenido = f.read(500).lower()

    if "memory" in contenido:
        return InformeMemory(path, ROOT_DIR)
    elif "galeria de tiro" in contenido:
        return InformeGaleria(path, ROOT_DIR)
    elif "tarea de topos" in contenido:
        return InformeTopos(path, ROOT_DIR)
    elif "tarea de caminos" in contenido:
        return InformeCaminos(path, ROOT_DIR)
    elif "tarea de aventuras" in contenido:
        return InformeAventuras(path, ROOT_DIR)
    elif "paciente" in contenido:
        return ResumenUsuario(path, ROOT_DIR)

    raise ValueError(f"No se reconoce el tipo de informe: {path}")

if modo_manual:
    print("🟢 Modo MANUAL activado")
    archivo = seleccionar_archivo()
    if archivo:
        informe = obtener_informe(archivo)
        resumen_path, tracking_path = informe.procesar()
        print(f"✅ Procesado único:\n- {resumen_path}\n- {tracking_path}")
    else:
        print("❌ No se seleccionó ningún archivo.")
else:
    print("🟡 Modo BATCH: procesando todos los archivos en data/*/")
    for carpeta in ["galeria", "memory", "topos", "caminos", "aventuras", "pacientes"]:
        ruta = os.path.join(ROOT_DIR, "data", carpeta)
        informes = glob.glob(os.path.join(ruta, "*.txt"))
        for path in informes:
            informe = obtener_informe(path)
            resumen_path, tracking_path = informe.procesar()
            print(f"\n✅ Procesado: {os.path.basename(path)}")
            print(f" - Resumen: {resumen_path}\n - Tracking: {tracking_path}")
