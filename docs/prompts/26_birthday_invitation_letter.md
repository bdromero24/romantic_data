# Requerimiento Técnico — `BirthdayInvitationLetter`

## 1. Contexto del proyecto

Estoy trabajando en una landing romántica desarrollada en **Python + Streamlit**. La aplicación ya tiene una estética visual consolidada:

- paleta rosa, blanco y fucsia;
- glassmorphism;
- neon glow;
- detalles 8-bit / pixel art;
- componentes personalizados renderizados con HTML/CSS/JS;
- despliegue en Streamlit Cloud;
- modo de datos congelados mediante `data/final/landing_data.json`.

Ya existe una sección/componente musical tipo cápsula/reproductor llamada conceptualmente `SpotifyCapsule`, inspirada en una lámpara acrílica neón de Spotify con estética 8-bit.

Después de esa sección musical, quiero agregar una nueva sección interactiva llamada:

```text
BirthdayInvitationLetter
```

Esta sección será una sorpresa/invitación de cumpleaños para mi novia.

---

## 2. Objetivo funcional

Implementar una nueva sección después de `SpotifyCapsule` que funcione como una **carta/invitación interactiva**.

El flujo visual aprobado es:

```text
SpotifyCapsule / Nuestra canción
        ↓ scroll
Sobre/carta cerrada con alitas y corazón
        ↓ click
Carta desplegada tipo pergamino viejo
        ↓ texto romántico + 2 botones externos
```

La carta será una invitación para pasar la noche de su cumpleaños en una de dos opciones de glamping/cabaña con jacuzzi y vista a la ciudad.

Conceptualmente, ambas opciones son lo mismo:

```text
una cabaña/glamping con jacuzzi y vista a la ciudad
```

pero deben mostrarse como **dos botones/enlaces distintos**, para que ella pueda ver las dos alternativas.

---

## 3. Decisión técnica aprobada

Usar:

```python
streamlit.components.v1.html()
```

El componente debe ser autocontenido en HTML/CSS/JS, similar a otros componentes visuales de la landing.

No usar modal externo ni librerías pesadas.

---

## 4. Archivos esperados

Crear:

```text
ui/birthday_invitation.py
```

Modificar:

```text
app/main.py
content_config.py
docs/content_configuration.md
docs/codex_session_debug.md
```

Si el proyecto usa otra ubicación real para `content_config.py`, respetar la arquitectura existente.

---

## 5. Nueva configuración en `content_config.py`

Agregar una configuración editable dentro de `ROMANTIC_CONTENT` o la estructura equivalente de configuración manual:

```python
"birthday_invitation": {
    "enabled": True,
    "closed_title": "Nueva carta para ti 💌",
    "closed_subtitle": "Toca para abrir tu invitación",
    "letter_title": "Querida Mar:",
    "letter_body": [
        "Tengo una invitación especial para ti.",
        "Quiero celebrar tu cumpleaños en un lugar bonito, tranquilo y con una vista increíble a la ciudad.",
        "Te invito a pasar una noche conmigo en una cabaña con jacuzzi y vista a la ciudad.",
        "Hay dos opciones que quiero mostrarte. La idea es que escojamos juntos el lugar donde vamos a guardar otro recuerdo bonito.",
        "No quiero que sea solo una salida. Quiero que sea una noche pensada para ti, para celebrar tu vida y para recordarte lo mucho que te amo."
    ],
    "signature": "Con amor, David",
    "primary_link_text": "Ver opción 1",
    "primary_link_url": "https://www.tiktok.com/...",
    "secondary_link_text": "Ver opción 2",
    "secondary_link_url": "https://www.tiktok.com/..."
}
```

### Reglas de configuración

- `enabled`: permite activar/desactivar el componente.
- `closed_title`: texto visible en el sobre cerrado.
- `closed_subtitle`: texto debajo del sobre cerrado.
- `letter_title`: título manuscrito de la carta.
- `letter_body`: párrafos editables de la carta.
- `signature`: firma final.
- `primary_link_text`: texto del primer botón.
- `primary_link_url`: link del primer glamping/cabaña.
- `secondary_link_text`: texto del segundo botón.
- `secondary_link_url`: link del segundo glamping/cabaña.

---

## 6. Componente Python esperado

Crear en `ui/birthday_invitation.py` una función principal:

```python
def render_birthday_invitation(config: dict) -> None:
    ...
```

Debe:

1. validar si `config.get("enabled")` está activo;
2. renderizar el componente con `components.html(...)`;
3. serializar la configuración de forma segura;
4. usar HTML/CSS/JS autocontenido;
5. no depender de la base de datos;
6. no depender de `landing_data.json`;
7. no romper Streamlit Cloud.

### Importaciones esperadas

```python
from __future__ import annotations

import html
import json

import streamlit.components.v1 as components
```

Se puede usar `html.escape()` para proteger textos configurables antes de inyectarlos en HTML.

---

## 7. Ubicación dentro de la landing

Modificar `app/main.py` para renderizar este componente **después del componente musical**.

Orden esperado:

```text
... secciones actuales
SpotifyCapsule / Nuestra canción
BirthdayInvitationLetter
... cierre o siguientes secciones si existen
```

Ejemplo conceptual:

```python
from ui.birthday_invitation import render_birthday_invitation

birthday_config = ROMANTIC_CONTENT.get("birthday_invitation", {})
render_birthday_invitation(birthday_config)
```

Si `SpotifyCapsule` también se controla desde `ROMANTIC_CONTENT`, mantener la misma convención.

---

## 8. Estado visual cerrado: sobre con alitas

El componente debe iniciar mostrando una sección tipo postal/cielo romántico.

### Elementos visuales

- fondo rosa pastel;
- nubes decorativas;
- corazones flotantes;
- sobre blanco con alitas;
- corazón en el centro del sobre;
- texto corto debajo;
- efecto `slide-up` o `float`;
- glow sutil fucsia;
- diseño centrado y responsive.

### Textos

Debe usar:

```python
closed_title
closed_subtitle
```

Ejemplo visual:

```text
Nueva carta para ti 💌
Toca para abrir tu invitación
```

### Interacción

Al hacer click en el sobre o en el área de invitación:

- ocultar/reducir el estado cerrado;
- desplegar la carta;
- aplicar animación suave tipo `slide-up`, `fade-in` o `unfold`.

---

## 9. Estado visual abierto: carta tipo pergamino viejo

Al abrirse, debe renderizar una carta inspirada en la imagen de referencia:

- papel viejo / pergamino claro;
- textura sutil;
- bordes suaves, ligeramente irregulares;
- sombra ligera;
- apariencia artesanal;
- tipografía manuscrita para título y firma;
- texto legible en tipografía limpia;
- sticker/corazón decorativo;
- sin imágenes de personas;
- sin fotografías circulares;
- sin imágenes externas obligatorias.

### Estructura visual esperada

```text
Querida Mar:

[párrafos de la carta]

[botón opción 1]
[botón opción 2]

Con amor, David
```

### Estilo de la carta

- Fondo tipo papel: beige claro, crema o pergamino suave.
- Mantener coherencia con la landing romántica.
- Puede incluir corazones dibujados tipo sticker.
- Puede tener clip decorativo o cinta visual si no complica el layout.
- Debe verse artesanal, no como un cuadro blanco genérico.

---

## 10. Botones externos

La carta debe incluir **dos botones**, no uno.

Los botones representan dos opciones de glamping/cabaña.

### Reglas

Cada botón debe abrir en nueva pestaña:

```html
target="_blank"
rel="noopener noreferrer"
```

Ejemplo:

```html
<a href="..." target="_blank" rel="noopener noreferrer">
  Ver opción 1
</a>
```

### Estilo

Los botones deben:

- mantener paleta fucsia/rosa;
- tener glow sutil;
- parecer botones románticos premium;
- no romper la estética de pergamino;
- ser claramente clickeables;
- funcionar en mobile.

---

## 11. Animación requerida

El estado cerrado debe tener una animación sutil:

- flotación del sobre;
- corazones moviéndose lentamente;
- glow suave;
- transición al abrir.

Al hacer click:

- desplegar carta con `slide-up`;
- aplicar `opacity` + `transform`;
- no recargar la página;
- no usar `st.button()`, salvo que sea estrictamente necesario.

Preferencia:

```text
interacción manejada dentro del HTML/JS del componente
```

---

## 12. CSS sugerido

Usar clases internas con prefijo para evitar conflictos:

```css
.birthday-invitation-root {}
.birthday-envelope-stage {}
.birthday-envelope {}
.birthday-envelope-wing {}
.birthday-letter {}
.birthday-letter-open {}
.birthday-heart-sticker {}
.birthday-link-button {}
```

### Paleta sugerida

```css
--birthday-pink: #ffd1ea;
--birthday-fuchsia: #ff007f;
--birthday-deep: #9d004f;
--birthday-paper: #f4e4c8;
--birthday-paper-dark: #d6b98e;
--birthday-ink: #3f2435;
--birthday-soft-shadow: rgba(157, 0, 79, 0.28);
```

### Tipografías sugeridas

Para título/firma manuscrita:

```css
font-family: "Dancing Script", "Great Vibes", cursive;
```

Para cuerpo:

```css
font-family: "Nunito", "Quicksand", system-ui, sans-serif;
```

Si ya existen fuentes globales en la landing, reutilizarlas.

---

## 13. Seguridad y serialización

Los textos y URLs vienen desde configuración. Por lo tanto:

- escapar textos con `html.escape`;
- serializar datos con `json.dumps(..., ensure_ascii=False)`;
- validar que URLs sean strings no vacíos;
- si un link no existe, no renderizar ese botón;
- no inyectar HTML arbitrario no escapado desde configuración;
- permitir emojis.

---

## 14. Fallbacks

Si `enabled=False`:

```text
no renderizar nada
```

Si falta `letter_body`:

```text
mostrar carta con mensaje fallback corto
```

Si falta un link:

```text
no mostrar ese botón
```

Si faltan ambos links:

```text
mostrar la carta sin botones, pero sin romper la app
```

---

## 15. Restricciones

No hacer lo siguiente:

- no tocar ETL;
- no tocar queries;
- no modificar `data/final/landing_data.json`;
- no romper `USE_STATIC_DATA=true`;
- no modificar `SpotifyCapsule`;
- no introducir dependencias externas innecesarias;
- no usar imágenes de personas dentro de la carta;
- no usar APIs externas;
- no requerir backend;
- no usar base de datos;
- no rediseñar toda la landing.

---

## 16. Validación local

Probar localmente con modo estático:

```powershell
$env:USE_STATIC_DATA="true"
streamlit run app/main.py
```

Validar:

1. la landing carga sin error;
2. `SpotifyCapsule` sigue funcionando;
3. después de la canción aparece el sobre/carta cerrada;
4. el sobre tiene alitas/corazón;
5. al hacer click se despliega la carta;
6. la carta se ve como pergamino viejo/papel romántico;
7. el texto configurado aparece correctamente;
8. los dos botones aparecen;
9. los dos botones abren los links en nueva pestaña;
10. no hay errores en consola de Streamlit;
11. funciona en desktop y mobile.

---

## 17. Documentación requerida

Actualizar:

```text
docs/content_configuration.md
```

Agregar sección:

```text
BirthdayInvitationLetter / Invitación de cumpleaños
```

Debe explicar:

- dónde se configura;
- cómo activar/desactivar;
- cómo editar título, cuerpo y firma;
- cómo cambiar los dos links;
- cómo probar localmente;
- que no depende de la base de datos.

Actualizar:

```text
docs/codex_session_debug.md
```

Agregar nota corta:

```text
Se agregó componente BirthdayInvitationLetter como sección interactiva posterior a SpotifyCapsule.
```

---

## 18. Entregable

Devolver:

1. archivos creados/modificados;
2. código completo por archivo;
3. explicación breve de integración;
4. pasos para probar localmente;
5. cualquier advertencia relevante.

---

## 19. Resultado esperado

Al finalizar, la landing debe tener una nueva experiencia:

```text
Después de la canción, el usuario sigue scrolleando.
Aparece una carta cerrada con alas y corazón.
Al tocarla, se abre una carta tipo pergamino viejo.
La carta invita a pasar una noche de cumpleaños en una cabaña/glamping con jacuzzi y vista a la ciudad.
La carta muestra dos botones externos: opción 1 y opción 2.
```

El resultado debe sentirse como una continuación emocional de la landing, no como un componente técnico aislado.
