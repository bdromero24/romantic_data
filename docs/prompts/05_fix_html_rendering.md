# Prompt único para Codex: corregir renderizado de HTML en Streamlit

Actúa como un desarrollador Python/Streamlit senior especializado en renderizado HTML seguro dentro de Streamlit.

La app ya corre correctamente. El error de importación quedó resuelto. Ahora el problema funcional pendiente es que algunas secciones siguen mostrando HTML crudo como texto, en vez de renderizar las tarjetas visuales.

## Contexto

Proyecto:

```text
C:\Users\User\OneDrive\Escritorio\landing_page
```

App:

```text
app/main.py
```

Componentes visuales probables:

```text
ui/components.py
ui/styles.py
```

La app es una landing romántica basada en datos de WhatsApp e Instagram. El backend/ETL ya funciona. No reescribas ETL, queries ni schema de base de datos. Esta tarea es solo para corregir el renderizado HTML de componentes visuales.

---

# Problema actual

En secciones como la línea de tiempo y frases bonitas, la app está mostrando HTML crudo en pantalla.

Ejemplo visible en la UI:

```html
<article class="timeline-card">
    <div class="date-pill">23/04/2026</div>
    <div class="timeline-title">...</div>
    <p class="timeline-detail">...</p>
</article>
```

También ocurre con tarjetas tipo:

```html
<article class="quote-card">
    <p class="quote-text">...</p>
    <div class="quote-sender">...</div>
    <div class="quote-date">...</div>
</article>
```

Esto indica que el HTML se está pasando a Streamlit con un método incorrecto, probablemente:

```python
st.write(html)
st.code(html)
st.text(html)
st.caption(html)
st.container().write(html)
```

o se está retornando como string desde una función de componentes pero luego se imprime sin `unsafe_allow_html=True`.

---

# Objetivo

Corregir todas las secciones donde el HTML aparece como texto plano para que las tarjetas se rendericen visualmente.

El resultado debe ser:

- las cards deben verse como tarjetas, no como código;
- no debe aparecer texto crudo con `<article>`, `<div>`, `<p>`, `<section>`, etc.;
- se deben conservar los estilos románticos existentes;
- se debe mantener el diseño glassmorphism, fucsia, rosa y tarjetas redondeadas;
- no se debe romper la app.

---

# Regla técnica principal

Todo HTML visual debe renderizarse con:

```python
st.markdown(html, unsafe_allow_html=True)
```

No usar para HTML visual:

```python
st.write(html)
st.code(html)
st.text(html)
st.caption(html)
```

---

# Tarea obligatoria

## 1. Buscar HTML generado como string

Inspeccionar especialmente:

```text
app/main.py
ui/components.py
ui/styles.py
```

y cualquier otro archivo que contenga:

```text
<article
<section
<div class=
<p class=
timeline-card
quote-card
special-message-card
bento-card
metric-card
```

Usar búsquedas tipo:

```powershell
Select-String -Path .\*.py,.\app\*.py,.\ui\*.py -Pattern "<article|<section|<div class=|quote-card|timeline-card|st.write|st.code|st.text" -AllMatches
```

Si el proyecto tiene más carpetas, ampliar búsqueda recursiva:

```powershell
Get-ChildItem -Recurse -Filter *.py | Select-String -Pattern "<article|<section|<div class=|quote-card|timeline-card|st.write|st.code|st.text"
```

---

## 2. Corregir funciones que retornan HTML

Si existen funciones que hacen esto:

```python
def render_timeline(...):
    html = "..."
    return html
```

y luego en `app/main.py` se hace:

```python
st.write(render_timeline(...))
```

cambiar el patrón.

Opción preferida:

```python
def render_timeline(...):
    html = "..."
    st.markdown(html, unsafe_allow_html=True)
```

y en `app/main.py` llamar:

```python
render_timeline(...)
```

sin envolverlo en `st.write`.

Opción aceptable:

```python
html = build_timeline_html(...)
st.markdown(html, unsafe_allow_html=True)
```

pero mantener nombres claros:

- funciones `build_*_html` devuelven string;
- funciones `render_*` renderizan con Streamlit y no devuelven HTML para imprimirlo.

---

## 3. Separar builders y renderers si hace falta

Si la estructura actual mezcla responsabilidades, aplicar esta convención:

```python
def build_timeline_html(items: list[dict]) -> str:
    return "..."

def render_timeline(items: list[dict]) -> None:
    st.markdown(build_timeline_html(items), unsafe_allow_html=True)
```

Lo mismo para:

```python
build_quote_cards_html(...)
render_quote_cards(...)

build_special_message_html(...)
render_special_message(...)

build_bento_metrics_html(...)
render_bento_metrics(...)
```

No es obligatorio crear todos si no existen; solo aplicar donde esté el bug.

---

# Seguridad: escapar contenido dinámico

Todo contenido dinámico proveniente de base de datos debe escaparse con:

```python
from html import escape
```

Ejemplo:

```python
safe_message = escape(str(row.get("message", "")))
safe_sender = escape(str(row.get("sender", "")))
```

No escapar el HTML estructural de las tarjetas; solo los valores dinámicos.

Correcto:

```python
html = f'''
<article class="quote-card">
    <p class="quote-text">"{escape(message)}"</p>
    <div class="quote-sender">{escape(sender)}</div>
</article>
'''
st.markdown(html, unsafe_allow_html=True)
```

Incorrecto:

```python
st.markdown(escape(html), unsafe_allow_html=True)
```

porque eso volvería a mostrar HTML como texto.

---

# Corrección específica para timeline

La sección "Lo que marcó nuestra historia" debe renderizar sus tarjetas.

Si actualmente se genera algo como:

```python
timeline_html = "".join(...)
st.write(timeline_html)
```

cambiar a:

```python
st.markdown(timeline_html, unsafe_allow_html=True)
```

o moverlo a:

```python
render_timeline(timeline_items)
```

La salida visual debe mostrar tarjetas, no código.

---

# Corrección específica para frases bonitas

La sección de frases bonitas debe renderizar sus tarjetas.

Si actualmente se genera algo como:

```python
quotes_html = "".join(...)
st.code(quotes_html)
```

o:

```python
st.write(quotes_html)
```

cambiar a:

```python
st.markdown(quotes_html, unsafe_allow_html=True)
```

La salida visual debe mostrar tarjetas con:

- mensaje;
- remitente;
- fecha.

No debe aparecer HTML crudo.

---

# Corrección específica para mensaje especial

Verificar que `render_special_message(...)` también use:

```python
st.markdown(html, unsafe_allow_html=True)
```

No debe retornar HTML para que luego otro archivo lo imprima con `st.write`.

---

# Validación funcional obligatoria

Después de corregir, ejecutar:

```powershell
streamlit run app/main.py
```

Validar visualmente que ya no aparezcan etiquetas como:

```text
<article
<section
<div class=
<p class=
</article>
</section>
```

en la interfaz.

Si se usa Playwright o screenshot validation, validar que las secciones:

- "Lo que marcó nuestra historia"
- "Frases bonitas"
- "Mensaje especial"

muestren cards reales.

---

# Documentación obligatoria

Actualizar o crear:

```text
docs/codex_session_debug.md
```

Agregar una sección nueva:

```md
## Bug 4: HTML renderizado como texto plano en tarjetas

### Síntoma

La app mostraba bloques HTML crudos en pantalla, por ejemplo `<article class="timeline-card">`.

### Causa raíz

Indicar exactamente la causa encontrada:
- uso de `st.write`;
- uso de `st.code`;
- función `render_*` devolvía string HTML;
- `app/main.py` imprimía HTML sin `unsafe_allow_html=True`;
- otra causa real.

### Archivos afectados

Listar rutas relativas.

### Corrección aplicada

Describir brevemente la corrección:
- se reemplazó `st.write(html)` por `st.markdown(html, unsafe_allow_html=True)`;
- se separaron funciones `build_*_html` y `render_*`;
- se escapó contenido dinámico con `html.escape`;
- etc.

### Verificación

Indicar comandos o revisión visual ejecutada.

### Resultado

Indicar si ya no se ve HTML crudo en:
- timeline;
- frases bonitas;
- mensaje especial.
```

Si `docs/codex_session_debug.md` ya existe, no reemplazarlo entero sin necesidad. Agregar la sección del bug nuevo manteniendo el contenido anterior.

---

# Restricciones

No reescribir el ETL.

No cambiar el schema de base de datos.

No cambiar queries salvo que sea estrictamente necesario para construir datos de las tarjetas.

No eliminar estilos románticos existentes.

No volver a dark mode.

No exponer NLP técnico.

No renderizar HTML como texto plano.

No usar `st.write`, `st.code`, `st.text` ni `st.caption` para bloques HTML visuales.

No escapar el HTML completo de la tarjeta; solo escapar los valores dinámicos.

No decir que está corregido sin verificar la interfaz o sin revisar que ya no haya uso incorrecto de `st.write(html)`.

---

# Formato de respuesta esperado

Devuelve únicamente:

1. Rutas de archivos modificados.
2. Contenido completo de cada archivo modificado.
3. Contenido actualizado de `docs/codex_session_debug.md`.

No agregues explicaciones adicionales fuera de los archivos.
