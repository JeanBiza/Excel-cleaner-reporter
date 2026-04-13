# Excel Cleaner & Reporter

Herramienta de automatización en Python que limpia archivos Excel y CSV con datos sucios, normaliza su contenido automáticamente y genera un reporte PDF con estadísticas y gráficos de distribución.

## Características

- 🔍 **Detección automática de tipos** — identifica fechas, RUTs, teléfonos, emails, precios y texto sin configuración manual
- 🧼 **Limpieza automática** — elimina duplicados, filas vacías y normaliza cada columna según su tipo
- 📊 **Reporte PDF** — genera un reporte con tabla de nulos y gráficos de distribución por columna numérica
- 📝 **Log de cambios** — registra en un `.txt` cuántos duplicados y filas vacías se eliminaron
- 📁 **Soporte múltiple** — procesa archivos `.xlsx` y `.csv`, uno o varios a la vez

## ¿Qué normaliza?

| Tipo detectado | Qué hace |
|---|---|
| **Texto** | Elimina espacios extra, aplica Title Case |
| **Fecha** | Estandariza al formato `YYYY-MM-DD` (soporta +15 formatos) |
| **RUT** | Estandariza al formato `XX.XXX.XXX-X` |
| **Teléfono** | Estandariza al formato `+569XXXXXXXX` |
| **Email** | Convierte a minúsculas y elimina espacios |
| **Precio** | Limpia símbolos ($, CLP, USD) y convierte a float |

## Estructura del proyecto

```
Excel-Cleaner-Reporter/
├── cleaner.py      # Detección automática y normalización de datos
├── reporter.py     # Generación del reporte PDF
├── main.py         # Script principal, orquesta todo
├── input/          # Coloca aquí tus archivos Excel o CSV
├── output/         # Aquí se generan los archivos limpios, logs y PDFs
└── requirements.txt
```

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/JeanBiza/Excel-Cleaner-Reporter.git
cd Excel-Cleaner-Reporter
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

## Uso

1. Coloca tu archivo `.xlsx` o `.csv` en la carpeta `input/`
2. Ejecuta el script:

```bash
python main.py
```

3. Si hay múltiples archivos, el programa te pregunta cuál procesar (o todos con `0`)
4. En `output/` encontrarás:
   - `clean_NombreArchivo.xlsx` → Excel limpio
   - `log_NombreArchivo.txt` → resumen de cambios
   - `Report_NombreArchivo.pdf` → reporte con estadísticas y gráficos

## Ejemplo de output

**Log generado:**
```
Archivo: clientes.xlsx
Filas originales: 100
Duplicados eliminados: 14
Filas vacías eliminadas: 5
Filas finales: 81
```

**Reporte PDF incluye:**
- Resumen de estadísticas del proceso
- Tabla de completitud por columna (% de datos no nulos)
- Histogramas de distribución por columna numérica

## Dependencias

```
pandas
openpyxl
reportlab
matplotlib
```

## Autor

Jean — [@JeanBiza](https://github.com/JeanBiza)