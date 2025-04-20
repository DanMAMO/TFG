# usuario/procesar.py
import os
import json
import pandas as pd
from base.informe_base import InformeBase
from utils.helpers import generar_nombre_unico, formatear_fecha_ddmmYYYY
from datetime import datetime


class ResumenUsuario(InformeBase):
    def procesar(self):
        with open(self.path_txt, "r", encoding="utf-8") as f:
            datos = json.load(f)

        fecha_actual = datetime.now()
        fecha_str = fecha_actual.strftime("%Y-%m-%d %H:%M:%S")
        fecha_formateada = formatear_fecha_ddmmYYYY(fecha_actual)

        fila = {
            "fecha_generacion": fecha_str,
            "fecha_formateada": fecha_formateada,
            "nombre": datos.get("nombre"),
            "codigo": datos.get("codigo"),
            "esZurdo": datos.get("esZurdo"),
            "ultimoNivelTopos": datos.get("ultimoNivelDesbloqueadoTareaTopos"),
            "ultimoNivelMemory": datos.get("ultimoNivelDesbloqueadoTareaMemory"),
            "ultimoNivelGaleriaTiro": datos.get("ultimoNivelDesbloqueadoTareaGaleriaTiro"),
            "ultimoNivelAventuras": datos.get("ultimoNivelDesbloqueadoTareaAventuras"),
            "ultimoNivelCaminos": datos.get("ultimoNivelDesbloqueadoTareaCaminos"),
            "nivelActualMemory": datos.get("nivelActualTareaMemory"),
            "jugandoNivelBonusMemory": datos.get("jugandoNivelDeBonusTareaMemory"),
            "puntuacionTopos": datos.get("puntuacionTareaTopos"),
            "puntuacionMemory": datos.get("puntuacionTareaMemory"),
            "puntuacionGaleriaTiro": datos.get("puntuacionTareaGaleriaTiro"),
            "puntuacionAventuras": datos.get("puntuacionTareaAventuras"),
            "puntuacionCaminos": datos.get("puntuacionTareaCaminos"),
            "nivelesRecordMemory": sum(datos.get("nivelesConRecordTareaMemory", [])),
            "medallasTotalesMemory": sum(datos.get("medallasTareaMemory", [])),
            "multiplicadorVelocidad": datos.get("multiplicadorVelocidad"),
        }

        df = pd.DataFrame([fila])

        # === GUARDADO ===
        codigo = str(fila["codigo"])
        nombre = str(fila["nombre"]).replace(" ", "_")
        root_dir = self.root_dir

        output_dir = os.path.join(root_dir, "outputs", "pacientes", codigo)
        os.makedirs(output_dir, exist_ok=True)

        nombre_archivo = f"resumen_usuario_{nombre}_{fecha_formateada.replace('.', '-')}.csv"
        ruta_csv = os.path.join(output_dir, nombre_archivo)
        ruta_csv = generar_nombre_unico(ruta_csv)

        df.to_csv(ruta_csv, index=False, sep=";")

        print(f"✅ Resumen de usuario generado: {ruta_csv}")
        return ruta_csv, None  # No hay tracking
