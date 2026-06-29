# Modo de datos congelados para Streamlit Cloud

El modo de datos congelados permite desplegar la landing en Streamlit Community
Cloud sin conectarse a PostgreSQL local. En este modo, la app lee el archivo
`data/final/landing_data.json` y renderiza la misma UI con datos estaticos.

Existe porque Streamlit Cloud no puede conectarse a una base PostgreSQL ubicada
en `localhost`, y no se deben subir exports originales, `.env`, credenciales ni
datos crudos al repositorio.

## Generar el archivo estatico

Ejecutar localmente, con PostgreSQL disponible:

```powershell
python scripts/export_landing_data.py
```

Esto crea:

```text
data/final/landing_data.json
```

## Probar modo estatico localmente

```powershell
$env:USE_STATIC_DATA="true"
streamlit run app/main.py
```

## Probar modo PostgreSQL localmente

```powershell
$env:USE_STATIC_DATA="false"
streamlit run app/main.py
```

## Archivo que debe subirse

```text
data/final/landing_data.json
```

Este archivo puede contener mensajes privados. El repositorio debe ser privado
antes de subirlo si contiene informacion sensible.

## Archivos que no deben subirse

```text
data/raw/
exports originales
.env
credenciales
logs
```

## Configurar Streamlit Cloud

En los secrets de Streamlit Cloud:

```toml
USE_STATIC_DATA = "true"
```

La app tambien acepta la variable de entorno `USE_STATIC_DATA`. Valores como
`true`, `True`, `TRUE`, `1`, `yes` y `y` activan el modo estatico.

## Cuando regenerar landing_data.json

Si cambian mensajes, IDs, metricas o datos, volver a ejecutar:

```powershell
python scripts/export_landing_data.py
```

Despues hacer commit del nuevo `data/final/landing_data.json` y push.

Si solo cambian estilos, CSS o assets, no es necesario regenerar
`landing_data.json`; basta con commit y push de los cambios visuales.

## Comandos de publicacion

```powershell
git add app/main.py services/static_landing_data.py scripts/export_landing_data.py .gitignore docs/deployment_streamlit_static_data.md data/final/landing_data.json
git commit -m "Add static landing data mode"
git push
```
