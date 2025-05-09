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
    """
    Carga en un solo DataFrame:
     - Todos los *_resumen.csv de juegos en cualquier subdirectorio
     - Todos los resumen_usuario_*.csv bajo outputs/pacientes/{codigo}/
    """
    patterns = [
        # Juego: busca recursivamente en cualquier nivel
        os.path.join(PACIENTES_DIR, "**", "*_resumen.csv"),
        # Usuario: solo en carpeta paciente (sin año/mes)
        os.path.join(PACIENTES_DIR, "*", "resumen_usuario_*.csv"),
    ]
    dfs = []
    for pat in patterns:
        for fpath in glob.glob(pat, recursive=True):
            df = pd.read_csv(fpath, sep=";")
            basename = os.path.basename(fpath).lower()
            # Determinar el nombre del juego / tipo de resumen
            if basename.startswith("resumen_usuario"):
                juego = "ResumenUsuario"
            else:
                # Extrae “Memory”, “Galería de tiro”, etc.
                parts = os.path.basename(fpath).split("-", 2)
                juego = parts[1].replace("Tarea ", "") if len(parts) >= 2 else "desconocido"
            df["juego"] = juego
            dfs.append(df)
    return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()

def generar_estadisticas(df):
    """Calcula descriptivos y guarda en Excel y PNG."""
    if df.empty:
        print("⚠️ No se encontraron archivos de resumen para análisis.")
        return None, None

    # 1) Descriptivos generales
    desc = df.describe(include="all")

    # 2) MediaPuntuacion desde ResumenUsuario
    pattern_user = os.path.join(PACIENTES_DIR, "*", "resumen_usuario_*.csv")
    user_dfs = []
    for path in glob.glob(pattern_user, recursive=False):
        u = pd.read_csv(path, sep=";")
        user_dfs.append(u)

    if user_dfs:
        df_user = pd.concat(user_dfs, ignore_index=True)
        df_mp = df_user[[
            "codigo",
            "puntuacionTopos",
            "puntuacionMemory",
            "puntuacionGaleriaTiro",
            "puntuacionAventuras",
            "puntuacionCaminos"
        ]].rename(columns={
            "puntuacionTareaTopos":       "Topos",
            "puntuacionTareaMemory":      "Memory",
            "puntuacionTareaGaleriaTiro": "Galería",
            "puntuacionTareaAventuras":   "Aventuras",
            "puntuacionTareaCaminos":     "Caminos",
        })
    else:
        df_mp = pd.DataFrame(columns=[
            "codigo", "Topos", "Memory", "Galería", "Aventuras", "Caminos"
        ])

    # 3) Generar gráfico de evolución para todos los juegos (usando df_user) de ejemplo (opcional)
    # — Convertimos fecha —
    df_user["fecha_dt"] = pd.to_datetime(
        df_user.get("fecha_formateada", df_user.get("fecha_num", "")),
        format="%d.%m.%Y", errors="coerce"
    )
    df_user = df_user.sort_values("fecha_dt")

    # — Preparamos paths —
    timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
    grafico_path = os.path.join(EDA_DIR, f"evolucion_{timestamp}.png")

    # — Dibujamos una línea por cada columna de df_mp —
    plt.figure(figsize=(8, 4))
    for col in ["Topos", "Memory", "Galería", "Aventuras", "Caminos"]:
        if col in df_mp.columns:
            plt.plot(df_user["fecha_dt"], df_user[col], marker="o", label=col)
    plt.title(f"Evolución de puntuación - Paciente {df_mp['codigo'].iloc[0]}")
    plt.xlabel("Fecha")
    plt.ylabel("Puntuación")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(grafico_path)
    print(f"→ Gráfico generado en {grafico_path}")

    # 4) Guardar todo en un solo Excel
    excel_path = os.path.join(EDA_DIR, f"EDA_completo_{timestamp}.xlsx")
    with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
        df.to_excel(writer,   sheet_name="DatosCrudos",      index=False)
        desc.to_excel(writer, sheet_name="Descriptivos")
        df_mp.to_excel(writer, sheet_name="MediaPuntuacion",   index=False)
    print(f"✅ EDA completo exportado a {excel_path}")

    # 5) Devuelve ambos DataFrames
    return desc, df_mp


def main():
    df_all = cargar_resumenes()
    generar_estadisticas(df_all)

if __name__ == "__main__":
    main()