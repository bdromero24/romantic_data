# Prompt para Codex: ajustes visuales finales de la landing romántica

Actúa como un Diseñador UI y Desarrollador Frontend experto en Streamlit, CSS, visual storytelling y experiencia de usuario.

## Contexto

Estoy trabajando en una landing romántica en Streamlit ubicada en:

```text
C:\Users\User\OneDrive\Escritorio\landing_page
```

La landing ya funciona, el backend/ETL ya está listo y la animación `reveal-on-scroll` quedó implementada correctamente. No modificar ETL, schema, queries ni lógica de base de datos.

El objetivo de esta sesión es hacer ajustes visuales finos para que la landing se vea más pulida, romántica, premium y consistente.

---

# Objetivo general

Mejorar la calidad visual de la landing sin cambiar la arquitectura ni romper funcionalidad existente.

Trabajar únicamente sobre:

- CSS;
- componentes visuales;
- estilos de tarjetas;
- estilos de gráficos;
- tipografía;
- espaciado;
- grosor de textos;
- burbujas tipo chat;
- documentación de cambios.

---

# 1. Grosor tipográfico general

Actualmente algunos textos se ven demasiado delgados. No quiero agrandar mucho la fuente; quiero que se vea más gruesa, legible y premium.

## Tarea

Ajustar `font-weight` en CSS para reforzar:

- títulos de sección;
- subtítulos importantes;
- labels de tarjetas;
- textos de mensajes;
- números de métricas;
- fechas;
- valores de ejes en gráficos;
- labels de gráficos.

## Dirección visual

No aumentar significativamente el tamaño de fuente. El cambio debe sentirse como más peso visual, no como texto más grande.

Usar pesos similares:

```css
font-weight: 650;
font-weight: 700;
font-weight: 750;
font-weight: 800;
```

## CSS sugerido

Adaptar al CSS actual:

```css
.section-title,
.romantic-section h2,
.timeline-title,
.quote-sender,
.ig-chat-title,
.metric-label,
.bento-card-title {
    font-weight: 800;
}

.quote-text,
.timeline-detail,
.ig-bubble,
.ig-bubble p,
.manual-subtitle,
.section-subtitle {
    font-weight: 650;
}

.metric-value,
.kpi-value,
.stat-value,
.date-pill,
.ig-bubble-meta {
    font-weight: 800;
}
```

---

# 2. Reforzar ejes y textos de gráficos

Los valores de los ejes de los gráficos se ven demasiado delgados.

## Tarea

Si los gráficos usan Plotly, ajustar layout para usar fuentes más gruesas y/o aplicar CSS sobre SVG.

## Plotly

Revisar dónde se construyen los gráficos y aplicar algo equivalente:

```python
fig.update_layout(
    font=dict(
        family="Nunito, Quicksand, Inter, sans-serif",
        color="#3f2435",
        size=14,
    ),
    xaxis=dict(
        tickfont=dict(
            family="Nunito, Quicksand, Inter, sans-serif",
            color="#8a5872",
            size=13,
        ),
        title_font=dict(
            family="Nunito, Quicksand, Inter, sans-serif",
            color="#3f2435",
            size=15,
        ),
    ),
    yaxis=dict(
        tickfont=dict(
            family="Nunito, Quicksand, Inter, sans-serif",
            color="#8a5872",
            size=13,
        ),
        title_font=dict(
            family="Nunito, Quicksand, Inter, sans-serif",
            color="#3f2435",
            size=15,
        ),
    ),
)
```

Si Plotly no respeta `font-weight`, aplicar CSS:

```css
.js-plotly-plot .xtick text,
.js-plotly-plot .ytick text,
.js-plotly-plot .gtitle,
.js-plotly-plot .legendtext,
.js-plotly-plot .annotation-text {
    font-weight: 700 !important;
}
```

## Altair

Si se usa Altair, configurar labels/títulos con `fontWeight` cuando aplique:

```python
axis=alt.Axis(
    labelFontWeight="bold",
    titleFontWeight="bold",
)
```

---

# 3. Burbujas tipo Instagram para mensajes especiales

Quiero que la sección de mensajes especiales pueda verse como conversación o mensajes tipo Instagram, con burbujas románticas usando blanco, rosa y fucsia.

## Tarea

Revisar la sección:

```text
Un mensaje que quiero guardar
```

y mejorar visualmente los mensajes si ya existen como cards.

## Estilo esperado

### Mensajes de ella

- alineados a la izquierda;
- fondo blanco o rosa muy claro;
- borde rosa/fucsia suave;
- texto oscuro;
- sombra suave;
- borde inferior izquierdo menos redondeado para parecer burbuja.

### Mensajes míos

- alineados a la derecha;
- fondo degradado fucsia/rosado;
- texto blanco;
- sombra fucsia suave;
- borde inferior derecho menos redondeado.

## CSS sugerido

Adaptar al CSS actual:

```css
.ig-chat-card {
    width: 100%;
    padding: 1.4rem;
    border-radius: 28px;
    background:
        linear-gradient(145deg, rgba(255, 255, 255, 0.72), rgba(255, 218, 238, 0.72));
    border: 1px solid rgba(212, 20, 114, 0.28);
    box-shadow: 0 20px 55px rgba(212, 20, 114, 0.16);
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    margin: 1rem 0;
}

.ig-message-list {
    display: flex;
    flex-direction: column;
    gap: 0.85rem;
}

.ig-bubble {
    max-width: min(78%, 620px);
    padding: 0.9rem 1rem;
    border-radius: 24px;
    font-weight: 650;
    line-height: 1.45;
    box-shadow: 0 12px 28px rgba(80, 30, 60, 0.10);
}

.ig-bubble p {
    margin: 0;
    font-weight: 650;
}

.ig-bubble-her {
    align-self: flex-start;
    background: rgba(255, 255, 255, 0.84);
    color: var(--text-main);
    border: 1px solid rgba(255, 95, 183, 0.30);
    border-bottom-left-radius: 8px;
}

.ig-bubble-me {
    align-self: flex-end;
    background: linear-gradient(135deg, #ff5fb7 0%, #d41472 48%, #a90058 100%);
    color: #ffffff;
    border: 1px solid rgba(255, 255, 255, 0.30);
    border-bottom-right-radius: 8px;
    box-shadow: 0 18px 36px rgba(212, 20, 114, 0.28);
}

.ig-bubble-meta {
    display: block;
    margin-top: 0.45rem;
    font-size: 0.78rem;
    font-weight: 800;
    opacity: 0.76;
}

.ig-bubble-me .ig-bubble-meta {
    color: rgba(255, 255, 255, 0.88);
}

.ig-bubble-her .ig-bubble-meta {
    color: var(--text-muted);
}

@media (max-width: 640px) {
    .ig-bubble {
        max-width: 92%;
    }
}
```

---

# 4. Mejorar consistencia de cards

Revisar que las cards principales tengan consistencia visual.

## Tarea

Unificar:

- border-radius;
- padding;
- sombras;
- bordes fucsia;
- background glassmorphism;
- hover state;
- spacing entre cards.

## Estilo esperado

Las cards deben verse como parte del mismo sistema visual:

```css
border-radius: 24px;
border: 1px solid rgba(212, 20, 114, 0.25);
box-shadow: 0 18px 50px rgba(212, 20, 114, 0.14);
background: rgba(255, 255, 255, 0.58);
backdrop-filter: blur(18px);
```

En hover:

```css
transform: translateY(-3px);
border-color: rgba(212, 20, 114, 0.55);
box-shadow: 0 24px 70px rgba(212, 20, 114, 0.22);
```

No exagerar el hover.

---

# 5. Mejorar degradados rosa/fucsia

El diseño debe mantener una presencia clara de rosa y fucsia. No debe volver a sentirse blanco plano.

## Tarea

Revisar fondo general, cards destacadas y botones.

El fondo puede usar algo como:

```css
[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(circle at top left, rgba(255, 46, 151, 0.24), transparent 34%),
        radial-gradient(circle at top right, rgba(212, 20, 114, 0.20), transparent 36%),
        linear-gradient(135deg, #fff0f8 0%, #ffd6ec 42%, #fff5fa 100%);
}
```

Mantener legibilidad.

---

# 6. Gloss/glitter sutil en acentos fucsia

Agregar o revisar un detalle visual tipo gloss/glitter en elementos fucsia importantes.

## Aplicar solo en:

- títulos principales;
- badges;
- botones principales;
- cards destacadas;
- mensaje especial;
- primer “te amo”.

## No aplicar en todo

El efecto debe ser sutil y elegante.

## CSS sugerido

```css
.glossy-fuchsia-text {
    display: inline-block;
    background: linear-gradient(
        180deg,
        #fff6fb 0%,
        #ff8ccc 22%,
        #ff2f9b 48%,
        #b80061 78%,
        #fff0fa 100%
    );
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    text-shadow:
        0 1px 0 rgba(255, 255, 255, 0.75),
        0 8px 24px rgba(212, 20, 114, 0.30),
        0 0 28px rgba(255, 95, 183, 0.34);
}

.glitter-accent {
    position: relative;
    overflow: hidden;
}

.glitter-accent::after {
    content: "";
    position: absolute;
    inset: -40%;
    background:
        radial-gradient(circle, rgba(255, 255, 255, 0.85) 0 1px, transparent 2px),
        linear-gradient(
            110deg,
            transparent 0%,
            transparent 38%,
            rgba(255, 255, 255, 0.55) 48%,
            transparent 58%,
            transparent 100%
        );
    background-size: 28px 28px, 220% 100%;
    opacity: 0.28;
    transform: translateX(-40%);
    animation: romantic-glitter-sweep 4.8s ease-in-out infinite;
    pointer-events: none;
}

@keyframes romantic-glitter-sweep {
    0% {
        transform: translateX(-45%) rotate(8deg);
        opacity: 0;
    }
    35% {
        opacity: 0.18;
    }
    55% {
        opacity: 0.38;
    }
    100% {
        transform: translateX(45%) rotate(8deg);
        opacity: 0;
    }
}

@media (prefers-reduced-motion: reduce) {
    .glitter-accent::after {
        animation: none;
        opacity: 0.16;
    }
}
```

---

# 7. Mantener reveal-on-scroll intacto

La animación `reveal-on-scroll` ya quedó bien.

## Reglas

- No eliminarla.
- No cambiar su comportamiento salvo que sea necesario por CSS.
- No romper `is-visible`.
- No cambiar el observer.
- Asegurar que nuevas cards mantengan la clase `reveal-on-scroll` si corresponde.

---

# 8. Documentación obligatoria

Actualizar:

```text
docs/codex_session_debug.md
```

Agregar sección:

```md
## Ajustes visuales finales

### Motivo

La landing ya funciona y la animación reveal-on-scroll quedó bien. Se hicieron ajustes visuales para mejorar grosor tipográfico, consistencia de cards, burbujas tipo Instagram y legibilidad de gráficos.

### Archivos afectados

Listar rutas relativas.

### Cambios aplicados

- Grosor tipográfico general.
- Refuerzo visual de ejes de gráficos.
- Mejora de cards.
- Mejora de burbujas tipo Instagram.
- Ajustes de degradado rosa/fucsia.
- Gloss/glitter sutil en acentos fucsia.
- Conservación de reveal-on-scroll.

### Resultado esperado

La landing mantiene el estilo romántico, pero se ve más pulida, más premium, más legible y menos plana.
```

Si existe:

```text
docs/content_configuration.md
```

actualizar solo si se agregan clases o instrucciones útiles para futuras cards.

---

# Validación

Ejecutar:

```powershell
streamlit run app/main.py
```

Verificar visualmente:

1. La app carga sin errores.
2. Los textos se ven más gruesos, no necesariamente más grandes.
3. Los valores de ejes de gráficos son más legibles.
4. Las cards tienen consistencia visual.
5. El fondo mantiene rosa/fucsia visible.
6. Las burbujas tipo Instagram se ven correctas.
7. El gloss/glitter es sutil.
8. La animación reveal-on-scroll sigue funcionando.
9. No aparece HTML ni CSS crudo en pantalla.
10. No se modificó ETL ni lógica de base de datos.

---

# Restricciones

No modificar ETL.

No modificar schema de base de datos.

No cambiar normalización.

No cambiar queries salvo que sea estrictamente necesario para estilos de gráficos.

No cambiar contenido configurado.

No romper reveal-on-scroll.

No instalar librerías nuevas.

No exponer errores técnicos en UI.

No renderizar HTML como texto.

---

# Formato de respuesta esperado

Devuelve únicamente:

1. Rutas de archivos modificados.
2. Contenido completo de cada archivo modificado.
3. Contenido actualizado de `docs/codex_session_debug.md`.
4. Contenido actualizado de `docs/content_configuration.md`, solo si fue modificado.

No agregues explicaciones adicionales fuera de los archivos.
