# Prompt para Codex: implementar solo animaciones reveal-on-scroll y documentar ajuste UX

Actúa como un desarrollador Python/Streamlit senior especializado en frontend, CSS y documentación técnica.

## Contexto

Estoy trabajando en una app Streamlit ubicada en:

```text
C:\Users\User\OneDrive\Escritorio\landing_page
```

La app es una landing romántica basada en datos de WhatsApp e Instagram. El backend/ETL, la configuración de contenido, el orden de secciones y la parametrización de mensajes ya están implementados.

No modifiques ETL, queries, schema de base de datos, lógica de mensajes, `content_config.py` ni orden de secciones salvo que sea estrictamente necesario para aplicar clases CSS de animación.

## Objetivo único

Implementar el ajuste UX:

```md
## Ajuste UX: animaciones reveal-on-scroll
```

La landing se ve demasiado estática. Necesito que las secciones y tarjetas aparezcan suavemente al hacer scroll hacia abajo.

El efecto técnico deseado se llama:

```text
reveal-on-scroll
scroll reveal animation
fade-up on scroll
scroll-triggered animation
staggered reveal animation
```

La implementación recomendada es:

```text
Intersection Observer API + CSS transitions
```

---

# Comportamiento visual esperado

Cuando el usuario haga scroll, los elementos deben entrar suavemente desde abajo hacia arriba.

Estado inicial:

```css
opacity: 0;
transform: translateY(28px);
```

Estado visible:

```css
opacity: 1;
transform: translateY(0);
```

La animación debe sentirse:

- sutil;
- romántica;
- premium;
- fluida;
- elegante;
- no exagerada.

Duración recomendada:

```text
650ms - 850ms
```

Easing recomendado:

```css
cubic-bezier(0.22, 1, 0.36, 1)
```

---

# Elementos donde aplicar animación

Aplicar `reveal-on-scroll` a:

- secciones principales;
- cards de métricas;
- bento cards;
- tarjetas de timeline;
- tarjetas de frases bonitas;
- mensaje especial;
- gráficos de “nuestro ritmo”;
- bloques de cierre emocional.

No aplicar animaciones excesivas a cada texto interno individual.

---

# CSS requerido

Agregar o integrar en el CSS centralizado algo equivalente a:

```css
.reveal-on-scroll {
    opacity: 0;
    transform: translateY(28px);
    transition:
        opacity 760ms cubic-bezier(0.22, 1, 0.36, 1),
        transform 760ms cubic-bezier(0.22, 1, 0.36, 1);
    transition-delay: var(--reveal-delay, 0ms);
    will-change: opacity, transform;
}

.reveal-on-scroll.is-visible {
    opacity: 1;
    transform: translateY(0);
}

@media (prefers-reduced-motion: reduce) {
    .reveal-on-scroll {
        opacity: 1;
        transform: none;
        transition: none;
    }
}
```

Si hay cards repetidas, agregar delay progresivo:

```html
<article class="quote-card reveal-on-scroll" style="--reveal-delay: 120ms;">
```

---

# JavaScript requerido

Inyectar JavaScript de manera segura en Streamlit.

Usar `IntersectionObserver`.

Ejemplo base:

```html
<script>
(function () {
    const revealElements = document.querySelectorAll('.reveal-on-scroll');

    if (!('IntersectionObserver' in window)) {
        revealElements.forEach((element) => element.classList.add('is-visible'));
        return;
    }

    const observer = new IntersectionObserver((entries, observerInstance) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                entry.target.classList.add('is-visible');
                observerInstance.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.14,
        rootMargin: '0px 0px -40px 0px'
    });

    revealElements.forEach((element) => observer.observe(element));
})();
</script>
```

## Consideración importante de Streamlit

Streamlit puede re-renderizar el DOM, por tanto:

1. El script debe poder ejecutarse después de que las secciones se rendericen.
2. No debe duplicar listeners problemáticos.
3. No debe mostrarse como texto en pantalla.
4. Si `st.markdown(..., unsafe_allow_html=True)` no ejecuta correctamente el script, usar:

```python
import streamlit.components.v1 as components
components.html(script_html, height=0)
```

5. La app no debe romperse si el navegador no soporta `IntersectionObserver`; en ese caso los elementos deben mostrarse visibles.

---

# Clase reutilizable

Usar esta clase para animar elementos:

```text
reveal-on-scroll
```

Ejemplo:

```html
<section class="romantic-section reveal-on-scroll">
    ...
</section>
```

Para retrasos:

```html
<article class="quote-card reveal-on-scroll" style="--reveal-delay: 120ms;">
    ...
</article>
```

---

# No instalar librerías externas

No instalar:

```text
AOS
GSAP
anime.js
Framer Motion
```

No son necesarias.

Usar CSS + JavaScript nativo.

---

# Documentación obligatoria

Actualizar o crear:

```text
docs/codex_session_debug.md
```

Agregar esta sección:

```md
## Ajuste UX: animaciones reveal-on-scroll

### Motivo

La landing se veía estática. Se agregó una animación suave para que las secciones y tarjetas aparezcan hacia arriba al scrollear.

### Técnica usada

Intersection Observer API + CSS transitions.

### Archivos afectados

Listar rutas relativas de archivos modificados.

### Cómo funciona

Explicar brevemente:
- clase `reveal-on-scroll`;
- clase `is-visible`;
- variable CSS `--reveal-delay`;
- respeto a `prefers-reduced-motion`.

### Cómo activar la animación en nuevas tarjetas

Agregar:

```html
class="reveal-on-scroll"
```

Opcionalmente agregar:

```html
style="--reveal-delay: 120ms;"
```

### Resultado esperado

Las secciones y tarjetas aparecen con fade-up progresivo al entrar en viewport.
```

Si existe:

```text
docs/content_configuration.md
```

agregar una sección breve:

```md
## Animaciones al hacer scroll

El efecto se llama `reveal-on-scroll` o `fade-up on scroll`.

Para activar la animación en una nueva tarjeta o sección, agregar la clase:

```html
reveal-on-scroll
```

Para retraso progresivo, usar:

```html
style="--reveal-delay: 120ms;"
```

La animación respeta `prefers-reduced-motion`.
```

---

# Validación obligatoria

Ejecutar la app:

```powershell
streamlit run app/main.py
```

Validar visualmente:

1. Las secciones no aparecen todas de golpe.
2. Las cards aparecen suavemente hacia arriba al scrollear.
3. No se muestra JavaScript ni HTML como texto.
4. No se rompe el renderizado de tarjetas existentes.
5. La landing mantiene el diseño romántico actual.
6. La app sigue funcionando si la animación no se ejecuta.
7. `prefers-reduced-motion` está contemplado en CSS.

---

# Restricciones

No modificar ETL.

No modificar schema de base de datos.

No modificar queries.

No cambiar mensajes configurados.

No cambiar `ROMANTIC_CONTENT`.

No cambiar el orden de secciones.

No reescribir la app completa.

No instalar librerías de animación.

No renderizar JS como texto visible.

No romper HTML existente.

---

# Formato de respuesta esperado

Devuelve únicamente:

1. Rutas de archivos modificados.
2. Contenido completo de cada archivo modificado.
3. Contenido actualizado de `docs/codex_session_debug.md`.
4. Contenido actualizado de `docs/content_configuration.md`, solo si fue modificado.

No agregues explicaciones adicionales fuera de los archivos.
