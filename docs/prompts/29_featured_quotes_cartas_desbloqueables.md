# Prompt para Codex — convertir “Mensajes para volver a leer despacio” en cartas desbloqueables tipo sobre

## 1. Contexto

Estoy trabajando en una landing romántica hecha en **Python + Streamlit**. La app ya tiene estética consolidada:

- rosa, blanco y fucsia;
- glassmorphism;
- neon glow;
- detalles 8-bit / pixel art;
- componentes personalizados con HTML/CSS;
- secciones románticas y narrativas;
- datos congelados para Streamlit Cloud.

La sección actual:

```text
Mensajes para volver a leer despacio
```

muestra varias cards con mensajes seleccionados. Visualmente funcionan, pero ahora se ven demasiado simples: son recuadros rosados con borde fucsia.

Quiero convertir esas cards en una experiencia más bonita e interactiva, inspirada en una **carta/sobre romántico**. La idea es que cada mensaje esté inicialmente “bloqueado” o cerrado dentro de un sobre, y al pasar el mouse o hacer click se desbloquee/revele el mensaje, parecido a un efecto de cartas en juegos tipo memory/match cards.

---

## 2. Objetivo visual

Reemplazar las cards simples de la sección:

```text
Mensajes para volver a leer despacio
```

por cards interactivas tipo:

```text
sobre cerrado → hover/click → mensaje revelado
```

Inspiración visual:

- sobre rosa con corazón en el centro;
- alas/corazones opcionales;
- estética romántica/premium;
- mantener paleta rosa/fucsia/blanco;
- que se sienta como “abrir una carta”;
- no perder legibilidad;
- no rediseñar toda la landing.

---

## 3. Comportamiento esperado

Cada card debe tener dos estados:

### Estado cerrado

Al cargar la sección, cada card debe verse como un sobre/carta cerrada.

Debe mostrar, como mínimo:

```text
💌 Mensaje guardado
```

o un texto breve configurable/fallback como:

```text
Toca para abrir
```

Visualmente:

- sobre rosa;
- corazón en el centro;
- borde fucsia/neón;
- sombras suaves;
- fondo con textura o degradado;
- animación sutil de glow o flotación.

### Estado abierto

Al hacer hover o click:

- el sobre se abre o gira;
- se revela el mensaje real;
- aparece el texto, sender y fecha;
- mantiene el mismo tamaño aproximado de la card;
- no rompe la grilla;
- no desplaza bruscamente el layout.

---

## 4. Interacción desktop y mobile

Implementar una interacción que funcione bien en:

### Desktop

- `hover` puede revelar la card.
- También permitir click para fijar/revelar.

### Mobile

Como no existe hover confiable:

- el click/tap debe revelar la card.
- Si se vuelve a tocar, puede cerrarse o mantenerse abierta. Preferencia: que se mantenga abierta.

---

## 5. Implementación sugerida

Buscar el componente que renderiza las featured quotes o cards de:

```text
Mensajes para volver a leer despacio
```

Probablemente está en alguno de estos archivos:

```text
ui/components.py
ui/styles.py
ui/...
```

o en una función similar a:

```python
render_featured_quotes(...)
render_quote_card(...)
```

Modificar únicamente esa sección/cards.

---

## 6. Clases CSS sugeridas

Usar clases específicas para evitar romper otras cards:

```css
.love-letter-grid {}
.love-letter-card {}
.love-letter-inner {}
.love-letter-front {}
.love-letter-back {}
.love-letter-envelope {}
.love-letter-heart-seal {}
.love-letter-message {}
.love-letter-sender {}
.love-letter-date {}
```

Evitar reutilizar clases genéricas que afecten otras secciones.

---

## 7. Efecto visual sugerido

### Opción recomendada: flip card

Usar una estructura tipo:

```html
<article class="love-letter-card">
  <div class="love-letter-inner">
    <div class="love-letter-front">
      <!-- sobre cerrado -->
    </div>
    <div class="love-letter-back">
      <!-- mensaje revelado -->
    </div>
  </div>
</article>
```

Con CSS:

```css
.love-letter-card {
    perspective: 1200px;
}

.love-letter-inner {
    transform-style: preserve-3d;
    transition: transform 700ms ease;
}

.love-letter-card:hover .love-letter-inner,
.love-letter-card.is-open .love-letter-inner {
    transform: rotateY(180deg);
}

.love-letter-front,
.love-letter-back {
    backface-visibility: hidden;
}

.love-letter-back {
    transform: rotateY(180deg);
}
```

### Opción alternativa: apertura de sobre

Si el flip se complica, usar una animación más simple:

- sobre cerrado encima;
- al hover/click, el sobre se desvanece;
- el mensaje aparece con `opacity` y `translateY`.

La prioridad es estabilidad visual.

---

## 8. Diseño del sobre cerrado

El frente de la card debe parecer un sobre similar a la referencia:

- fondo rosa claro;
- solapas triangulares usando `linear-gradient` o pseudo-elementos;
- corazón/sello central fucsia;
- borde fucsia;
- glow suave;
- sombra romántica;
- no usar imagen externa obligatoria.

Ejemplo conceptual de CSS:

```css
.love-letter-front {
    background:
        linear-gradient(135deg, transparent 49%, rgba(255, 0, 127, 0.12) 50%),
        linear-gradient(225deg, transparent 49%, rgba(255, 0, 127, 0.10) 50%),
        linear-gradient(180deg, #ffe1f0, #ffc1df);
    border: 2px solid #ff4fab;
    box-shadow: 0 0 24px rgba(255, 0, 127, 0.28);
}
```

El sello/corazón puede hacerse con HTML/CSS:

```html
<div class="love-letter-heart-seal">♥</div>
```

---

## 9. Diseño del reverso/mensaje abierto

El reverso debe mantener el estilo romántico existente, pero más elaborado que la card actual:

- fondo tipo papel rosado/pergamino suave;
- borde fucsia más fino o glow;
- texto bien espaciado;
- sender en fucsia;
- fecha en tono muted;
- padding suficiente;
- tipografía consistente con la app.

No debe verse como un recuadro plano/simple.

---

## 10. Contenido a mostrar

Cuando la card esté abierta, debe mostrar lo mismo que actualmente:

```text
mensaje
sender
fecha
```

No cambiar los mensajes seleccionados, IDs, `message_key` ni lógica de datos.

Solo cambiar presentación/interacción.

---

## 11. JavaScript para click/tap

Si se usa `st.markdown(..., unsafe_allow_html=True)`, incluir un pequeño script si ya existe mecanismo de scripts en el proyecto.

Si ya existe un helper para inyectar JS o reveal observers, reutilizarlo.

El comportamiento esperado:

```javascript
document.querySelectorAll(".love-letter-card").forEach((card) => {
  card.addEventListener("click", () => {
    card.classList.add("is-open");
  });
});
```

Preferencia:

- en desktop, hover abre;
- en mobile, click abre;
- después de abierto, que permanezca abierto para que ella pueda leer tranquila.

Si el proyecto usa `components.html()` para scripts más complejos, evaluar si conviene encapsular esta sección o mantenerla con `st.markdown`.

---

## 12. Responsive

Mantener la grilla actual de 3 columnas en desktop si ya existe.

En tablet/mobile:

- 2 columnas o 1 columna según ancho;
- cards suficientemente altas para mostrar sobre y mensaje;
- evitar texto cortado;
- mantener tamaños consistentes.

Ejemplo:

```css
@media (max-width: 768px) {
    .love-letter-grid {
        grid-template-columns: 1fr;
    }
}
```

---

## 13. Accesibilidad básica

Cada card debe ser accesible como elemento clickeable:

- usar `role="button"` si aplica;
- `tabindex="0"`;
- soportar Enter/Espacio si se agrega JS;
- mantener contraste legible.

---

## 14. Restricciones

- No tocar ETL.
- No tocar queries.
- No modificar `content_config.py` salvo que sea estrictamente necesario.
- No modificar `landing_data.json`.
- No cambiar mensajes, IDs ni `message_key`.
- No romper otras secciones.
- No alterar `SpotifyCapsule`.
- No alterar `BirthdayInvitationLetter`.
- No introducir dependencias externas.
- No usar imágenes externas obligatorias.
- No convertir los mensajes a imágenes.
- El texto debe seguir siendo texto real HTML.

---

## 15. Validación local

Probar con:

```powershell
$env:USE_STATIC_DATA="true"
streamlit run app/main.py
```

Validar:

1. la landing carga sin errores;
2. la sección “Mensajes para volver a leer despacio” sigue apareciendo;
3. las cards ahora se ven como sobres/cartas cerradas;
4. al pasar el mouse o hacer click, se revela el mensaje;
5. el mensaje, sender y fecha se leen correctamente;
6. no hay recortes;
7. la grilla sigue alineada;
8. funciona en mobile;
9. no se dañan otras secciones.

---

## 16. Documentación

Actualizar si aplica:

```text
docs/codex_session_debug.md
```

Agregar nota corta:

```text
Se actualizó la sección featured quotes para renderizar mensajes como cartas/sobres desbloqueables con interacción hover/click.
```

Si existe documentación visual o de configuración:

```text
docs/content_configuration.md
```

agregar nota de que esta sección sigue alimentándose desde `featured_quotes`, pero ahora visualmente usa cartas desbloqueables.

---

## 17. Entregable

Devuélveme:

1. archivos modificados;
2. código completo por archivo;
3. explicación breve del cambio;
4. clases CSS nuevas;
5. cómo probar localmente;
6. confirmación de que no se tocaron ETL, queries ni datos congelados.
