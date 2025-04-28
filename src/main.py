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

    # Detección por nombre de archivo
    if "galeria" in nombre_archivo:
        return InformeGaleria(path, ROOT_DIR)
    elif "memory" in nombre_archivo:
        return InformeMemory(path, ROOT_DIR)
    elif "topos" in nombre_archivo:
        return InformeTopos(path, ROOT_DIR)
    elif "caminos" in nombre_archivo:
        return InformeCaminos(path, ROOT_DIR)
    elif "aventuras" in nombre_archivo:
        return InformeAventuras(path, ROOT_DIR)
    elif nombre_archivo.startswith("paciente") and nombre_archivo.endswith(".txt"):
        return ResumenUsuario(path, ROOT_DIR)

    # Heurística por contenido (fallback)
    try:
        with open(path, "r", encoding="utf-8") as f:
            preview = f.read(1000).lower()
            if '"nombre"' in preview and '"codigo"' in preview:
                return ResumenUsuario(path, ROOT_DIR)
            elif "galeria de tiro" in preview:
                return InformeGaleria(path, ROOT_DIR)
            elif "memory" in preview:
                return InformeMemory(path, ROOT_DIR)
            elif "tarea de topos" in preview:
                return InformeTopos(path, ROOT_DIR)
            elif "tarea de caminos" in preview:
                return InformeCaminos(path, ROOT_DIR)
            elif "tarea de aventuras" in preview:
                return InformeAventuras(path, ROOT_DIR)
    except Exception:
        pass

    raise ValueError(f"No se reconoce el tipo de informe: {path}")

if modo_manual:
    print("🟢 Modo MANUAL activado")
    archivo = seleccionar_archivo()
    if archivo:
        # Saltar archivos vacíos
        if os.path.getsize(archivo) == 0:
            print(f"⚠️ Informe vacío: {os.path.basename(archivo)} → saltando.")
        else:
            try:
                informe = obtener_informe(archivo)
                resumen_path, tracking_path = informe.procesar()
                print(f"✅ Procesado único:\n- {resumen_path}\n- {tracking_path}")
            except Exception as e:
                print(f"⚠️ Error procesando {os.path.basename(archivo)}: {e}")
    else:
        print("❌ No se seleccionó ningún archivo.")
else:
    print("🟡 Modo BATCH: procesando todos los archivos en data/*/")
    for carpeta in ["galeria", "memory", "topos", "caminos", "aventuras", "pacientes"]:
        ruta = os.path.join(ROOT_DIR, "data", carpeta)
        informes = glob.glob(os.path.join(ruta, "*.txt"))
        for path in informes:
            nombre = os.path.basename(path)
            # Saltar archivos vacíos
            if os.path.getsize(path) == 0:
                print(f"\n⚠️ Informe vacío: {nombre} → saltando.")
                continue

            try:
                informe = obtener_informe(path)
                resumen_path, tracking_path = informe.procesar()
                print(f"\n✅ Procesado: {nombre}")
                print(f" - Resumen: {resumen_path}\n - Tracking: {tracking_path}")
            except Exception as err:
                print(f"\n⚠️ Error procesando {nombre}: {err}")
                # Continuar con el siguiente informe
                continue
