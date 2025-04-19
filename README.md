# README.md

# TFG - Procesador de Informes Cognitivos

Este proyecto automatiza el procesamiento de archivos `.txt` generados por distintos juegos cognitivos, extrayendo datos relevantes y generando informes `.csv` organizados por paciente, año y mes.

---

## 📂 Estructura del Proyecto

```
TFG/
├── src/
│   ├── base/                   # Clase base común para todos los informes
│   │   └── informe_base.py
│   ├── galeria/               # Procesamiento para juego Galería de tiro
│   │   └── procesar.py
│   ├── memory/                # Procesamiento para juego Memory
│   │   └── procesar.py
│   ├── utils/                 # Utilidades generales
│   │   └── helpers.py
│   └── main.py                # Entrada principal para ejecutar todo
├── data/
│   ├── galeria/               # Archivos .txt de Galería
│   └── memory/                # Archivos .txt de Memory
├── outputs/                   # Resultados exportados por paciente/año/mes
└── README.md
```

---

## ▶️ Cómo ejecutar

### ✅ Modo BATCH (procesar todo lo que haya en `data/*/`):

```bash
python src/main.py
```

### ✅ Modo MANUAL (elegir archivo con ventana):

```bash
python src/main.py --manual
```

El sistema detectará automáticamente el tipo de informe según el **nombre de la carpeta** o el **contenido del archivo** (por ejemplo: "Tarea de memory").

---

## 📄 Qué genera

Por cada informe procesado, se generan dos archivos CSV:

- `*_resumen.csv` → con los datos globales del informe
- `*_tracking.csv` → con el seguimiento frame a frame

Ubicados en:

```
outputs/pacientes/{codigo}/{año}/{mes}/
```

Los nombres de archivo se guardan con separador `;` y evitan sobrescritura (`v2`, `v3`, ...).

---

## 🎮 Juegos soportados actualmente

- 🟢 **Galería de tiro** (`galeria/`)
- 🟢 **Memory** (`memory/`)

Más juegos como "Topos" y "Secuencia" pueden añadirse fácilmente gracias a la arquitectura modular basada en herencia (`InformeBase`).

---

## 🧠 Dependencias

- Python 3.8+
- pandas

Instalación:
```bash
pip install pandas
```

---

## ✅ Buenas prácticas

- No versionar la carpeta `outputs/`: ya está ignorada vía `.gitignore`
- Usar ramas como `juegos` para desarrollo e integración progresiva de nuevos módulos
- Agregar una nueva clase hija en su carpeta (`src/{juego}/procesar.py`) y conectarla en `main.py`

---

¿Listo para añadir más juegos o exportar a Excel? Este proyecto lo permite sin romper la arquitectura 💪
