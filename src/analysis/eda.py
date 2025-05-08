import os
import glob
import pandas as pd
import matplotlib.pyplot as plt

# === Configuración de rutas ===
CURRENT_DIR    = os.path.dirname(__file__)
PROJECT_ROOT   = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))
PACIENTES_DIR  = os.path.join(PROJECT_ROOT, "outputs", "pacientes")
EDA_DIR        = os.path.join(PROJECT_ROOT, "outputs", "eda")
os.makedirs(EDA_DIR, exist_ok=True)

def cargar_resumenes():
    """Carga todos los *_resumen.csv en un único DataFrame."""
    pattern = os.path.join(PACIENTES_DIR, "*", "*", "*", "*_resumen.csv")
    files = glob.glob(pattern)
    dfs = []
    for fpath in files:
        df = pd.read_csv(fpath, sep=";")
        basename = os.path.basename(fpath)
        parts = basename.split("-", 2)
        if len(parts) >= 2:
            juego = parts[1].replace("Tarea ", "")
        else:
            juego = "desconocido"
        df["juego"] = juego
        dfs.append(df)
    return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()

def generar_estadisticas(df):
    """Calcula descriptivos y guarda en Excel y PNG."""
    if df.empty:
        print("⚠️ No se encontraron archivos de resumen para análisis.")
        return None, None

    # Estadísticos y pivote
    desc = df.describe(include="all")
    pivot = df.pivot_table(index="codigo", columns="juego", values="puntuacion", aggfunc="mean")

    # Timestamp para nombres de archivo
    timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
    excel_path = os.path.join(EDA_DIR, f"EDA_completo_{timestamp}.xlsx")
    grafico_path = os.path.join(EDA_DIR, f"evolucion_{timestamp}.png")

    # Generar gráfico de evolución para el primer paciente
    plt.figure(figsize=(6, 4))
    paciente = df["codigo"].iloc[0]
    sub = df[df["codigo"] == paciente].copy()
    sub["fecha_dt"] = pd.to_datetime(sub["fecha_num"], format="%d.%m.%Y", errors="coerce")
    sub = sub.sort_values("fecha_dt")
    plt.plot(sub["fecha_dt"], sub["puntuacion"], marker="o")
    plt.title(f"Evolución de puntuación - Paciente {paciente}")
    plt.xlabel("Fecha")
    plt.ylabel("Puntuación")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(grafico_path)
    print(f"→ Gráfico generado en {grafico_path}")

    # Guardar todo en un solo Excel con varias hojas
    with pd.ExcelWriter(excel_path, engine="xlsxwriter") as writer:
        df.to_excel(writer, sheet_name="DatosCrudos", index=False)
        desc.to_excel(writer, sheet_name="Descriptivos")
        pivot.to_excel(writer, sheet_name="MediaPuntuacion")
    print(f"✅ EDA completo exportado a {excel_path}")

    return desc, pivot

def main():
    df_all = cargar_resumenes()
    generar_estadisticas(df_all)

if __name__ == "__main__":
    main()