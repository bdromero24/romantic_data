# Prompt para Codex — modo de datos congelados para desplegar Streamlit sin PostgreSQL local

Necesito implementar un **modo de datos congelados** para desplegar mi landing romántica en **Streamlit Community Cloud** sin depender de PostgreSQL local.

Actualmente la app funciona localmente porque consulta PostgreSQL en `localhost`, pero en Streamlit Cloud falla porque esa base local no existe en la nube. La opción que quiero implementar es generar localmente un archivo final con el estado actual de la landing y que Streamlit Cloud lea ese archivo estático.

---

## Objetivo general

Agregar soporte para dos modos de ejecución:

1. **Modo desarrollo/local con PostgreSQL**  
   La app mantiene el comportamiento actual: consulta la base local/remota usando las funciones existentes.

2. **Modo producción/cloud con datos congelados**  
   La app carga un archivo:

```text
data/final/landing_data.json
```

Ese archivo debe contener todas las métricas y datos necesarios para renderizar la landing sin conectarse a PostgreSQL.

---

## Contexto del proyecto

El proyecto es una landing romántica en Streamlit basada en conversaciones de WhatsApp e Instagram.

La app tiene capas separadas:

```text
app/        -> entrypoint Streamlit
services/   -> construcción de métricas y datos románticos
db/         -> queries y conexión PostgreSQL
etl/        -> extracción, transformación y carga
ui/         -> componentes visuales, estilos, gráficos y assets
```

La UI ya está prácticamente terminada. No quiero rediseñar nada visualmente.

---

## Problema actual

En local, la app funciona porque puede hacer consultas a PostgreSQL.

En Streamlit Cloud, la app falla porque:

- la base está en `localhost`;
- la carpeta `data/raw` no se sube a GitHub;
- no quiero subir exports originales de WhatsApp/Instagram;
- no quiero depender de una DB remota para esta versión final;
- la landing no va a cambiar constantemente.

Por eso quiero congelar el estado actual de la página en un JSON final.

---

## Requerimiento 1 — Crear script exportador

Crear un script:

```text
scripts/export_landing_data.py
```

Este script debe ejecutarse **localmente**, donde sí existe PostgreSQL y donde la app funciona.

Debe hacer lo siguiente:

1. Importar la función actual que construye los datos completos de la landing. Probablemente sea algo como:

```python
get_romantic_landing_metrics()
```

2. Ejecutar esa función usando la configuración local actual.

3. Convertir el resultado a JSON serializable.

4. Manejar correctamente tipos no serializables como:

```text
datetime
date
time
Decimal
pandas.Timestamp
numpy int/float
otros tipos comunes usados por métricas o gráficos
```

5. Crear la carpeta si no existe:

```text
data/final/
```

6. Guardar el archivo final en:

```text
data/final/landing_data.json
```

7. Imprimir por consola una confirmación clara, por ejemplo:

```text
Static landing data exported to data/final/landing_data.json
```

8. Si ocurre un error, debe mostrar/loguear un mensaje claro sin ocultar completamente el traceback durante ejecución local.

---

## Requerimiento 2 — Crear helper para cargar datos estáticos

Crear un módulo:

```text
services/static_landing_data.py
```

Debe exponer una función:

```python
load_static_landing_data(path: str | None = None) -> dict
```

La función debe:

1. Usar por defecto:

```text
data/final/landing_data.json
```

2. Resolver la ruta de forma robusta desde la raíz del proyecto, no desde el working directory accidental.

3. Validar que el archivo exista.

4. Cargar el JSON con `json.load()`.

5. Devolver el mismo tipo de estructura/dict que espera actualmente la UI.

6. Lanzar un error claro si el archivo no existe, por ejemplo:

```text
Static landing data file not found. Run: python scripts/export_landing_data.py
```

---

## Requerimiento 3 — Modificar el entrypoint Streamlit

Modificar el entrypoint principal de Streamlit, probablemente:

```text
app/main.py
```

para soportar los dos modos.

### Lógica esperada

Si `USE_STATIC_DATA=true`, entonces:

- cargar datos desde `data/final/landing_data.json`;
- NO conectarse a PostgreSQL;
- NO ejecutar queries;
- renderizar la landing usando exactamente los mismos componentes visuales existentes.

Si `USE_STATIC_DATA=false` o no existe, entonces:

- mantener el comportamiento actual con PostgreSQL;
- no romper el flujo local existente.

### Prioridad de lectura de configuración

Leer `USE_STATIC_DATA` con esta prioridad:

1. `st.secrets` si existe;
2. variable de entorno `os.getenv("USE_STATIC_DATA")`;
3. valor por defecto `false`.

Debe aceptar valores como:

```text
true
True
TRUE
1
yes
y
```

como verdadero.

Debe aceptar valores como:

```text
false
False
FALSE
0
no
n
```

como falso.

---

## Requerimiento 4 — Mantener la UI intacta

No cambiar visualmente la landing.

No tocar:

- estilos generales;
- cards;
- gráficos;
- pergaminos;
- fresa/corazón 8-bit;
- textos;
- layout;
- animaciones;
- tipografías;
- IDs manuales;
- `content_config.py`, salvo que sea absolutamente necesario.

El único objetivo es cambiar la fuente de datos cuando el modo estático esté activo.

---

## Requerimiento 5 — Ajustar `.gitignore`

Revisar `.gitignore` para que siga ignorando datos sensibles, pero permita subir el archivo congelado final.

Debe seguir ignorando:

```text
.env
.env.*
data/raw/
data/staging/
data/processed/
exports originales de WhatsApp
exports originales de Instagram
*.parquet
*.csv
*.xlsx
*.zip
*.rar
logs/
*.log
```

Pero debe permitir subir:

```text
data/final/landing_data.json
```

Si actualmente se ignora toda la carpeta `data/`, corregirlo con reglas específicas para permitir `data/final/landing_data.json`.

Ejemplo de intención:

```gitignore
data/raw/
data/staging/
data/processed/

!data/final/
!data/final/landing_data.json
```

Ajustar según la estructura real del `.gitignore` actual.

---

## Requerimiento 6 — Documentación

Crear documentación:

```text
docs/deployment_streamlit_static_data.md
```

Debe explicar claramente:

1. Qué es el modo de datos congelados.
2. Por qué existe: Streamlit Cloud no puede conectarse a PostgreSQL local.
3. Cómo generar el archivo:

```powershell
python scripts/export_landing_data.py
```

4. Cómo probar localmente el modo estático en PowerShell:

```powershell
$env:USE_STATIC_DATA="true"
streamlit run app/main.py
```

5. Cómo probar localmente el modo PostgreSQL:

```powershell
$env:USE_STATIC_DATA="false"
streamlit run app/main.py
```

6. Qué archivo debe subirse a GitHub:

```text
data/final/landing_data.json
```

7. Qué archivos NO deben subirse:

```text
data/raw/
exports originales
.env
credenciales
logs
```

8. Cómo configurar Streamlit Cloud:

```toml
USE_STATIC_DATA = "true"
```

9. Qué hacer si se cambian mensajes, IDs, métricas o datos:

```text
Volver a ejecutar scripts/export_landing_data.py, hacer commit del nuevo landing_data.json y hacer push.
```

10. Qué hacer si solo se cambian estilos/CSS/assets:

```text
No es necesario regenerar landing_data.json; basta con commit y push de los cambios visuales.
```

---

## Requerimiento 7 — Nota en debug/changelog si existe

Si existe alguno de estos archivos:

```text
docs/codex_session_debug.md
docs/changelog.md
docs/sessions/
```

agregar una nota corta indicando:

```text
Se agregó modo de datos congelados para despliegue en Streamlit Cloud sin PostgreSQL local.
```

No crear documentación duplicada innecesaria si ya existe un patrón de documentación en el proyecto.

---

## Requerimiento 8 — Validaciones locales

Después de implementar, indicar comandos de validación.

Como mínimo:

```powershell
python scripts/export_landing_data.py
$env:USE_STATIC_DATA="true"
streamlit run app/main.py
```

Si existen tests, ejecutar o indicar:

```powershell
pytest tests/
```

Si no se pueden ejecutar, explicar brevemente por qué.

---

## Requerimiento 9 — Seguridad y privacidad

No subir datos crudos.

No subir `.env`.

No subir exports originales.

No subir credenciales.

Advertir si `landing_data.json` contiene mensajes privados y recomendar que el repositorio sea privado antes de subirlo.

No imprimir secretos en consola.

No exponer `DATABASE_URL` en UI ni logs públicos.

---

## Entregable esperado

Devuélveme:

1. Lista de archivos creados/modificados.
2. Código completo por archivo modificado o creado.
3. Explicación breve de cómo usarlo.
4. Comandos exactos para:
   - exportar datos;
   - probar modo estático;
   - subir a GitHub;
   - configurar Streamlit Cloud.
5. No rediseñar la landing.
6. No cambiar lógica visual.
7. No modificar mensajes manuales ni IDs parametrizados.
8. debe estar funcionando la landing page en la url actual que ofrece streamlit que es, https://nuestr4historia.streamlit.app. Esta url está conectada al repositorio de github pero si es necesario subir mas archivos al repositorio, se subiran.

---

## Resultado esperado final

Después del cambio, el flujo debe ser:

```text
Local:
PostgreSQL local funcionando
        ↓
python scripts/export_landing_data.py
        ↓
data/final/landing_data.json
        ↓
git add data/final/landing_data.json + cambios de código
        ↓
git commit && git push
        ↓
Streamlit Cloud con USE_STATIC_DATA=true
        ↓
La app carga sin conectarse a PostgreSQL
```

La landing debe verse igual que local, pero usando el JSON congelado.
