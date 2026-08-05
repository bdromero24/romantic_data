# Prompt para Codex — Carrusel de portadas en SpotifyCapsule 8-bit Neon Player

## 1. Contexto del proyecto

Estoy trabajando en una landing romántica construida en **Python + Streamlit**. La app ya está desplegada en Streamlit Cloud y usa un modo de **datos congelados** mediante `data/final/landing_data.json`, por lo que en producción no debe depender de PostgreSQL.

La estética general de la landing combina:

- rosa, blanco y fucsia;
- glassmorphism;
- neon glow fucsia;
- pixel art / 8-bit;
- assets locales;
- componentes HTML/CSS/JS renderizados desde Streamlit;
- una experiencia visual de cápsula romántica, no dashboard técnico.

Ya existe un componente tipo reproductor musical llamado algo similar a:

```text
SpotifyCapsule
```

o una función similar a:

```python
def render_spotify_8bit_player(config: dict) -> None:
    ...
```

Este componente actualmente renderiza una cápsula visual inspirada en una **lámpara acrílica de neón tipo Spotify**, adaptada a estilo **8-bit / Retro Pixel Art**.

El componente ya reproduce un fragmento de audio de la canción **“Mujer Amante” — Rata Blanca** y muestra una portada/foto personalizada.

---

## 2. Objetivo de este cambio

Necesito mejorar el componente para que la portada no sea una sola imagen fija, sino un **carrusel automático de varias imágenes**.

La intención visual es que siga pareciendo un **reproductor premium tipo Spotify / placa acrílica musical**, pero sin abandonar la estética actual:

```text
Spotify premium + lámpara acrílica neón + 8-bit + fucsia/glassmorphism
```

El resultado esperado es:

- varias fotos en la portada del player;
- cambio automático cada 15 segundos;
- transición suave tipo fade/glow;
- diseño elegante, no brusco;
- coherencia visual con el reproductor actual;
- soporte para fallback si solo hay una imagen.

---

## 3. Cambio funcional requerido

Actualmente la configuración probablemente usa una sola ruta:

```python
"cover_image_path": "ui/assets/images/spotify_capsule_cover.png"
```

Necesito que soporte una lista:

```python
"cover_image_paths": [
    "ui/assets/images/spotify_capsule_cover_1.png",
    "ui/assets/images/spotify_capsule_cover_2.png",
    "ui/assets/images/spotify_capsule_cover_3.png",
    "ui/assets/images/spotify_capsule_cover_4.png",
],
"cover_rotation_seconds": 15,
```

### Compatibilidad requerida

Mantener compatibilidad hacia atrás:

- si existe `cover_image_paths`, usar esa lista;
- si no existe `cover_image_paths` pero existe `cover_image_path`, usar esa imagen única;
- si la lista está vacía o las imágenes no existen, mostrar un placeholder visual neón/pixel sin romper la app.

---

## 4. Configuración esperada

Actualizar la configuración del componente en el archivo donde actualmente esté configurado, probablemente `content_config.py` o el módulo equivalente.

La configuración debería quedar conceptualmente así:

```python
"spotify_capsule": {
    "enabled": True,
    "title": "Mujer Amante",
    "artist": "Rata Blanca",
    "badge_text": "La primera canción que te dediqué",
    "song_path": "ui/assets/audio/mujer_amante_fragment.mp3",
    "cover_image_paths": [
        "ui/assets/images/spotify_capsule_cover_1.png",
        "ui/assets/images/spotify_capsule_cover_2.png",
        "ui/assets/images/spotify_capsule_cover_3.png",
        "ui/assets/images/spotify_capsule_cover_4.png",
    ],
    "cover_rotation_seconds": 15,
    "start_time_seconds": 0,
    "lyrics_data": [
        {"time": 0, "text": "Un fragmento corto para volver a ese momento."}
    ],
}
```

### Importante

No modificar ni eliminar `lyrics_data`. Este cambio es únicamente para el carrusel de imágenes y el pulido visual del player.

---

## 5. Manejo técnico de assets

El componente debe seguir soportando assets locales dentro del repo.

Rutas esperadas:

```text
ui/assets/images/spotify_capsule_cover_1.png
ui/assets/images/spotify_capsule_cover_2.png
ui/assets/images/spotify_capsule_cover_3.png
ui/assets/images/spotify_capsule_cover_4.png
```

Requerimientos:

- convertir cada imagen local a `data URI` / base64 para que funcione dentro de `streamlit.components.v1.html()`;
- no depender de URLs externas;
- mantener compatibilidad con Streamlit Cloud;
- si una imagen no existe, omitirla y registrar/mostrar un fallback razonable;
- no romper el render si una de las rutas está mal.

Si ya existen helpers como:

```python
def _image_to_data_uri(path: str) -> str | None:
    ...
```

reutilizarlos. Si no existen, crearlos en el módulo del componente.

---

## 6. Comportamiento del carrusel

Implementar en el JavaScript interno del componente:

1. Mostrar la primera imagen disponible al cargar.
2. Cambiar automáticamente a la siguiente imagen cada `cover_rotation_seconds` segundos.
3. Al llegar a la última imagen, volver a la primera.
4. Si solo hay una imagen, no iniciar intervalo.
5. Si hay cero imágenes válidas, mostrar placeholder.

Ejemplo de comportamiento esperado:

```text
Foto 1 → 15 segundos → Foto 2 → 15 segundos → Foto 3 → 15 segundos → Foto 4 → vuelve a Foto 1
```

---

## 7. Transición visual esperada

La transición debe sentirse premium y coherente con la estética neón.

Requerimientos visuales:

- transición tipo fade suave;
- leve glow fucsia al cambiar;
- evitar parpadeos fuertes;
- mantener borde neón alrededor de la portada;
- mantener overlay CRT/scanlines si ya existe;
- mantener proporción visual de la portada;
- usar `object-fit: cover` para que las imágenes llenen bien el marco sin deformarse.

CSS sugerido:

```css
.spotify-cover-img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition:
        opacity 420ms ease,
        filter 420ms ease,
        transform 420ms ease;
}

.spotify-cover-img.is-changing {
    opacity: 0.35;
    filter: blur(1px) drop-shadow(0 0 18px #ff007f);
    transform: scale(1.015);
}
```

No es obligatorio usar exactamente ese CSS, pero el resultado debe lograr ese efecto.

---

## 8. Estilo premium tipo Spotify + neon acrylic lamp

Aprovechar este cambio para pulir el look del componente sin rediseñarlo completamente.

Quiero que se sienta más como un reproductor premium:

- portada con marco limpio;
- controles alineados;
- barra de progreso visualmente clara;
- glow fucsia controlado;
- glassmorphism bien integrado;
- sin aspecto improvisado;
- sin romper la estética 8-bit.

Mantener:

- fuente pixelada;
- estética retro;
- colores fucsia/rosa/blanco;
- sensación de lámpara acrílica de neón;
- visualizador/waveform si ya existe;
- controles `Play`, `Pause`, `+5s`, `-5s`.

---

## 9. Integración con el componente actual

No crear un segundo reproductor desde cero si ya existe el componente.

Modificar el componente actual, probablemente ubicado en:

```text
ui/spotify_capsule.py
```

O el archivo equivalente que renderiza el player.

Buscar la lógica actual de:

```python
cover_image_path
```

Y reemplazarla por una lógica compatible con:

```python
cover_image_paths
```

sin romper la compatibilidad con `cover_image_path`.

---

## 10. Validaciones esperadas

Validar localmente con:

```powershell
$env:USE_STATIC_DATA="true"
streamlit run app/main.py
```

Confirmar:

- la app carga completa;
- la cápsula aparece;
- la primera imagen aparece correctamente;
- cada 15 segundos cambia de imagen;
- no hay distorsión de las fotos;
- no hay parpadeo brusco;
- los controles de audio siguen funcionando;
- la barra de progreso sigue funcionando;
- el fragmento de audio sigue reproduciéndose;
- `lyrics_data` o RPG Dialog no se rompe;
- Streamlit Cloud sigue siendo compatible.

---

## 11. Pruebas y robustez

Agregar o ajustar tests si el proyecto ya tiene pruebas para este componente.

Validar como mínimo:

- config con `cover_image_paths` múltiple;
- config con una sola imagen;
- config legacy con `cover_image_path`;
- config sin imágenes válidas;
- que el componente no falle al serializar la configuración.

Si el proyecto no tiene tests específicos para HTML/componentes, al menos agregar validaciones defensivas en Python.

---

## 12. Documentación requerida

Actualizar la documentación correspondiente, probablemente:

```text
docs/content_configuration.md
docs/codex_session_debug.md
```

Explicar:

1. dónde poner las imágenes del carrusel;
2. cómo configurar `cover_image_paths`;
3. cómo cambiar `cover_rotation_seconds`;
4. cómo mantener una sola portada usando `cover_image_path`;
5. qué pasa si una imagen no existe;
6. cómo probar localmente antes de hacer commit/push.

---

## 13. Restricciones

- No tocar ETL.
- No tocar queries.
- No tocar `data/final/landing_data.json` salvo que sea estrictamente necesario.
- No romper el modo `USE_STATIC_DATA=true`.
- No reemplazar el reproductor completo si puede modificarse el existente.
- No eliminar la reproducción de audio.
- No eliminar `lyrics_data`.
- No generar ni descargar assets externos.
- No introducir dependencias nuevas innecesarias.
- No cambiar la estética general de la landing fuera de este componente.

---

## 14. Entregable esperado

Devuélveme:

1. archivos creados/modificados;
2. código completo de los archivos modificados;
3. explicación breve del cambio;
4. instrucciones para poner las imágenes en `ui/assets/images/`;
5. instrucciones para probar localmente;
6. advertencias si alguna imagen configurada no existe.

---

## 15. Nota sobre una implementación futura

Más adelante voy a pedir otro botón/componente para renderizar una carta/invitación romántica estilo pergamino viejo y redirigir a un TikTok del lugar al que quiero invitar a mi novia por su cumpleaños.

No implementar eso todavía.

Este prompt es únicamente para:

```text
Carrusel de imágenes dentro de SpotifyCapsule.
```
