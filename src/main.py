# src/main.py
import os
import glob
from src.galeria.procesador import procesar_archivo_galeria

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(ROOT_DIR, "data", "galeria_tiro")

informes = glob.glob(os.path.join(DATA_DIR, "*.txt"))

for informe in informes:
    resumen_path, tracking_path = procesar_archivo_galeria(informe, ROOT_DIR)
    print(f"\n✅ Procesado: {os.path.basename(informe)}")
    print(f" - Resumen: {resumen_path}\n - Tracking: {tracking_path}")