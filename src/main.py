# src/main.py
import os
import glob
import sys
import shutil
import time
from collections import defaultdict

from galeria.procesar import InformeGaleria
from memory.procesar import InformeMemory
from topos.procesar import InformeTopos
from caminos.procesar import InformeCaminos
from aventuras.procesar import InformeAventuras
from usuario.procesar import ResumenUsuario
from analysis.eda import main as run_eda

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# === Funciones de limpieza ===
ALLOWED_CLEAN_DIRS = {
    os.path.join(ROOT_DIR, "data"),
    os.path.join(ROOT_DIR, "outputs"),
    os.path.join(ROOT_DIR, "outputs", "eda")
}

def limpiar_directorio(path):
    abs_path = os.path.abspath(path)
    if abs_path not in ALLOWED_CLEAN_DIRS:
        print(f"❌ Ruta no autorizada para limpiar: {abs_path}")
        return
    for entry in os.listdir(abs_path):
        full = os.path.join(abs_path, entry)
        if os.path.isdir(full):
            shutil.rmtree(full)
        else:
            os.remove(full)
    print(f"✅ Contenido borrado en: {abs_path}")

def limpiar_data():
    limpiar_directorio(os.path.join(ROOT_DIR, "data"))

def limpiar_outputs():
    limpiar_directorio(os.path.join(ROOT_DIR, "outputs"))

def limpiar_eda():
    limpiar_directorio(os.path.join(ROOT_DIR, "outputs", "eda"))

def eliminar_archivos_vacios():
    """Recorre 'data/' y 'outputs/' eliminando archivos de tamaño 0 bytes."""
    for base in ("data", "outputs"):
        base_dir = os.path.join(ROOT_DIR, base)
        for dirpath, dirnames, filenames in os.walk(base_dir):
            for fname in filenames:
                fpath = os.path.join(dirpath, fname)
                try:
                    if os.path.getsize(fpath) == 0:
                        os.remove(fpath)
                        print(f"🗑️ Eliminado archivo vacío: {fpath}")
                except OSError:
                    pass

# --- Rutina de limpieza por comandos ---
if "--clean-data" in sys.argv:
    limpiar_data()
    sys.exit(0)
if "--clean-outputs" in sys.argv:
    limpiar_outputs()
    sys.exit(0)
if "--clean-eda" in sys.argv:
    limpiar_eda()
    sys.exit(0)
if "--remove-empty" in sys.argv:
    eliminar_archivos_vacios()
    sys.exit(0)

# --- Ejecutar EDA ---
if "--eda" in sys.argv:
    run_eda()
    sys.exit(0)

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
    print("🟡 Modo BATCH: procesando todos los archivos en data/**/*")
    pattern = os.path.join(ROOT_DIR, "data", "**", "*.txt")
    informes = glob.glob(pattern, recursive=True)

    total_files = 0
    skipped_empty = 0
    errors = 0
    success = 0

    durations_all = []
    durations_by_game = defaultdict(list)

    for path in informes:
        total_files += 1
        nombre = os.path.basename(path)

        # Saltar archivos vacíos
        if os.path.getsize(path) == 0:
            print(f"\n⚠️ Informe vacío: {nombre} → saltando.")
            skipped_empty += 1
            continue

        t0 = time.perf_counter()
        try:
            informe = obtener_informe(path)
            resumen_path, tracking_path = informe.procesar()
            dt = time.perf_counter() - t0

            print(f"\n✅ Procesado: {nombre}")
            print(f" - Resumen: {resumen_path}\n - Tracking: {tracking_path}")

            success += 1
            durations_all.append(dt)
            juego = type(informe).__name__.replace("Informe", "")
            durations_by_game[juego].append(dt)

        except Exception as err:
            print(f"\n⚠️ Error procesando {nombre}: {err}")
            errors += 1
            continue

    # Reportar métricas
    print("\n=== MÉTRICAS DE VALIDACIÓN ===")
    print(f"Total de archivos encontrados : {total_files}")
    print(f"Procesados con éxito          : {success} ({100*success/total_files:.1f} %)")
    print(f"Saltados (vacíos)             : {skipped_empty} ({100*skipped_empty/total_files:.1f} %)")
    print(f"Errores de parsing            : {errors} ({100*errors/total_files:.1f} %)")

    if durations_all:
        tm = sum(durations_all) / len(durations_all)
        print(f"Tiempo medio por archivo      : {tm:.3f} s")

        print("\n--- Tiempo medio por juego ---")
        for juego, lst in durations_by_game.items():
            m = sum(lst) / len(lst)
            print(f"  {juego:<10}: {m:.3f} s (n={len(lst)})")
