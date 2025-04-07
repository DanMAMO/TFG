# src/main.py
import os
import glob
import sys
from src.galeria.procesar import procesar_archivo_galeria

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
        resumen_path, tracking_path = procesar_archivo_galeria(archivo, ROOT_DIR)
        print(f"✅ Procesado único:\n- {resumen_path}\n- {tracking_path}")
    else:
        print("❌ No se seleccionó ningún archivo.")
else:
    print("🟡 Modo BATCH: procesando todos los archivos en carpeta")
    informes = glob.glob(os.path.join(DATA_DIR, "*.txt"))
    for informe in informes:
        resumen_path, tracking_path = procesar_archivo_galeria(informe, ROOT_DIR)
        print(f"\n✅ Procesado: {os.path.basename(informe)}")
        print(f" - Resumen: {resumen_path}\n - Tracking: {tracking_path}")
