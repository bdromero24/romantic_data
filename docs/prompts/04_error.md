# Fix Streamlit import error and Playwright visual validation

Actúa como un desarrollador Python/Streamlit senior.

La app está fallando por un error de importación y además la validación visual con Playwright no se ejecuta correctamente aunque Playwright ya funciona cuando se prueba directamente.

## Contexto

La app es una landing romántica hecha en Streamlit. El backend/ETL ya funciona. No reescribas el ETL ni cambies la lógica de base de datos salvo que sea estrictamente necesario para corregir los errores actuales.

Actualmente aparece este error al ejecutar Streamlit:

```text
ImportError: cannot import name 'render_special_message' from 'ui.components'
(C:\Users\User\OneDrive\Escritorio\landing_page\ui\components.py)
```

El traceback indica que `app/main.py` está importando `render_special_message` desde `ui.components`, pero esa función no existe o no está exportada correctamente en `ui/components.py`.

También aparece este mensaje:

```text
Validación visual con Playwright no ejecutada: falta Chrome en:
C:\Users\User\AppData\Local\Google\Chrome\Application\chrome.exe
```

Sin embargo, Playwright sí funciona correctamente cuando se ejecuta una prueba directa con Chromium. Por tanto, el problema no es Playwright, sino que algún script de validación visual está buscando Google Chrome en una ruta hardcodeada.

---

# Objetivo

Corregir ambos problemas:

1. La app debe ejecutar sin fallar por `ImportError`.
2. La validación visual debe usar Chromium administrado por Playwright por defecto.
3. No debe exigir Google Chrome instalado en una ruta local de Windows.
4. La validación visual debe ser opcional y nunca debe bloquear la ejecución de la app Streamlit.

---

# Parte 1: corregir `render_special_message`

## Problema

`app/main.py` importa:

```python
from ui.components import (
    ...
    render_special_message,
)
```

Pero `ui/components.py` no define una función llamada `render_special_message`.

## Tarea

1. Inspeccionar `app/main.py`.
2. Inspeccionar `ui/components.py`.
3. Corregir el mismatch entre imports y funciones disponibles.
4. Preferir agregar una función `render_special_message(...)` en `ui/components.py` si no existe.
5. Asegurar que `app/main.py` importe únicamente funciones existentes.
6. No eliminar componentes visuales existentes si pueden reutilizarse.

## Requerimientos de `render_special_message`

La función debe renderizar una tarjeta destacada para un mensaje especial parametrizable.

Firma sugerida:

```python
def render_special_message(
    message: dict | None,
    title: str = "Un mensaje que quiero guardar",
    subtitle: str = "Hay palabras que merecen quedarse aquí.",
) -> None:
    ...
```

Debe aceptar un diccionario o registro con al menos:

```python
{
    "message": "...",
    "sender": "...",
    "timestamp": ...
}
```

Debe mostrar:

* título;
* subtítulo;
* mensaje original;
* remitente;
* fecha;
* diseño destacado;
* clases CSS románticas existentes si están disponibles.

Clases sugeridas:

```text
special-message-card
quote-card
quote-card-featured
glitter-accent
glossy-card-highlight
```

## Regla crítica de HTML

No renderizar HTML como texto plano.

No usar:

```python
st.write(html)
st.code(html)
```

para bloques visuales HTML.

Usar siempre:

```python
st.markdown(html, unsafe_allow_html=True)
```

## Escapar contenido dinámico

Todo contenido proveniente de la base de datos debe escaparse para evitar romper el HTML.

Usar:

```python
from html import escape
```

Ejemplo esperado:

```python
safe_message = escape(str(message.get("message", "")))
safe_sender = escape(str(message.get("sender", "")))
```

Si `timestamp` tiene `strftime`, formatearlo como:

```python
timestamp.strftime("%d/%m/%Y")
```

Si no, convertirlo a string escapado.

## Comportamiento si no hay mensaje

Si `message` es `None` o está vacío, la función no debe fallar. Debe renderizar una tarjeta fallback indicando que aún no hay mensaje especial seleccionado.

---

# Parte 2: corregir Playwright visual validation

## Problema

El script de validación visual está buscando Chrome en esta ruta:

```text
C:\Users\User\AppData\Local\Google\Chrome\Application\chrome.exe
```

Eso está mal como dependencia obligatoria.

Playwright ya fue instalado y Chromium funciona cuando se ejecuta una prueba directa. Por tanto, la validación visual debe usar Chromium administrado por Playwright.

## Tarea

1. Buscar el script o módulo que ejecuta la validación visual con Playwright.
2. Eliminar cualquier dependencia obligatoria de esta ruta hardcodeada:

```text
C:\Users\User\AppData\Local\Google\Chrome\Application\chrome.exe
```

3. Usar Playwright-managed Chromium por defecto:

```python
browser = playwright.chromium.launch(headless=True)
```

4. Si se quiere permitir Chrome real, debe ser opcional mediante variable de entorno:

```env
PLAYWRIGHT_CHROME_PATH=
```

5. La lógica correcta debe ser:

```python
chrome_path = os.getenv("PLAYWRIGHT_CHROME_PATH")

if chrome_path and Path(chrome_path).exists():
    browser = playwright.chromium.launch(
        headless=True,
        executable_path=chrome_path,
    )
else:
    browser = playwright.chromium.launch(headless=True)
```

6. No fallar solo porque Google Chrome no esté instalado.
7. No bloquear la app Streamlit si la validación visual no puede ejecutarse.
8. Si Chromium no está instalado, mostrar una instrucción clara:

```bash
python -m pip install playwright
python -m playwright install chromium
```

9. Si Playwright falla, capturar la excepción y mostrar un warning/log controlado, no romper la ejecución principal de Streamlit.

---

# Parte 3: validación esperada

Después de los cambios, deben cumplirse estos puntos:

## Streamlit

La app debe correr con:

```bash
streamlit run app/main.py
```

sin este error:

```text
ImportError: cannot import name 'render_special_message'
```

## Playwright

La validación visual debe funcionar si Chromium de Playwright está instalado.

No debe exigir:

```text
C:\Users\User\AppData\Local\Google\Chrome\Application\chrome.exe
```

## HTML

No debe aparecer HTML crudo visible en pantalla, por ejemplo:

```html
<article class="quote-card">
```

Todo HTML visual debe renderizarse mediante:

```python
st.markdown(html, unsafe_allow_html=True)
```

## Mensaje especial

La app debe poder mostrar una tarjeta especial usando un mensaje parametrizable.

Si existe una configuración como:

```python
SPECIAL_MESSAGE_ID = 39145
```

o:

```python
SPECIAL_MESSAGES = {
    "primer_te_amo": 39145,
    "mensaje_especial": 39145,
}
```

debe mantenerse o integrarse sin romper la app.

---

# Restricciones

No reescribir el ETL.

No cambiar el schema de base de datos.

No eliminar estilos románticos existentes.

No volver a dark mode.

No exponer NLP técnico en la interfaz.

No renderizar HTML como texto plano.

No dejar imports apuntando a funciones inexistentes.

No hardcodear rutas locales de Chrome como requisito obligatorio.

---

# Formato de respuesta esperado

Devuelve únicamente:

* rutas de archivos modificados;
* contenido completo de cada archivo modificado.

No incluyas explicaciones adicionales.
