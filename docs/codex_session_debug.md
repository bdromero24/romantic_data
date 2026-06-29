## Modo de datos congelados para Streamlit Cloud

Se agrego modo de datos congelados para despliegue en Streamlit Cloud sin
PostgreSQL local.

## Ajuste final: promedio, KPI conversacion y pergaminos

### Motivo

La landing necesitaba redondear visualmente el promedio diario, ubicar
`Quien prendio mas veces la conversacion` junto a `Hater de tiempo completo`
y hacer que los mensajes destacados se vieran como un unico pergamino.

### Cambio aplicado

- `services/romantic_metrics.py`: `_build_summary_cards()` muestra
  `Promedio diario` con `_format_rounded_number()` y agrega la card de
  conversacion como KPI secundario despues de `Hater de tiempo completo`.
- `app/main.py`: deja de renderizar `render_conversation_starter()` como
  bloque separado para evitar una fila completa.
- `ui/styles.py`: `.scroll-quote-card` usa el PNG del pergamino solo como
  mascara; neutraliza fondo, borde, radio, sombra y blur heredados de
  `.quote-card`.
- `ui/styles.py`: `.scroll-quote-card::before` dibuja la silueta/borde fucsia
  y `::after` dibuja el relleno translucido para eliminar el blanco del asset
  y mantener uniformidad con las demas cards.

### Verificacion

```powershell
.\venv\Scripts\python.exe -m pytest tests/test_ui_components.py tests/test_romantic_metrics.py
```

## Bug 4: HTML renderizado como texto plano en tarjetas

## Ajuste KPIs: tipografia, orden y promedio diario

### Motivo

La seccion `Pequenos datos bonitos` necesitaba priorizar los cards mas
importantes a la izquierda y agregar un KPI de promedio diario. Ademas, los
subtitulos internos del bloque especial debian usar la misma fuente decorativa
del titulo principal y el corazon 8-bit debia quedar sin fondo opaco.

### Cambio aplicado

- `ui/styles.py`: `.special-message-block-title` usa `--font-script` y tamano
  `calc(clamp(1.8rem, 4vw, 2.7rem) - 2px)`.
- `services/romantic_metrics.py`: `_build_summary_cards()` reordena los KPIs
  para priorizar `Mensajes compartidos`, `Primer te amo` y `Mes mas intenso`.
- `db/queries.py`: se agrego `ROMANTIC_AVERAGE_DAILY_MESSAGES_QUERY`.
- `db/romantic_queries.py`: se agrego `fetch_average_daily_messages()`.
- `services/romantic_metrics.py`: se agrego el KPI `Promedio diario`.
- `ui/styles.py`: `.bento-grid` usa `grid-auto-flow: dense` para que cards
  pequenos rellenen la zona derecha en desktop.
- `ui/assets/corazon.png`: se transparento el fondo claro conectado a los
  bordes del PNG.

### Verificacion

```powershell
.\venv\Scripts\python.exe -m pytest tests/test_ui_components.py tests/test_romantic_metrics.py tests/test_romantic_queries.py
```

## Ajuste visual: pergamino por asset y corazon 8-bit

### Motivo

La seccion `Mensajes para volver a leer despacio` debia usar el PNG de
pergamino entregado en la raiz del proyecto como marco/fondo real de cada
mensaje. Los cards relacionados con `Primer te amo` debian mostrar un detalle
de corazon 8-bit sin cambiar la logica de datos.

### Assets

- `perrgamino.png` se movio a `ui/assets/perrgamino.png`.
- `corazon.png` se movio a `ui/assets/corazon.png`.

### Cambio aplicado

- `ui/components.py`: `build_quote_cards_html()` carga el pergamino como
  `data URI` y lo expone por la variable CSS `--scroll-bg-image`.
- `ui/styles.py`: `.scroll-quote-card` usa `--scroll-bg-image` como capa de
  fondo y mantiene gradientes rosa/fucsia para legibilidad.
- `ui/components.py`: `build_metric_cards_html()` y `build_timeline_html()`
  insertan el corazon solo si el label/titulo contiene `Primer te amo`.
- `ui/styles.py`: `.first-te-amo-card` y `.first-te-amo-heart` controlan el
  posicionamiento del ornamento 8-bit.

### Verificacion

```powershell
.\venv\Scripts\python.exe -m pytest tests/test_ui_components.py tests/test_romantic_metrics.py
```

## Ajuste visual: pergaminos romanticos en frases bonitas

### Motivo

La seccion `Mensajes para volver a leer despacio` debia mantener sus 9
mensajes, pero dejar de verse como cards rectangulares normales.

### Cambio aplicado

- `ui/components.py`: las cards de frases bonitas ahora usan
  `quote-card scroll-quote-card`.
- `ui/styles.py`: `.scroll-quote-card` agrega fondo rosado claro,
  bordes fucsia suaves, sombras, textura por gradientes y pseudo-elementos
  `::before` / `::after` para simular extremos de pergamino.
- `ui/styles.py`: `.special-message-block-title` queda en cursiva para los
  subtitulos internos `Cosas bonitas que ella me dijo` y
  `Una conversacion que quiero recordar`.

### Como ajustar el efecto

Editar en `ui/styles.py`:

```css
.scroll-quote-card
.scroll-quote-card::before
.scroll-quote-card::after
```

No requiere assets externos ni cambios en IDs, ETL o queries.

### Verificacion

```powershell
.\venv\Scripts\python.exe -m pytest tests/test_ui_components.py tests/test_romantic_metrics.py
```

## Ajuste bloque especial: titulos internos configurables

### Motivo

La seccion `Un mensaje que quiero guardar` mostraba un encabezado externo
duplicado antes de la card principal: `Frases bonitas`, el titulo de la
seccion y el texto `Me gusta saber lo que sientes.`. Ademas, los subtitulos
internos de los bloques especiales no debian depender de textos hardcodeados.

### Cambio aplicado

- `app/main.py`: se elimino el `render_section_header()` previo a
  `render_special_message()`.
- `app/content_config.py`: los titulos internos se parametrizan en
  `ROMANTIC_CONTENT["special_message"]["blocks"][*]["title"]`.
- `services/romantic_metrics.py`: los titulos vacios se conservan como vacios
  para que no aparezcan defaults.
- `ui/components.py`: cada titulo interno se renderiza solo si existe.
- `ui/styles.py`: `.special-message-block-title` aplica glow fucsia suave con
  `text-shadow`.

### Como ocultar un titulo interno

Dejar el campo vacio:

```python
"title": ""
```

La app no renderiza el titulo ni deja un header vacio.

### Verificacion

```powershell
.\venv\Scripts\python.exe -m pytest tests/test_ui_components.py tests/test_romantic_metrics.py
```

### Sintoma

La app mostraba bloques HTML crudos en pantalla, por ejemplo `<article class="timeline-card">`.

### Causa raiz

En el estado revisado no quedaban llamadas `st.write`, `st.code`, `st.text` ni `st.caption` para las tarjetas visuales de `timeline`, `quotes` o `special_message`. La causa real era que el HTML generado conservaba indentacion de 8 a 12 espacios antes de varias etiquetas; Markdown interpretaba esas lineas como bloques de codigo y Streamlit mostraba etiquetas como `<article>`, `<div class=` y `<p class=` en texto plano. Se dejo explicita la separacion entre builders `build_*_html` y renderers `render_*`, y todos los renderers visuales pasan por `st.markdown(html, unsafe_allow_html=True)` con normalizacion previa.

### Archivos afectados

- `ui/components.py`
- `tests/test_ui_components.py`
- `docs/codex_session_debug.md`

### Correccion aplicada

- Se separaron funciones `build_*_html` y `render_*` para hero, secciones, metricas, timeline, frases bonitas y mensaje especial.
- Se centralizo el renderizado HTML visual en `_render_html`, que usa `st.markdown(html, unsafe_allow_html=True)`.
- Se agrego `_normalize_html` para eliminar indentacion inicial de lineas HTML antes de enviarlas a Markdown.
- Se mantuvo el HTML estructural sin escapar y se escaparon los valores dinamicos con `html.escape`.
- Se agregaron tests para verificar que timeline renderiza con markdown inseguro permitido y que frases bonitas y mensaje especial escapan contenido dinamico.

### Verificacion

- `python -m pytest tests/test_ui_components.py tests/test_streamlit_entrypoint.py`
- `streamlit run app/main.py --server.headless true --server.port 8502`
- Revision visual con Playwright en `http://localhost:8502`: no hubo texto visible con `<article`, `<section`, `<div class=` ni `<p class=`.
- Conteo DOM verificado: 6 `.timeline-card`, 5 `.quote-card`, 1 `.special-message-card`.

### Resultado

Ya no debe verse HTML crudo en:

- timeline;
- frases bonitas;
- mensaje especial.

## Bug 5: Labels visibles usaban texto normalizado sin ñ y mensajes repetidos

### Síntoma

La UI mostraba valores como `te extrano` y podía repetir mensajes como "el primer te amo" en varias secciones visibles: mensaje especial, timeline y frases bonitas.

### Causa raíz

- `services/romantic_metrics.py` definía labels visibles junto a keywords internas y tenía `te extrano` como texto de presentación.
- La selección del mensaje especial y del primer `te amo` estaba hardcodeada en el servicio, sin configuración centralizada.
- La sección de frases bonitas usaba fallback automático sin excluir IDs ya reservados por secciones manuales.
- El timeline no podía mezclar de forma declarativa hitos automáticos y mensajes manuales por ID.

### Archivos afectados

- `app/content_config.py`
- `services/romantic_metrics.py`
- `ui/components.py`
- `tests/test_romantic_metrics.py`
- `tests/test_ui_components.py`
- `docs/content_configuration.md`
- `docs/codex_session_debug.md`

### Corrección aplicada

- Se creó `app/content_config.py` con `DISPLAY_LABELS`, `ROMANTIC_CONTENT`, `get_display_label()` y `get_reserved_message_ids()`.
- Se mapeó `te extrano` a `te extraño` para labels visibles.
- Se parametrizaron `special_message`, `first_te_amo`, `timeline` y `featured_quotes` por `message_id`.
- Se mantuvo `message_normalized` solo para búsquedas, filtros y conteos.
- Se mantuvo `message` como fuente de textos visibles provenientes de la base de datos.
- Se agregó exclusión de IDs reservados en el fallback automático de frases bonitas.
- Se permitió `<strong>...</strong>` solo en textos manuales de configuración, mientras los mensajes de base de datos siguen escapados.

### Verificación

- `.\venv\Scripts\python.exe -m pytest tests/test_romantic_metrics.py tests/test_ui_components.py tests/test_streamlit_entrypoint.py`
- `Get-ChildItem -Recurse -Filter *.py | Select-String -Pattern "message_normalized|extrano|featured_quotes|timeline|special_message|first_te_amo"`
- `Get-ChildItem -Path app,services,ui,db,tests -Recurse -Filter *.py | Select-String -Pattern "message_normalized|extrano|featured_quotes|timeline|special_message|first_te_amo"`

### Resultado

- La UI ya no debe mostrar `te extrano` como label visible.
- Los mensajes manuales se parametrizan desde `app/content_config.py`.
- El primer `te amo` no se repite automáticamente en frases bonitas cuando el fallback está activo.
- Los textos manuales soportan `<strong>...</strong>` de forma controlada.

## Ajuste UX: reordenamiento de la sección "nuestro ritmo"

### Motivo

La sección "nuestro ritmo" contiene gráficos y tiene más peso visual, por lo que debe aparecer después de "pequeños datos bonitos".

### Cambio aplicado

El orden de renderizado se cambió en `app/main.py`.

El nuevo orden es:

1. Hero / portada romántica.
2. Pequeños datos bonitos.
3. Nuestro ritmo / gráficos.
4. Mensaje especial.
5. Lo que marcó nuestra historia / timeline.
6. Frases bonitas.
7. Nuestro lenguaje.
8. Cierre emocional.

### Resultado esperado

La landing presenta primero los elementos grandes y de mayor atención, y luego avanza hacia secciones más pequeñas, narrativas o de lectura pausada.

## Ajuste UX: animaciones reveal-on-scroll

### Motivo

La landing se veia estatica. Se agrego una animacion suave para que las secciones y tarjetas aparezcan hacia arriba al scrollear.

### Tecnica usada

Intersection Observer API + CSS transitions.

### Archivos afectados

- `app/main.py`
- `ui/components.py`
- `ui/charts.py`
- `ui/styles.py`
- `tests/test_ui_components.py`
- `docs/codex_session_debug.md`
- `docs/content_configuration.md`
- `docs/sessions/11_reveal_on_scroll_20260612.md`

### Como funciona

- La clase `reveal-on-scroll` deja cada bloque en estado inicial con `opacity: 0` y `transform: translateY(28px)`.
- La clase `is-visible` se agrega por JavaScript cuando el elemento entra al viewport y activa `opacity: 1` y `transform: translateY(0)`.
- La variable CSS `--reveal-delay` permite escalonar cards repetidas sin crear clases adicionales.
- El media query `prefers-reduced-motion: reduce` desactiva transiciones y deja los elementos visibles.

### Como activar la animacion en nuevas tarjetas

Agregar:

```html
class="reveal-on-scroll"
```

## Correccion de conteo Hater de tiempo completo

### Problema

La card `Hater de tiempo completo` mostraba `0` aunque existian mensajes
validos en `messages.message_normalized` con las palabras completas `odio`
o `hate`.

### Causa raiz

El sender configurado en `app/content_config.py` no coincidia con el valor
real guardado en `messages.sender`. La configuracion usaba un valor mojibake
distinto, mientras la base local contiene `\U0001d474\U0001d482\U0001d493\U0001f353`
(`𝑴𝒂𝒓🍓`). Por eso el filtro `sender = :sender_name` devolvia cero filas.

Ademas, la query original usaba `COUNT(*)`, por lo que solo contaba mensajes
coincidentes, no ocurrencias reales dentro del mismo mensaje.

### Cambio aplicado

- `app/content_config.py`: `HER_SENDER_NAME` queda alineado con el sender real
  `𝑴𝒂𝒓🍓`.
- `db/queries.py`: `ROMANTIC_HATER_WORD_COUNT_QUERY` usa
  `regexp_count(message_normalized, :pattern, 1, 'i')` y conserva SQL
  parametrizado.
- `db/romantic_queries.py`: el patron queda centralizado como
  `\m(odio|hate)\M` y el helper devuelve `int(row["total_odio"])`.
- `tests/test_romantic_queries.py`: valida patron, alias `total_odio`, uso de
  `message_normalized` y conteo por `regexp_count`.
- `tests/test_romantic_metrics.py`: valida que el servicio pase
  `HER_SENDER_NAME` al helper y que el valor llegue a la card.

### Validacion local

Consulta de solo lectura ejecutada contra PostgreSQL local:

```text
sender real: \U0001d474\U0001d482\U0001d493\U0001f353
patron usado: \m(odio|hate)\M
ocurrencias de odio o hate: 135
sender configurado anterior: 0 mensajes, 0 ocurrencias
```

El conteo actualizado cuenta ocurrencias reales de `odio` y `hate` como
palabras completas sobre `message_normalized`. Por ejemplo, `odio hate`
cuenta 2 y `odioso` no cuenta.

## Correccion de bloques especiales, frases bonitas y encoding visual

### Archivos modificados

- `app/content_config.py`
- `app/main.py`
- `services/romantic_metrics.py`
- `ui/components.py`
- `ui/styles.py`
- `tests/test_romantic_metrics.py`
- `tests/test_streamlit_entrypoint.py`
- `tests/test_ui_components.py`
- `docs/content_configuration.md`
- `docs/codex_session_debug.md`

### Bloques especiales

`ui/components.py` renderiza cada entrada de
`special_message["blocks"]` con `_build_special_message_block_html()`.

- `her_messages` queda agrupado en un solo
  `.special-message-block.special-message-block-her-messages`.
- `conversation_pair` queda en otro
  `.special-message-block.special-message-block-conversation-pair`.
- Las burbujas internas conservan el orden manual recibido desde
  `services/romantic_metrics.py`.
- `role = "me"` se renderiza con burbuja derecha y cualquier otro valor cae a
  `"her"`.

### Encoding visual

La metadata de burbujas ya no usa el literal mojibake `Ã‚Â·`. Ahora se construye
con `_build_message_meta_html()` y un separador ASCII seguro:

```html
<span class="message-meta-separator">-</span>
```

### Frases bonitas por ID

`services/romantic_metrics.py` resuelve
`ROMANTIC_CONTENT["featured_quotes"]["message_ids"]` con
`fetch_messages_by_ids()`, conserva el orden configurado e ignora valores
invalidos o IDs inexistentes.

El fallback automatico solo se ejecuta cuando `message_ids` esta vacio. Si no
hay mensajes finales para renderizar, `app/main.py` no muestra la seccion con
solo titulo.

### Configuracion

Para editar los bloques, usar `app/content_config.py`:

- `special_message.blocks[*].type = "her_messages"` con `message_ids`.
- `special_message.blocks[*].type = "conversation_pair"` con `messages`.
- `featured_quotes.message_ids` para frases bonitas manuales.

`get_reserved_message_ids()` tambien incluye `featured_quotes.message_ids` para
evitar duplicados en el fallback automatico.

Opcionalmente agregar:

```html
style="--reveal-delay: 120ms;"
```

### Resultado esperado

Las secciones y tarjetas aparecen con fade-up progresivo al entrar en viewport.

### Verificacion

Bloqueada por entorno Python local:

```text
.\venv\Scripts\python.exe -m pytest tests/test_ui_components.py tests/test_streamlit_entrypoint.py
Acceso denegado a pythoncore-3.14-64\python.exe

python -m pytest tests/test_ui_components.py tests/test_streamlit_entrypoint.py
python no esta disponible en PATH

py --version
py no esta disponible en PATH

streamlit run app/main.py
streamlit no esta disponible en PATH
```

## Bug: ImportError de `render_reveal_observer`

### Sintoma

La app fallaba al iniciar porque `app/main.py` importaba `render_reveal_observer` desde `ui.components`, pero el proceso Streamlit activo estaba sirviendo una version stale donde esa funcion no estaba disponible.

### Causa raiz

`render_reveal_observer` existe en `ui/components.py`, pero habia un servidor Streamlit antiguo en `http://localhost:8501` que seguia mostrando el `ImportError`. El import se valido con el Python del entorno virtual y el servidor se reinicio para cargar el codigo actual.

### Archivos afectados

- `app/main.py`
- `ui/components.py`
- `.streamlit/config.toml`
- `ui/error_boundary.py`
- `ui/styles.py`
- `tests/test_error_boundary.py`
- `tests/test_streamlit_entrypoint.py`
- `docs/codex_session_debug.md`

### Correccion aplicada

- Se mantuvo `render_reveal_observer` en `ui/components.py`.
- Se mantuvo el import y la llamada desde `app/main.py`.
- Se reinicio el proceso Streamlit stale que exponia el `ImportError`.
- Se agrego un error boundary global para que futuros errores no expongan tracebacks en UI.

### Verificacion

```powershell
.\venv\Scripts\python.exe -c "import ui.components as c; print(c.__file__); print(hasattr(c, 'render_reveal_observer'))"
```

Resultado:

```text
C:\Users\User\OneDrive\Escritorio\landing_page\ui\components.py
True
```

Validacion con Chromium headed:

```powershell
$env:PLAYWRIGHT_BASE_URL='http://127.0.0.1:8501'; npx playwright test e2e/streamlit-landing.spec.ts --headed --project=chromium
```

Resultado:

```text
1 passed
```

### Resultado

La app ya no muestra `ImportError` ni traceback visible por `render_reveal_observer`.

## Mejora de seguridad: manejo global de errores en Streamlit

### Motivo

La UI no debe exponer tracebacks, rutas locales, credenciales ni detalles tecnicos.

### Cambio aplicado

- Se creo `ui/error_boundary.py`.
- Se separo `run_app()` y `main()` en `app/main.py`.
- `main()` captura excepciones globales, llama `log_app_exception()` y renderiza `render_safe_error_message()`.
- `log_app_exception()` registra tipo de excepcion, contexto y traceback completo usando `logger.logger.log_critical_error`.
- `sanitize_error_message()` redacta URLs PostgreSQL con credenciales, variables sensibles y rutas locales antes de enviar el mensaje al logger existente.
- Se agrego `.streamlit/config.toml` con `showErrorDetails = false`.
- Se agrego CSS para `.safe-error-card` en `ui/styles.py`.

### Comportamiento final

- Excepciones completas quedan en logs, con datos sensibles redactados por el helper antes de usar el logger central.
- UI muestra solo: `Oops... Algo fallo. Contacta al administrador.`
- No se exponen credenciales ni detalles tecnicos en la UI.
- No se usa `except: pass`.

### Archivos afectados

- `app/main.py`
- `.streamlit/config.toml`
- `ui/error_boundary.py`
- `ui/styles.py`
- `tests/test_error_boundary.py`
- `tests/test_streamlit_entrypoint.py`
- `docs/codex_session_debug.md`

### Verificacion

```powershell
.\venv\Scripts\python.exe -m pytest tests/test_error_boundary.py tests/test_ui_components.py tests/test_streamlit_entrypoint.py
```

Resultado:

```text
9 passed
```

Depuracion adicional con Chromium headed:

```text
exceptionCount: 0
rawHtmlVisible: false
importErrorVisible: false
tracebackVisible: false
revealCount: 44
visibleRevealCount: 4
visibleAfterScroll: 8
```

## Ajustes visuales finales

### Motivo

La landing ya funciona y la animacion reveal-on-scroll quedo bien. Se hicieron ajustes visuales para mejorar grosor tipografico, consistencia de cards, burbujas tipo Instagram y legibilidad de graficos.

### Archivos afectados

- `ui/styles.py`
- `ui/components.py`
- `ui/charts.py`
- `tests/test_ui_components.py`
- `tests/test_ui_charts.py`
- `docs/codex_session_debug.md`

### Cambios aplicados

- Grosor tipografico general en titulos, labels, fechas, mensajes, metricas, chips y textos secundarios.
- Refuerzo visual de ejes de graficos Altair y helper Plotly con fuentes mas legibles.
- Mejora de cards con radio, bordes, sombras, glassmorphism y hover mas consistentes.
- Mejora de la seccion `Un mensaje que quiero guardar` como tarjeta tipo Instagram con burbuja alineada por remitente.
- Ajustes de degradado rosa/fucsia en acentos principales y cards destacadas.
- Gloss/glitter sutil en acentos fucsia, hero y mensaje especial.
- Conservacion de `reveal-on-scroll`, `is-visible` y el observer existente.

### Verificacion

```powershell
.\venv\Scripts\python.exe -m pytest tests/test_ui_components.py tests/test_ui_charts.py tests/test_streamlit_entrypoint.py
```

Resultado:

```text
7 passed
```

Validacion visual con Streamlit y Chromium headed:

```powershell
streamlit run app/main.py --server.port 8502
$env:PLAYWRIGHT_BASE_URL='http://127.0.0.1:8502'; npx playwright test e2e/streamlit-landing.spec.ts --headed --project=chromium
```

Resultado:

```text
1 passed
```

Inspeccion DOM:

```text
rawHtmlVisible: false
exceptionCount: 0
importErrorVisible: false
tracebackVisible: false
igChatCount: 1
igBubbleCount: 1
metricWeight: 800
sectionTitleWeight: 800
chartTitleWeight: 800
specialKickerWeight: 800
heroHasGloss: true
glitterCount: 1
revealCount: 44
```

### Resultado esperado

La landing mantiene el estilo romantico, pero se ve mas pulida, mas premium, mas legible y menos plana.

## Ajuste visual: fresa 8-bit en hero

### Motivo

El hero tenia un circulo decorativo vacio y se agrego una fresa pixel art como detalle visual dentro de ese espacio.

### Cambio aplicado

- Se agrego el asset transparente en `ui/assets/strawberry_8bit.png`.
- Se renderizo la imagen desde `ui/components.py` en `build_hero_html()`.
- Se agregaron `ASSETS_DIR`, `STRAWBERRY_IMAGE` y `STRAWBERRY_IMAGE_MIME_TYPE` con rutas basadas en `Path(__file__).parent`.
- Se agrego `_build_hero_strawberry_html()` para construir el contenedor visual.
- Se agrego `_build_image_data_uri()` para cargar el PNG local sin rutas absolutas.
- Se modifico `ui/styles.py`: el circulo vacio paso a `.hero-orb` y la imagen usa `.hero-strawberry`.
- Se mantuvieron `romantic-hero`, `reveal-on-scroll` y los textos principales del hero.

### Como cambiar la imagen

Reemplazar el archivo:

```text
ui/assets/strawberry_8bit.png
```

Si se usa otro nombre, actualizar `STRAWBERRY_IMAGE` en `ui/components.py`.

### Alcance

No se modifico ETL, queries, schema, base de datos ni logica de datos.

### Verificacion

```powershell
.\venv\Scripts\python.exe -m pytest tests/test_ui_components.py tests/test_streamlit_entrypoint.py
```

Resultado:

```text
8 passed
```

Validacion manual en `http://127.0.0.1:8503`:

```text
heroExists: true
orbExists: true
imageExists: true
imageSourceIsPngDataUri: true
imageComplete: true
imageNaturalWidth: 225
imageNaturalHeight: 225
orbDisplay: flex
orbAlignItems: center
orbJustifyContent: center
imageRendering: pixelated
rawHtmlVisible: false
tracebackVisible: false
```

Validacion movil:

```text
viewport: 390x844
orb: 96x96
image: 94x94
imageComplete: true
```

## Ajuste visual: glow fucsia en titulos

- Se aplico un efecto `text-shadow` fucsia suave a los titulos principales de secciones, timeline, graficos y cierre.
- El objetivo fue replicar de forma sutil el brillo visual del hero "Nuestra historia".
- El cambio quedo implementado en `ui/styles.py`.
- Selectores modificados: `.romantic-title-glow`, `.section-title`, `.timeline-title`, `.chart-title`, `.closing-card h2`.
- No se aplico glow al body, parrafos, captions, tooltips ni ejes de graficos.
- No se modifico la logica ETL ni la estructura de datos.

Verificacion:

```powershell
.\venv\Scripts\python.exe -m pytest tests/test_ui_components.py tests/test_streamlit_entrypoint.py
```

Resultado:

```text
8 passed
```

Validacion manual en `http://127.0.0.1:8504`:

```text
.section-title textShadow: rgba(212, 20, 114, 0.3) 0px 0px 10px
.timeline-title textShadow: rgba(212, 20, 114, 0.3) 0px 0px 10px
.chart-title textShadow: rgba(212, 20, 114, 0.3) 0px 0px 10px
.closing-card h2 textShadow: rgba(212, 20, 114, 0.3) 0px 0px 10px
.hero-subtitle textShadow: none
rawHtmlVisible: false
tracebackVisible: false
```

## Ajuste de configuracion: mensajes especiales y frases bonitas por ID

### Motivo

La landing ya estaba visualmente correcta, pero faltaba parametrizar correctamente que mensajes aparecen en "Un mensaje que quiero guardar" y "Mensajes para volver a leer despacio".

### Cambio aplicado

Archivos modificados:

- `app/content_config.py`
- `db/queries.py`
- `db/romantic_queries.py`
- `services/romantic_metrics.py`
- `ui/components.py`
- `tests/test_romantic_metrics.py`
- `tests/test_romantic_queries.py`
- `tests/test_ui_components.py`
- `docs/content_configuration.md`
- `docs/codex_session_debug.md`
- `docs/sessions/12_parametrizar_mensajes_por_id_20260613_195613.md`

Se agrego soporte para la estructura:

```python
ROMANTIC_CONTENT["special_message"]["blocks"]
```

Tipos soportados:

- `her_messages`: varios mensajes de ella definidos en `message_ids`.
- `conversation_pair`: conversacion compuesta por mensajes con `role` y `message_id`.

Tambien se mantuvo compatibilidad con:

```python
ROMANTIC_CONTENT["special_message"]["message_id"]
```

si `blocks` no tiene IDs validos.

La seccion:

```python
ROMANTIC_CONTENT["featured_quotes"]["message_ids"]
```

ahora usa consulta por lista de IDs cuando hay IDs manuales y conserva fallback automatico si la lista esta vacia.

### Como se configura

Los IDs se editan en:

```text
app/content_config.py
```

Para varios mensajes de ella:

```python
{
    "type": "her_messages",
    "title": "Cosas bonitas que ella me dijo",
    "message_ids": [123, 456, 789],
}
```

Para una conversacion:

```python
{
    "type": "conversation_pair",
    "title": "Una conversacion que quiero recordar",
    "messages": [
        {"role": "me", "message_id": 111},
        {"role": "her", "message_id": 222},
    ],
}
```

Para frases bonitas:

```python
ROMANTIC_CONTENT["featured_quotes"]["message_ids"] = [123, 456, 789]
```

### Resultado esperado

- Se pueden mostrar varios mensajes de ella.
- Se puede mostrar una conversacion con mensaje mio y respuesta de ella.
- Se pueden seleccionar frases bonitas cortas por ID.
- Se mantiene fallback automatico si no hay IDs configurados.
- No se repiten IDs reservados en fallback automatico.
- La UI usa `message`, no `message_normalized`, para mostrar textos originales.
- Los mensajes de base de datos se escapan antes de renderizar HTML visual.

### Verificacion

```powershell
.\venv\Scripts\python.exe -m pytest tests/test_romantic_metrics.py tests/test_ui_components.py tests/test_romantic_queries.py tests/test_streamlit_entrypoint.py
```

Resultado:

```text
16 passed
```

## Correccion de parsing de fechas en ETL

### Problema

El extractor de WhatsApp probaba primero formatos `DD/MM/YYYY` y `DD/MM/YY`.
Eso convertia fechas reales del export `MM/DD/YY`, como `6/12/26`,
en `2026-12-06` en lugar de `2026-06-12`.

Instagram no tenia inversion dia/mes porque usa `timestamp_ms` de Unix epoch
en milisegundos, pero el transformador lo dejaba en UTC mientras WhatsApp
quedaba sin timezone. Eso mezclaba datetimes naive y timezone-aware.

### Fuente de verdad

- WhatsApp: `MM/DD/YY` o `MM/DD/YYYY`, segun el archivo real exportado.
- Instagram: `timestamp_ms` como Unix epoch en milisegundos.
- Salida transformada: `datetime` timezone-aware en `-0500`.
- Rango esperado de conversacion: `2025-10-10` a `2026-06-21`.

### Cambio aplicado

- `etl/extract/whatsapp_extract.py`: `WHATSAPP_DATE_FORMATS` ahora solo
  acepta formatos explicitos `MM/DD/YYYY` y `MM/DD/YY`; el resultado se
  crea con timezone `-0500`.
- `etl/transform.py`: `parse_instagram_timestamp()` convierte epoch ms a
  `datetime` en UTC y luego a timezone `-0500`.
- `scripts/validate_timestamp_consistency.py`: diagnostica artefactos
  transformados y falla si hay timestamps string, naive, fuera de rango,
  meses sospechosos de inversion o registros desordenados.
- `db/queries.sql`: se elimino un `UPDATE` manual que cambiaba junio por
  diciembre y se reemplazo por consultas no destructivas de diagnostico.

### Como probar

```powershell
.\venv\Scripts\python.exe -m pytest tests/test_whatsapp_extract.py tests/test_transform.py tests/test_timestamp_consistency.py
```

Validar un artefacto transformado:

```powershell
.\venv\Scripts\python.exe scripts\validate_timestamp_consistency.py data\staging\transformed\archivo_transformado.parquet
```

### Reprocesamiento de datos ya cargados

No ejecutar SQL destructivo sin respaldo.

Procedimiento recomendado:

1. Crear respaldo de `messages`.
2. Borrar staging transformado corrupto si fue generado con el parser anterior.
3. Limpiar `messages` solo despues del respaldo.
4. Volver a correr ETL con los archivos fuente originales.
5. Ejecutar `scripts\validate_timestamp_consistency.py` sobre el nuevo
   artefacto transformado.
6. Revisar las consultas no destructivas agregadas en `db/queries.sql`.

Comando ETL recomendado:

```powershell
.\venv\Scripts\python.exe scripts\run_etl.py data\raw\WhatsApp_Chat_with_Mar🍓.txt data\raw\ig_message_1.json data\raw\ig_message_2.json --save-artifacts
```
