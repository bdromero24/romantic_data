# Requerimiento Técnico: Componente `SpotifyCapsule` — 8-Bit Neon Player

## 1. Contexto del proyecto

Estoy trabajando en una landing romántica construida en **Python + Streamlit**. La app ya está desplegada en Streamlit Cloud y actualmente puede funcionar en modo de **datos congelados** mediante `data/final/landing_data.json`, por lo que en producción no debe depender obligatoriamente de PostgreSQL.

La estética actual de la landing combina:

- rosa, blanco y fucsia;
- glassmorphism;
- neon glow fucsia;
- pixel art / 8-bit;
- assets locales como fresa 8-bit, corazón 8-bit y pergaminos;
- renderizado de HTML personalizado mediante `st.markdown(..., unsafe_allow_html=True)` y/o `streamlit.components.v1.html()`.

Necesito agregar un nuevo detalle interactivo tipo **easter egg** llamado `SpotifyCapsule`, inspirado visualmente en una **lámpara acrílica neón tipo Spotify**, pero adaptado al estilo visual de la landing.

El componente celebrará la primera canción dedicada: **“Mujer Amante” — Rata Blanca**.

---

## 2. Objetivo funcional

Crear un componente interactivo que renderice un player visual tipo cápsula/lámpara neón con:

- portada/foto personalizada;
- título de canción;
- artista;
- badge romántico;
- botón play/pause;
- botones `-5s` y `+5s`;
- audio iniciado en un segundo configurable;
- reproducción limitada a un fragmento aproximado de **45 segundos**;
- barra de progreso;
- visualizador simple tipo waveform/pixel bars;
- letras/frases sincronizadas por tiempo;
- efecto máquina de escribir / diálogo RPG para el texto sincronizado.

El componente debe poder mostrarse desde una nueva sección, botón o pestaña dentro de la landing, preferiblemente como easter egg con copy tipo:

```text
Nuestra canción
```

---

## 3. Alcance recomendado

Implementar una **versión 1 estable** del componente.

### Debe incluir

- Player visual.
- Imagen local.
- Audio local.
- Play/pause.
- Inicio en segundo configurable.
- Fin automático del fragmento después de 45 segundos o después de `end_time_seconds` si se configura.
- Letras/frases sincronizadas.
- Botón o pestaña “Nuestra canción”.
- Estética 8-bit / neon / glassmorphism.
- Compatibilidad con Streamlit Cloud.

### No incluir en esta primera versión

- Integración real con Spotify.
- Descarga de audio desde internet.
- Letras completas de canciones.
- Web Audio API avanzada.
- Visualizador real de frecuencia de audio.
- Dependencias externas innecesarias.

---

## 4. Requisitos de arquitectura

Crear un nuevo módulo:

```text
ui/spotify_capsule.py
```

con una función principal:

```python
def render_spotify_8bit_player(config: dict) -> None:
    ...
```

La función debe usar:

```python
streamlit.components.v1.html(...)
```

para renderizar un componente HTML/CSS/JS autocontenido.

No modificar la arquitectura general de la landing ni romper secciones existentes.

---

## 5. Configuración desde `content_config.py`

Agregar una configuración editable, idealmente dentro de `ROMANTIC_CONTENT`:

```python
"spotify_capsule": {
    "enabled": True,
    "title": "Mujer Amante",
    "artist": "Rata Blanca",
    "badge_text": "Nuestra primera canción 🎵",
    "song_path": "ui/assets/audio/mujer_amante_fragment.mp3",
    "cover_image_path": "ui/assets/images/spotify_capsule_cover.png",
    "start_time_seconds": 45,
    "duration_seconds": 45,
    "lyrics_data": [
        {
            "time": 45,
            "text": "Fragmento corto o frase personalizada configurada manualmente."
        },
        {
            "time": 52,
            "text": "Otra frase breve sincronizada."
        }
    ]
}
```

### Reglas importantes

- No generar letras automáticamente.
- No descargar letras desde internet.
- No incluir letras completas protegidas por copyright.
- Las frases deben venir únicamente desde configuración manual.
- El audio debe ser un fragmento corto proporcionado manualmente por el usuario.

---

## 6. Fragmento de audio

Inicialmente pensé en usar toda la canción, pero el alcance correcto será usar un fragmento de aproximadamente **45 segundos**.

### Requerimientos

- El audio debe iniciar en `start_time_seconds`.
- El player debe detenerse automáticamente cuando se cumpla:

```text
start_time_seconds + duration_seconds
```

Ejemplo:

```python
"start_time_seconds": 45,
"duration_seconds": 45
```

Entonces el audio debe reproducirse desde el segundo 45 hasta aproximadamente el segundo 90.

### Comportamiento esperado

- En la primera reproducción, saltar a `start_time_seconds`.
- Si el usuario pausa y vuelve a reproducir, continuar desde el punto actual.
- Si el audio llega al límite del fragmento, pausar y volver al estado visual inicial o mostrar estado de finalizado.
- Los botones `+5s` y `-5s` deben respetar el rango permitido del fragmento.

---

## 7. Manejo de assets locales

El componente debe soportar archivos locales del repo:

```text
ui/assets/audio/
ui/assets/images/
```

Requerimientos:

- convertir la imagen a `base64` para incrustarla en el HTML;
- convertir el audio a `base64` o resolverlo de forma compatible con Streamlit Cloud;
- si el archivo de audio no existe, mostrar un fallback visual sin romper la app;
- si la imagen no existe, mostrar placeholder visual pixel/neón;
- no depender de rutas absolutas locales;
- usar rutas relativas al proyecto.

Crear helpers internos como:

```python
def _asset_to_base64(path: str) -> str | None:
    ...

def _audio_to_data_uri(path: str) -> str | None:
    ...

def _image_to_data_uri(path: str) -> str | None:
    ...
```

---

## 8. Estilo visual

El player debe tener estética:

```text
8-bit / neon / glassmorphism / acrylic lamp
```

Inspiración visual: una lámpara acrílica neón tipo Spotify, pero con estética romántica 8-bit.

### Estilo requerido

- fondo semitransparente tipo acrílico;
- borde fucsia `#ff007f`;
- efecto neon glow con `box-shadow`, `filter: drop-shadow()` o `text-shadow`;
- tipografía pixelada usando Google Fonts:
  - `Press Start 2P`, o
  - `VT323`;
- controles tipo consola arcade;
- overlay de scanlines CRT sutil;
- imagen central con tratamiento pixel/neón;
- diseño responsive;
- color coherente con la landing actual;
- sensación de “placa acrílica iluminada” sobre una base oscura.

### Paleta base

```css
--neon-pink: #ff007f;
--soft-pink: #ffd1ea;
--deep-pink: #b0005a;
--white-glass: rgba(255, 255, 255, 0.16);
--dark-panel: rgba(35, 10, 28, 0.55);
```

---

## 9. Interacción de audio

El componente debe incluir un `<audio>` controlado por JavaScript.

Funcionalidad:

- al presionar play:
  - si es la primera reproducción, iniciar en `start_time_seconds`;
  - luego alternar play/pause normalmente;
- botón `-5s`;
- botón `+5s`;
- barra de progreso actualizada;
- tiempo actual / duración del fragmento;
- detener audio al llegar a `start_time_seconds + duration_seconds`;
- manejar errores de audio con mensaje visual amigable.

Eventos sugeridos:

```javascript
audio.addEventListener("loadedmetadata", ...)
audio.addEventListener("timeupdate", ...)
audio.addEventListener("ended", ...)
```

### Restricción del rango de reproducción

Si el usuario presiona `-5s`, no debe ir antes de `start_time_seconds`.

Si el usuario presiona `+5s`, no debe superar:

```text
start_time_seconds + duration_seconds
```

---

## 10. Letras/frases sincronizadas

Usar `lyrics_data` como lista de objetos:

```python
[
    {"time": 45, "text": "..."},
    {"time": 52, "text": "..."}
]
```

Reglas:

- ordenar por `time`;
- mostrar la frase correspondiente según `audio.currentTime`;
- aplicar efecto máquina de escribir cuando cambia la frase;
- si no hay `lyrics_data`, mostrar `badge_text` o mensaje fallback;
- no usar letras generadas automáticamente;
- no incluir letras completas.

---

## 11. Seguridad y serialización

Al pasar `config` al HTML:

- usar `json.dumps(config, ensure_ascii=False)`;
- escapar datos dinámicos cuando sea necesario;
- evitar interpolar texto no escapado directamente dentro de HTML;
- evitar romper el script si hay comillas, emojis o caracteres especiales;
- evitar exponer rutas locales del sistema operativo.

---

## 12. Integración en `app/main.py`

Agregar la sección de forma controlada.

Opción recomendada:

```python
from ui.spotify_capsule import render_spotify_8bit_player
```

Y renderizarla cerca del cierre o como easter egg después de una sección romántica.

Debe respetar:

```python
spotify_config = ROMANTIC_CONTENT.get("spotify_capsule", {})

if spotify_config.get("enabled", False):
    render_spotify_8bit_player(spotify_config)
```

No debe afectar el modo estático `USE_STATIC_DATA=true`.

---

## 13. Botón o pestaña

Agregar un trigger visual simple, por ejemplo:

```text
🎵 Nuestra canción
```

Puede implementarse con:

```python
st.button()
```

y `st.session_state`, o como botón interno del componente HTML.

### Preferencia

- si se puede mantener simple, usar `st.session_state`;
- si el diseño queda mejor autocontenido, implementar el botón dentro del HTML.

### Experiencia esperada

```text
El usuario ve un botón/pestaña “Nuestra canción”.
Al activarlo, aparece la cápsula neón 8-bit.
```

---

## 14. Compatibilidad con Streamlit Cloud

El componente debe funcionar en Streamlit Cloud.

Requisitos:

- no depender de PostgreSQL;
- no depender de archivos fuera del repo;
- no depender de rutas absolutas;
- no requerir instalación de librerías adicionales si no son estrictamente necesarias;
- no romper el modo de datos congelados;
- no modificar `data/final/landing_data.json` para esta funcionalidad, salvo que sea estrictamente necesario.

---

## 15. Validaciones esperadas

Validar localmente:

```powershell
$env:USE_STATIC_DATA="true"
streamlit run app/main.py
```

Confirmar:

- la landing carga;
- el botón/sección aparece;
- la cápsula renderiza;
- la imagen carga;
- el audio reproduce;
- el audio inicia en el segundo configurado;
- el audio se detiene después de aproximadamente 45 segundos;
- los botones `+5s` y `-5s` funcionan;
- las frases sincronizadas cambian;
- no hay errores en consola de Streamlit;
- no se rompe el despliegue actual.

---

## 16. Documentación

Actualizar documentación:

```text
docs/content_configuration.md
docs/codex_session_debug.md
```

Explicar:

- dónde configurar la cápsula;
- dónde poner audio e imagen;
- cómo cambiar `start_time_seconds`;
- cómo cambiar `duration_seconds`;
- cómo editar `lyrics_data`;
- cómo desactivar el componente con `enabled=False`;
- advertencia de no subir audio sensible o no autorizado en repo público.

---

## 17. Restricciones

- No cambiar ETL.
- No cambiar queries.
- No cambiar datos congelados salvo que sea estrictamente necesario.
- No romper el deploy de Streamlit Cloud.
- No introducir dependencia externa innecesaria.
- No descargar audio desde internet.
- No generar letras completas protegidas por copyright.
- No tocar secciones visuales existentes salvo la integración del nuevo componente.
- No exponer rutas locales o secretos.

---

## 18. Entregable

Devolver:

1. archivos creados/modificados;
2. código completo por archivo;
3. explicación breve de integración;
4. pasos para probar localmente;
5. advertencias si falta el archivo de audio o imagen;
6. comandos sugeridos para commit/push si todo queda validado.
