import os
import glob
import pandas as pd
import matplotlib.pyplot as plt

# === Configuración de rutas ===
# Partimos de este archivo en src/analysis/eda.py
CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))
OUTPUTS_DIR = os.path.join(PROJECT_ROOT, "outputs", "pacientes")

def cargar_resumenes():
    """Carga todos los *_resumen.csv en un único DataFrame."""
    pattern = os.path.join(OUTPUTS_DIR, "*", "*", "*", "*_resumen.csv")
    files = glob.glob(pattern)
    dfs = []
    for fpath in files:
        df = pd.read_csv(fpath, sep=";")
        basename = os.path.basename(fpath)
        # Extrae juego del nombre de archivo (asume "código-Tarea juego-fecha_resumen.csv")
        parts = basename.split("-", 2)
        if len(parts) >= 2:
            juego = parts[1].replace("Tarea ", "")
        else:
            juego = "desconocido"
        df["juego"] = juego
        dfs.append(df)
    return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()

def generar_estadisticas(df):
    """Calcula descriptivos y guarda en CSV."""
    if df.empty:
        print("⚠️ No se encontraron archivos de resumen para análisis.")
        return None, None
    # Descriptivos generales
    desc = df.describe(include="all")
    desc.to_csv("eda_descriptivos.csv", sep=";")
    print("→ eda_descriptivos.csv generado")
    # Pivot: media de puntuación por paciente y juego
    pivot = df.pivot_table(
        index="codigo", columns="juego", values="puntuacion", aggfunc="mean"
    )
    pivot.to_csv("eda_puntuacion_media_por_paciente.csv", sep=";")
    print("→ eda_puntuacion_media_por_paciente.csv generado")
    return desc, pivot

def plot_evolucion(df, paciente=None):
    """Grafica evolución de la puntuación para un paciente (el primero por defecto)."""
    if df.empty:
        print("⚠️ DataFrame vacío, no se genera gráfico.")
        return
    if paciente is None:
        paciente = df["codigo"].iloc[0]
    sub = df[df["codigo"] == paciente].copy()
    # Convertir fecha_num a datetime
    sub["fecha_dt"] = pd.to_datetime(sub["fecha_num"], format="%d.%m.%Y", errors="coerce")
    sub = sub.sort_values("fecha_dt")
    plt.figure(figsize=(6, 4))
    plt.plot(sub["fecha_dt"], sub["puntuacion"], marker="o")
    plt.title(f"Evolución de puntuación - Paciente {paciente}")
    plt.xlabel("Fecha")
    plt.ylabel("Puntuación")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("evolucion_puntuacion_paciente.png")
    print("→ evolucion_puntuacion_paciente.png generado")

if __name__ == "__main__":
    df_all = cargar_resumenes()
    desc, pivot = generar_estadisticas(df_all)
    plot_evolucion(df_all)
