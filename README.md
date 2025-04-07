# README.md
"""
# TFG - Procesamiento de Informes por Juego

Este proyecto procesa informes de tareas cognitivas por paciente y juego, extrayendo datos clave y organizando los resultados automáticamente.

## 📁 Estructura del Proyecto

```
TFG/
├── src/
│   ├── galeria/
│   │   └── procesador.py         # Procesamiento específico para galería de tiro
│   ├── utils/
│   │   └── helpers.py            # Funciones comunes: fecha, guardado, nombrado
│   └── main.py                  # Ejecuta procesamiento en lote
├── data/
│   └── galeria_tiro/           # Archivos .txt crudos por paciente
├── outputs/
│   └── pacientes/...           # Resultados CSV organizados por paciente/año/mes
├── .gitignore
└── README.md
```

## ⚙️ Cómo usar

### Modo BATCH (varios archivos automáticamente):

1. Colocá archivos `.txt` en `data/galeria_tiro/`
2. Ejecutá:

```bash
python src/main.py
```

### Modo MANUAL (archivo único con selector visual):

```bash
python src/main.py --manual
```

Se generarán `.csv` por cada informe en:

```
outputs/pacientes/{codigo}/{año}/{mes}/
```

## ✅ Funcionalidades

- Extrae resumen y tracking frame a frame
- Genera CSVs automáticamente con nombre único
- Detecta fecha desde el nombre del archivo
- Organiza resultados de forma escalable
- Modo dual: automático o manual

"""