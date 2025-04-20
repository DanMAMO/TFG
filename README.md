# 🧠 Proyecto TFG - Procesamiento de Informes Cognitivos

Este proyecto permite procesar automáticamente informes en formato `.txt` generados por distintas tareas de evaluación cognitiva: **Galería de tiro**, **Memory**, y **Topos**. Extrae información clave y genera dos archivos `.csv` por cada informe:

- `*_resumen.csv`: con metadatos relevantes del paciente y la tarea
- `*_tracking.csv`: con los datos frame a frame del desarrollo de la tarea

---

## 📁 Estructura del Proyecto
```
TFG/
├── data/
│   ├── galeria/
│   ├── memory/
│   └── topos/
├── outputs/
│   └── pacientes/{codigo}/{año}/{mes}/
├── src/
│   ├── galeria/
│   ├── memory/
│   ├── topos/
│   ├── base/
│   ├── utils/
│   └── main.py
└── README.md
```

---

## 🚀 Uso

### Modo manual
```bash
python src/main.py --manual
```
- Abre un selector de archivos.
- Detecta automáticamente el tipo de juego en el `.txt`.
- Procesa y genera dos `.csv` de salida.

### Modo batch (procesamiento masivo)
```bash
python src/main.py
```
- Recorre automáticamente todos los `.txt` en `data/galeria`, `data/memory`, y `data/topos`
- Procesa cada uno y los guarda organizadamente en `outputs/pacientes/...`

---

## ✅ Juegos soportados

### 🎯 Galería de tiro
Detectado por:
- Nombre del archivo o
- Contenido que incluya `galeria de tiro`

### 🧠 Memory
Detectado por:
- Nombre del archivo o
- Contenido que incluya `memory`

### 🕳️ Topos
Detectado por:
- Nombre del archivo o
- Contenido que incluya `tarea de topos`

---

## 📄 Formato de Salida

### `*_resumen.csv`
Contiene:
- `codigo`, `fecha`, `fecha_num`
- Datos relevantes como `nivel`, `aciertos`, `errores`, etc.
- Variables específicas del juego (estimulos, posiciones, matriz, etc.)

### `*_tracking.csv`
Contiene:
- `tiempo`, `x`, `y`, `estimulo_objetivo`, `matriz_estado`, etc.
- En formato estructurado y ordenado

---

## 🛠️ Dependencias
- Python 3.10+
- pandas

Instalación:
```bash
pip install -r requirements.txt
```

---

## 🔧 Notas de desarrollo
- Las fechas se normalizan al formato `dd.mm.yyyy` (`fecha_num`)
- Las matrices del estado de tareas se representan en una sola columna (`matriz_estado`) como una cadena unificada separada por `-`
- Las clases de cada juego heredan de una base común `InformeBase`
- Se pueden agregar más tareas creando nuevos módulos similares

---

## ✅ Buenas prácticas del proyecto

- Mantener los módulos por tarea en carpetas independientes (`galeria`, `memory`, `topos`, etc.)
- Reutilizar funciones comunes desde `utils/helpers.py`
- Usar nombres de archivo descriptivos para los `.txt`
- No versionar archivos de salida ni temporales. Asegurarse que en `.gitignore` esté:
  ```
  /outputs
  *.csv
  *.zip
  ```
- Probar primero en modo manual antes de ejecutar en batch
- Documentar cada nueva tarea o modificación importante en este README

