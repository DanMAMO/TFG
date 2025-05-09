# 🧠 Proyecto TFG - Procesamiento de Informes Cognitivos

Este proyecto permite procesar automáticamente informes en formato `.txt` generados por distintas tareas de evaluación cognitiva: **Galería de tiro**, **Memory**, **Topos**, **Caminos**, **Aventuras**, y **Resumen de Usuario**. Extrae información clave y genera uno o dos archivos `.csv` por cada informe, además de un análisis exploratorio (EDA) empaquetado para su importación en Power BI.

---

## 📁 Estructura del Proyecto

````
TFG/
├── data/
├── outputs/
│   ├── pacientes/{codigo}/{año}/{mes}/        # CSVs de resumen y tracking
│   └── eda/                                   # EDA completo (Excel + gráfico)
├── src/
│   ├── aventuras/
│   ├── base/
│   ├── caminos/
│   ├── galeria/
│   ├── memory/
│   ├── pruebas/
│   ├── topos/
│   ├── usuario/
│   ├── utils/
│   ├── analysis/                              # Script de EDA
│   └── main.py
└── README.md
````

---

## 🚀 Uso

### Modo manual
```bash
python src/main.py --manual
````

* Abre un selector de archivos.
* Detecta automáticamente el tipo de informe.
* Procesa y genera los `.csv` de salida.

### Modo batch (procesamiento masivo)

```bash
python src/main.py
```

* Recorre automáticamente todos los `.txt` en `data/galeria`, `data/memory`, `data/topos`, `data/caminos`, `data/aventuras` y `data/pacientes`.
* Procesa cada uno y los guarda organizadamente en `outputs/pacientes/...`.

### Limpieza de carpetas y archivos vacíos

**Nota de seguridad:** solo se permiten limpiar estas carpetas dentro del proyecto:

- `data/`  
- `outputs/`  
- `outputs/eda/`  

Cualquier otra ruta será rechazada.

- `--clean-data` → limpia `data/`  
- `--clean-outputs` → limpia `outputs/`  
- `--clean-eda` → limpia `outputs/eda/`  
- `--remove-empty` → borra archivos de tamaño 0 en `data/` y `outputs/`


---

## ✅ Informes soportados

### 👤 Resumen de Usuario

Detectado por:

* Nombre del archivo tipo `Paciente000.txt`
* Contenido JSON que contenga `"nombre"` y `"codigo"`

### 🎯 Galería de tiro

Detectado por:

* Nombre del archivo o
* Contenido que incluya `galeria de tiro`

### 🧠 Memory

Detectado por:

* Nombre del archivo o
* Contenido que incluya `memory`

### 🕳️ Topos

Detectado por:

* Nombre del archivo o
* Contenido que incluya `tarea de topos`

### 🧭 Caminos

Detectado por:

* Nombre del archivo o
* Contenido que incluya `tarea de caminos`

### 🗺️ Aventuras

Detectado por:

* Nombre del archivo o
* Contenido que incluya `tarea de aventuras`

---

## 📄 Formato de Salida

### `resumen_usuario_*.csv`

Contiene:

* `nombre`, `codigo`, `esZurdo`, niveles y puntuaciones por tarea
* Sumatorios como `nivelesRecordMemory`, `medallasTotalesMemory`
* `multiplicadorVelocidad`
* `fecha_generacion` y `fecha_formateada` del momento de procesado

Se guarda en:

```
outputs/pacientes/{codigo}/resumen_usuario_{nombre}_{dd-mm-yyyy}.csv
```

### `*_resumen.csv`

Contiene:

* `codigo`, `fecha`, `fecha_num`
* Datos relevantes: `nivel`, `aciertos`, `errores`, `omisiones`, `puntuacion`
* Variables específicas del juego (estímulos, posiciones, matriz, etc.)

### `*_tracking.csv`

Contiene:

* `tiempo`, `x`, `y`, y otras variables según el juego
* En **Caminos**, incluye posiciones fijas de las tarjetas por fila
* En **Aventuras**, cada par de coordenadas de `item` y `peligro` en columnas separadas

---

## 🧪 Análisis Exploratorio (EDA)

En `src/analysis/eda.py` hay un script que:

1. Carga todos los `*_resumen.csv` desde `outputs/pacientes/`.
2. Genera un **Excel** `EDA_completo_{timestamp}.xlsx` con tres hojas:

   * **DatosCrudos**: combinación de todos los resúmenes
   * **Descriptivos**: estadísticas (`count`, `mean`, `std`, `min`, percentiles, `max`)
   * **MediaPuntuacion**: tabla con las puntuaciones de cada paciente en cada juego, extraídas del CSV resumen_usuario_*.csv (columnas Topos, Memory, Galería, Aventuras, Caminos).
   
3. Todos los resultados se almacenan en:

```
outputs/eda/
└── EDA_completo_{timestamp}.xlsx
```

### Uso

```bash
pip install pandas openpyxl
python src/analysis/eda.py
```

---

## 🛠️ Dependencias
- Python 3.10+  
- pandas   
- openpyxl  



---

## ✅ Buenas prácticas del proyecto

* Mantener módulos por tarea en carpetas independientes (`galeria`, `memory`, etc.)
* Reutilizar funciones comunes desde `utils/helpers.py`
* Probar primero en modo manual antes de ejecutar en batch
* No versionar archivos de salida (`outputs/`, `eda/`, CSVs, PNGs) ni datos de prueba (`data/`)
* Documentar cada nueva tarea o modificación importante en este README
