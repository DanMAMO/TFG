# src/main.py
import os
import glob
import sys
from galeria.procesar import InformeGaleria

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(ROOT_DIR, "data", "galeria_tiro")

# Modo opcional con tkinter

def seleccionar_archivo():
    from tkinter import Tk, filedialog
    Tk().withdraw()
    return filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])

modo_manual = "--manual" in sys.argv

if modo_manual:
    print("🟢 Modo MANUAL activado")
    archivo = seleccionar_archivo()
    if archivo:
        informe = InformeGaleria(archivo, ROOT_DIR)
        resumen_path, tracking_path = informe.procesar()
        print(f"✅ Procesado único:\n- {resumen_path}\n- {tracking_path}")
    else:
        print("❌ No se seleccionó ningún archivo.")
else:
    print("🟡 Modo BATCH: procesando todos los archivos en carpeta")
    informes = glob.glob(os.path.join(DATA_DIR, "*.txt"))
    for path in informes:
        informe = InformeGaleria(path, ROOT_DIR)
        resumen_path, tracking_path = informe.procesar()
        print(f"\n✅ Procesado: {os.path.basename(path)}")
        print(f" - Resumen: {resumen_path}\n - Tracking: {tracking_path}")