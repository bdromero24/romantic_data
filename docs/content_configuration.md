# Configuracion manual de contenido romantico

## Archivo principal

La configuracion manual vive en:

```text
app/content_config.py
```

Ese archivo contiene `ROMANTIC_CONTENT`, `DISPLAY_LABELS` y el helper `get_reserved_message_ids()`.

Regla general:

```text
message_normalized -> busquedas, filtros y conteos
message            -> textos originales visibles en la UI
DISPLAY_LABELS     -> labels visibles para palabras normalizadas
```

## Configuracion visual del hero

La fresa 8-bit del hero se carga desde:

```text
ui/assets/strawberry_8bit.png
```

La ruta se define en `ui/components.py` con `Path(__file__).parent`, sin rutas absolutas de maquina.

Para cambiar la imagen, reemplaza ese PNG por otro asset con fondo transparente. Si cambias el nombre del archivo, actualiza:

```python
STRAWBERRY_IMAGE = ASSETS_DIR / "strawberry_8bit.png"
```

El circulo decorativo y la imagen se controlan en `ui/styles.py` con:

```css
.hero-orb
.hero-strawberry
```

Este ajuste no modifica ETL, consultas ni logica de datos.

## Assets visuales de secciones romanticas

Los assets decorativos de la landing viven en:

```text
ui/assets/
```

Assets actuales:

```text
ui/assets/strawberry_8bit.png
ui/assets/perrgamino.png
ui/assets/corazon.png
```

`ui/components.py` carga estos PNG como `data:image/png;base64` con
`_build_image_data_uri()`, para que Streamlit los renderice sin rutas locales
visibles en la UI.

## Como editar "Un mensaje que quiero guardar"

La seccion se configura en:

```python
ROMANTIC_CONTENT["special_message"]["blocks"]
```

La card principal de esta seccion se renderiza desde:

```text
ui/components.py
```

con `render_special_message()` y `build_special_message_html()`.

La estructura permite varios bloques manuales. Si `blocks` no tiene IDs validos, la app conserva el fallback heredado de:

```python
ROMANTIC_CONTENT["special_message"]["message_id"]
```

### Varios mensajes de ella

Edita `message_ids` con IDs reales de la tabla `messages`:

```python
{
    "type": "her_messages",
    "title": "Cosas bonitas que ella me dijo",
    "message_ids": [123, 456, 789],
}
```

La app consulta esos mensajes por `id`, mantiene el orden de la lista y los renderiza como burbujas de ella dentro de un solo recuadro visual para ese bloque.

### Conversacion mio + respuesta de ella

Edita cada `message_id` dentro de `messages`:

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

Reglas de rol:

```text
role = "me"  -> burbuja alineada a la derecha
role = "her" -> burbuja alineada a la izquierda
```

Si aparece un rol no reconocido, la app lo trata como `"her"`.

Cada bloque `conversation_pair` se renderiza en su propio recuadro visual, separado de los bloques `her_messages`, y conserva el orden manual de `messages`.

### Titulos internos del bloque especial

Los subtitulos internos de cada bloque se editan en:

```python
ROMANTIC_CONTENT["special_message"]["blocks"][*]["title"]
```

Ejemplos:

```python
"title": "Cosas bonitas que ella me dijo"
"title": "Una conversacion que quiero recordar"
```

Estos titulos se renderizan con la clase CSS
`.special-message-block-title` en `ui/styles.py`, que aplica brillo fucsia
suave mediante `text-shadow`.

La tipografia de esos subtitulos tambien se controla desde
`.special-message-block-title`. Usa la misma familia decorativa que el titulo
principal del bloque especial (`--font-script`) y un tamano calculado como
2 px menor que `.special-message-kicker`.

Para ocultar un titulo interno, dejarlo vacio:

```python
"title": ""
```

Cuando queda vacio, la app no renderiza un titulo ni deja un header vacio en
ese bloque.

## Como editar "Mensajes para volver a leer despacio"

La seccion se configura en:

```python
ROMANTIC_CONTENT["featured_quotes"]["message_ids"]
```

La seccion se renderiza desde `ui/components.py` con `render_quotes()` y
`build_quote_cards_html()`.

Ejemplo:

```python
"message_ids": [123, 456, 789]
```

Si la lista contiene IDs, la app muestra exactamente esos mensajes disponibles, en el orden configurado. Si la lista queda vacia, se activa el fallback automatico con `fallback_limit`.

El fallback automatico solo se usa cuando `message_ids` esta vacio. Si la lista tiene valores invalidos o IDs inexistentes, esos valores se ignoran de forma segura y no se muestra una seccion vacia con solo titulo.

### Cartas desbloqueables

Cada mensaje de esta seccion usa:

```html
class="love-letter-card"
```

La seccion se renderiza desde `ui/components.py` con `render_quotes()` y
`build_quote_cards_html()`.

La seccion sigue alimentandose desde `featured_quotes`, pero visualmente usa
cartas desbloqueables tipo sobre. Cada card se muestra cerrada como
`Mensaje guardado` y revela el mensaje, sender y fecha con hover en desktop o
click/tap en mobile.

Clases principales:

```text
.love-letter-grid
.love-letter-card
.love-letter-inner
.love-letter-front
.love-letter-back
.love-letter-envelope
.love-letter-heart-seal
.love-letter-message
.love-letter-sender
.love-letter-date
```

El comportamiento click/tap se inyecta desde `render_love_letter_unlocker()`
con `streamlit.components.v1.html()`. El efecto visual se controla en
`ui/styles.py` con las clases `love-letter-*`.

Los IDs y la logica de carga no dependen de este estilo.

## Corazon 8-bit en "Primer te amo"

El asset del corazon 8-bit queda en:

```text
ui/assets/corazon.png
```

Los cards relacionados con `Primer te amo` se renderizan desde:

```text
ui/components.py
```

Renderers implicados:

```python
build_metric_cards_html()
build_timeline_html()
```

La clase CSS que controla el contenedor marcado es:

```css
.first-te-amo-card
```

La clase CSS que posiciona el corazon 8-bit es:

```css
.first-te-amo-heart
```

El corazon se inserta solo cuando el label o titulo del card contiene
`Primer te amo`. No cambia la logica del calculo ni los IDs configurados.

El fondo transparente del asset se corrige directamente en
`ui/assets/corazon.png`; el CSS mantiene `background: transparent`,
`image-rendering: pixelated` y no agrega contenedores con fondo.

## SpotifyCapsule 8-bit neon

La capsula tipo player neon se configura en:

```python
ROMANTIC_CONTENT["spotify_capsule"]
```

El componente se renderiza desde:

```text
ui/spotify_capsule.py
```

La integracion controlada vive en:

```text
app/main.py
```

Para desactivarlo:

```python
"spotify_capsule": {
    "enabled": False,
}
```

### Audio e imagen

El fragmento de audio local debe ponerse en:

```text
ui/assets/audio/Mujer_amante_fragment.mp3
```

Las portadas locales del carrusel deben ponerse en:

```text
ui/assets/images/spotify_capsule_cover.png
ui/assets/images/spotify_capsule_cover_2.png
ui/assets/images/spotify_capsule_cover_3.png
ui/assets/images/spotify_capsule_cover_4.png
```

Las rutas se editan en:

```python
"song_path": "ui/assets/audio/Mujer_amante_fragment.mp3"
"cover_image_path": "ui/assets/images/spotify_capsule_cover.png"
"cover_image_paths": [
    "ui/assets/images/spotify_capsule_cover.png",
    "ui/assets/images/spotify_capsule_cover_2.png",
    "ui/assets/images/spotify_capsule_cover_3.png",
    "ui/assets/images/spotify_capsule_cover_4.png",
]
"cover_rotation_seconds": 15
```

`cover_image_paths` activa el carrusel automatico. El player cambia a la
siguiente imagen cada `cover_rotation_seconds` segundos con una transicion
fade/glow. Si hay una sola imagen valida, se muestra fija y no inicia
intervalo.

`cover_image_path` se conserva como configuracion legacy para una sola
portada. Si existe `cover_image_paths`, el componente usa esa lista y omite
las rutas que no existan. Si no queda ninguna imagen valida, muestra un
placeholder pixel/neon sin romper la app.

El componente convierte audio e imagenes a `data:` URI base64 para no exponer
rutas absolutas locales. Si falta el audio, el player muestra un mensaje
visual y desactiva controles.

No subas al repo publico audio sensible, privado o sin autorizacion. Usa solo
un fragmento corto proporcionado manualmente y con permiso.

### Inicio y duracion del fragmento

Edita:

```python
"start_time_seconds": 45,
"duration_seconds": 45,
```

Con esa configuracion, el audio empieza en el segundo 45 y se detiene al
llegar aproximadamente al segundo 90. Los botones `-5s` y `+5s` respetan ese
rango.

### Frases sincronizadas

Las frases visibles se editan manualmente en:

```python
"lyrics_data": [
    {"time": 45, "text": "Frase breve configurada manualmente."},
    {"time": 52, "text": "Otra frase corta."},
]
```

Reglas:

- No generar letras automaticamente.
- No descargar letras desde internet.
- No pegar letras completas protegidas por copyright.
- Usar frases cortas o texto personalizado configurado a mano.

## KPIs de "Pequenos datos bonitos"

El layout de los KPIs se renderiza desde:

```text
ui/components.py
```

con `render_metric_cards()` y `build_metric_cards_html()`.

El orden de los cards se arma en:

```text
services/romantic_metrics.py
```

con `_build_summary_cards()`. Los tres cards grandes priorizados son:

```text
Mensajes compartidos
Primer te amo
Mes mas intenso
```

El grid visual se controla en `ui/styles.py` con `.bento-grid`,
`.bento-card`, `.bento-card.large` y `.bento-card.full`. La card
`Quien prendio mas veces la conversacion` se arma como KPI secundario en
`services/romantic_metrics.py` dentro de `_build_summary_cards()` para quedar
en la misma grilla, a la derecha de `Hater de tiempo completo` cuando el
ancho disponible lo permite.

### Promedio diario

El KPI `Promedio diario` se calcula con:

```text
db/queries.py -> ROMANTIC_AVERAGE_DAILY_MESSAGES_QUERY
db/romantic_queries.py -> fetch_average_daily_messages()
```

La query agrupa mensajes validos por dia calendario y calcula
`AVG(total_messages)`, considerando ambos sender.

El valor de UI se redondea en `services/romantic_metrics.py` con
`_format_rounded_number()` dentro de `_build_summary_cards()`. El calculo
interno puede seguir siendo decimal, pero la card renderizada por
`ui/components.py` muestra un entero.

Verificacion visual recomendada:

1. Ejecutar `streamlit run app/main.py`.
2. Abrir la seccion `Pequenos datos bonitos`.
3. Confirmar que los tres cards grandes aparecen primero y a la izquierda en
   desktop.
4. Confirmar que `Promedio diario` aparece como card secundaria sin overflow.

Verificacion del carrusel SpotifyCapsule:

```powershell
.\venv\Scripts\python.exe -m pytest tests/test_spotify_capsule.py tests/test_streamlit_entrypoint.py
$env:USE_STATIC_DATA="true"
streamlit run app/main.py
```

Abrir la capsula, confirmar que la primera portada carga y esperar
`cover_rotation_seconds` para validar el cambio automatico. Si todavia no
existen `spotify_capsule_cover_2.png`, `spotify_capsule_cover_3.png` o
`spotify_capsule_cover_4.png`, la app las omite y mantiene la portada valida.

## Message key estable

`message_key` es una llave SHA-256 deterministica construida con:

```text
source|sender|timestamp_iso|message_normalized
```

El `id` de `messages` sigue soportado, pero no debe ser la unica referencia a
largo plazo porque puede cambiar si se reinicia la identidad de la tabla.

Antes de migrar referencias manuales:

```powershell
python scripts/backup_configured_messages.py
python scripts/backfill_message_keys.py
python scripts/export_content_config_message_keys.py
```

Para obtener `message_key` de un mensaje configurado, usa el CSV generado en:

```text
data/backups/content_config_message_key_mapping_YYYYMMDD_HHMMSS.csv
```

Luego agrega `message_key` junto a `message_id`:

```python
{
    "message_id": 40210,
    "message_key": "hash_sha256",
}
```

Para listas de mensajes, usa `message_keys` en el mismo orden que
`message_ids`:

```python
{
    "message_ids": [123, 456],
    "message_keys": ["hash_123", "hash_456"],
}
```

La app primero busca por `message_key`; si no existe o no encuentra fila, usa
`message_id` como fallback.

## Que ID usar

Usa el valor de la columna `id` de la tabla `messages`.

No uses el numero de fila visual del visor de base de datos, porque ese numero puede cambiar segun filtros, ordenamientos o paginacion.

Para nuevas referencias manuales, conserva el `message_id` como fallback y
agrega tambien `message_key` despues de ejecutar el backfill.

## Que pasa si dejo IDs vacios o None

- `None` significa no usar mensaje manual en ese campo.
- Una lista vacia en `blocks[*]["message_ids"]` omite ese bloque.
- Una lista vacia en `featured_quotes["message_ids"]` activa el fallback automatico.
- La app no debe fallar si un ID no existe o si un bloque queda sin mensajes validos.

## Evitar duplicados

`get_reserved_message_ids()` recolecta IDs manuales usados en:

```python
ROMANTIC_CONTENT["special_message"]["message_id"]
ROMANTIC_CONTENT["special_message"]["blocks"][*]["message_ids"]
ROMANTIC_CONTENT["special_message"]["blocks"][*]["messages"][*]["message_id"]
ROMANTIC_CONTENT["first_te_amo"]["message_id"]
ROMANTIC_CONTENT["timeline"][*]["message_id"]
ROMANTIC_CONTENT["featured_quotes"]["message_ids"]
```

Cuando `featured_quotes["message_ids"]` esta vacio, el fallback automatico excluye esos IDs reservados para evitar repeticiones en frases bonitas.

## ETL incremental recomendado

No se recomienda hacer `TRUNCATE` sobre `messages`, porque reinicia los IDs y
puede hacer que la landing renderice mensajes distintos a los configurados.

El flujo recomendado es incremental/idempotente:

```powershell
python scripts/run_etl.py data/raw/archivo.txt data/raw/archivo.json --save-artifacts
```

La carga usa `ON CONFLICT (source, sender, message, timestamp) DO UPDATE` para
insertar mensajes nuevos y completar campos derivados como `message_key` en
mensajes ya existentes. No actualiza `source`, `sender`, `message`,
`timestamp`, `id` ni `created_at`.

## Separador visual de metadata

La metadata de burbujas de mensaje se renderiza con un separador HTML seguro:

```html
<span class="message-meta-separator">-</span>
```

Esto evita mojibake visible como `Ã‚Â·` en la UI.

## Seguridad HTML

Los mensajes que vienen de la base de datos se escapan con `html.escape` antes de renderizarse.

No metas HTML en mensajes crudos de la tabla `messages`; se mostrara como texto seguro, no como HTML.

En textos manuales de `app/content_config.py`, la app permite solamente `<strong>...</strong>` limpio mediante el sanitizador de componentes.

## Como cambiar labels visibles

`message_normalized` puede contener texto sin tildes ni `ñ`, por ejemplo `te extrano`, porque se usa para busquedas y conteos.

Para mostrar el label correcto en la UI, edita:

```python
DISPLAY_LABELS = {
    "te extrano": "te extraño",
}
```

## Como editar el timeline

El timeline se controla en:

```python
ROMANTIC_CONTENT["timeline"]
```

Para agregar un hito manual:

```python
{
    "title": "Un mensaje que quiero recordar",
    "message_id": 40210,
    "mode": "manual_message",
}
```

Modos automaticos disponibles:

```text
auto_first_message
auto_first_te_amo
auto_first_te_extrano
auto_first_happy_message
auto_peak_day
auto_peak_month
```

## BirthdayInvitationLetter / Invitacion de cumpleanos

La invitacion interactiva se configura en:

```python
ROMANTIC_CONTENT["birthday_invitation"]
```

El componente se renderiza desde:

```text
ui/birthday_invitation.py
```

Para activar o desactivar la seccion, edita:

```python
"enabled": True
```

Usa `False` para ocultarla sin borrar la configuracion.

Campos editables:

```python
"closed_title": "Nueva carta para ti \U0001f48c",
"closed_subtitle": "Toca para abrir tu invitacion",
"letter_title": "Querida Mar:",
"letter_body": [
    "Tengo una invitacion especial para ti.",
],
"signature": "Con amor, David",
"primary_link_text": "Ver opcion 1",
"primary_link_url": "https://www.tiktok.com/...",
"secondary_link_text": "Ver opcion 2",
"secondary_link_url": "https://www.tiktok.com/...",
```

`letter_body` es una lista de parrafos. Cada item se muestra como un parrafo
separado dentro de la carta tipo pergamino.

Los dos links de glamping/cabana se cambian en:

```python
"primary_link_url": "https://www.tiktok.com/...",
"secondary_link_url": "https://www.tiktok.com/...",
```

Si un link queda vacio, ese boton no se renderiza. Si ambos links quedan
vacios, la carta se muestra sin botones y la app no falla.

Verificacion local recomendada:

```powershell
.\venv\Scripts\python.exe -m pytest tests/test_birthday_invitation.py tests/test_streamlit_entrypoint.py
$env:USE_STATIC_DATA="true"
streamlit run app/main.py
```

El componente no depende de la base de datos, no lee
`data/final/landing_data.json` y no requiere backend ni APIs externas.
