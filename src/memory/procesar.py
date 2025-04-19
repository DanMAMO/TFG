# src/memory/procesar.py
import pandas as pd
import os
import re
from utils.helpers import extraer_fecha_desde_lineas, guardar_csvs
from base.informe_base import InformeBase

class InformeMemory(InformeBase):
    def procesar(self):
        with open(self.path_txt, "r", encoding="utf-8") as f:
            lineas = f.readlines()

        resumen = {}
        estimulos = []
        posiciones = []
        leyenda_texto = ""
        tabla_inicio = None

        for i, linea in enumerate(lineas):
            linea = linea.strip()

            if linea.startswith("Leyenda:"):
                leyenda_texto = linea
                tabla_inicio = i + 1
                break
            elif ":" in linea:
                clave, valor = linea.split(":", 1)
                resumen[clave.strip().lower()] = valor.strip()
            elif "Estimulos seleccionados para las tarjetas" in linea:
                contenido_mismo_renglon = linea.replace("Estimulos seleccionados para las tarjetas", "").strip()
                if contenido_mismo_renglon:
                    estimulos += [e.strip() for e in contenido_mismo_renglon.split(";") if e.strip()]
                for j in range(i + 1, len(lineas)):
                    est = lineas[j].strip()
                    if est.startswith("Posiciones") or est.startswith("Leyenda") or not est:
                        break
                    estimulos += [e.strip() for e in est.split(";") if e.strip()]
            elif "Posiciones fijas de las tarjetas" in linea:
                contenido_mismo_renglon = linea.replace("Posiciones fijas de las tarjetas", "").strip()
                if contenido_mismo_renglon:
                    posiciones += [p.strip() for p in contenido_mismo_renglon.split() if p.strip()]
                for j in range(i + 1, len(lineas)):
                    pos = lineas[j].strip()
                    if pos.startswith("Leyenda") or not pos:
                        break
                    posiciones += [p.strip() for p in pos.split() if p.strip()]

        for linea in lineas:
            if not resumen.get("partida de bonus"):
                match_bonus = re.search(r"partida de bonus\??\s*(si|no)", linea.lower())
                if match_bonus:
                    resumen["partida de bonus"] = match_bonus.group(1).capitalize()
            if not resumen.get("la matriz del memory es"):
                match = re.search(r"la matriz del memory es\s+(\d+x\d+)", linea.lower())
                if match:
                    resumen["la matriz del memory es"] = match.group(1)

        df_resumen = pd.DataFrame([{
            "codigo": resumen.get("codigo del paciente"),
            "fecha": resumen.get("fecha de registro"),
            "nivel": resumen.get("nivel actual"),
            "bonus": resumen.get("partida de bonus"),
            "aciertos": resumen.get("aciertos"),
            "errores": resumen.get("errores"),
            "matriz": resumen.get("la matriz del memory es"),
            **{f"estimulo_{i+1}": estimulos[i] for i in range(len(estimulos))},
            **{f"posicion_{i+1}": posiciones[i] for i in range(len(posiciones))}
        }])

        tabla_data = [line.strip() for line in lineas[tabla_inicio:] if line.strip()]

        matriz_size = resumen.get("la matriz del memory es", "0x0")
        try:
            cols, rows = map(int, matriz_size.lower().split("x"))
            matriz_len = cols * rows
        except:
            matriz_len = 0

        columnas = ["tiempo", "x", "y", "matriz_vista", "matriz_estado"]
        tracking_filas = []
        for row in tabla_data:
            partes = row.split(";")
            if len(partes) >= (3 + 2 * matriz_len):
                tiempo, x, y = partes[0], partes[1], partes[2]
                matriz_vista = "-".join(partes[3:3 + matriz_len])
                matriz_estado = "-".join(partes[3 + matriz_len:3 + 2 * matriz_len])
                tracking_filas.append([tiempo, x, y, matriz_vista, matriz_estado])

        df_tracking = pd.DataFrame(tracking_filas, columns=columnas)

        nombre_base = os.path.splitext(os.path.basename(self.path_txt))[0]
        fecha = extraer_fecha_desde_lineas(lineas, nombre_base)
        codigo = df_resumen.at[0, "codigo"]

        return guardar_csvs(df_resumen, df_tracking, codigo, fecha, nombre_base, self.root_dir)
