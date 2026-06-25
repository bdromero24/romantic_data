# Prompt 02 - Refactor visual Streamlit romantico premium

## Rol

Actua como un disenador UI y desarrollador frontend experto en Streamlit.

Tengo un dashboard en Python/Streamlit que procesa datos de WhatsApp e Instagram mediante pipeline ETL y posiblemente NLP en backend. El diseno actual es demasiado tecnico, frio y cercano a un dashboard de ingenieria.

Necesito reestructurar visualmente la interfaz para convertirla en una landing page romantica premium para mi novia.

## Objetivo de esta sesion

Refactorizar exclusivamente la capa visual y de experiencia de usuario de la app Streamlit.

Esta sesion debe enfocarse en:

- CSS personalizado.
- Paleta romantica.
- Layout visual.
- Cards.
- Bento grid.
- Glassmorphism.
- Tipografia.
- Espaciado.
- Responsividad mobile-first.
- Estilizacion de Plotly/Altair.

No implementar ETL nuevo.
No implementar NLP nuevo.
No mover logica pesada al frontend.
No cambiar la arquitectura backend salvo que sea estrictamente necesario para renderizar la pagina.

## Uso obligatorio de CSS en Streamlit

Inyectar CSS personalizado usando:

```python
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
```

Centralizar el CSS en una constante clara, por ejemplo:

```python
CUSTOM_CSS = """
<style>
...
</style>
"""
```

Si la estructura del proyecto lo permite, mover estilos a un modulo dedicado, por ejemplo:

```text
ui/styles.py
```

Y consumirlo desde la app principal.

## Uso de skill visual

Usar la skill `tasteskill` para estandarizar el sistema visual de la interfaz.

La skill debe aplicarse para asegurar consistencia en:

- Paleta de colores.
- Tipografia.
- Fondo.
- Alineacion.
- Spacing.
- Padding.
- Bordes.
- Cards.
- Estados hover.
- Jerarquia visual.
- Responsividad.

## 1. Paleta de colores romantica y premium

Reemplazar el look de ingenieria por una paleta limpia, romantica y elegante.

Usar:

```css
--color-bg: #fff7fb;
--color-bg-soft: #ffeaf4;
--color-surface: rgba(255, 255, 255, 0.62);
--color-surface-strong: rgba(255, 255, 255, 0.82);
--color-pink-soft: #ffd1e5;
--color-pink: #ff8fc7;
--color-fuchsia: #ff2d95;
--color-fuchsia-deep: #c2186a;
--color-text: #3a2430;
--color-muted: #8a5c72;
--color-border: rgba(255, 45, 149, 0.26);
--color-glow: rgba(255, 45, 149, 0.28);
```

Reglas:

- Fondo principal blanco/rosa muy suave.
- Acentos y botones en fucsia vibrante.
- Evitar negro puro.
- Evitar dark mode.
- Evitar grises corporativos.
- Evitar colores tecnicos tipo azul dashboard.

## 2. Glassmorphism y bordes glow

Redisenar contenedores y bloques visuales para que parezcan tarjetas de cristal esmerilado.

Aplicar a cards, secciones y metric blocks:

```css
background: rgba(255, 255, 255, 0.62);
backdrop-filter: blur(18px);
-webkit-backdrop-filter: blur(18px);
border: 1px solid rgba(255, 45, 149, 0.26);
border-radius: 28px;
box-shadow: 0 18px 45px rgba(194, 24, 106, 0.10);
```

Agregar hover sutil:

```css
box-shadow: 0 22px 60px rgba(255, 45, 149, 0.24);
transform: translateY(-2px);
```

Reglas:

- Bordes ultra finos de 1px en fucsia translúcido.
- Glow sutil, no exagerado.
- Transiciones suaves.
- Bordes redondeados grandes.
- Sensacion premium, no infantil.

## 3. Bento grid responsiva y mobile-first

Organizar las metricas de la historia en bloques visuales asimetricos, redondeados y adaptables.

La estructura debe parecer una bento grid:

- Cards grandes para metricas principales.
- Cards medianas para datos secundarios.
- Cards pequenas para detalles romanticos.
- Layout fluido.
- Mobile-first.

Ejemplo CSS sugerido:

```css
.bento-grid {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: 1rem;
  margin: 1.5rem 0;
}

.bento-card {
  grid-column: span 4;
}

.bento-card.large {
  grid-column: span 8;
}

.bento-card.full {
  grid-column: 1 / -1;
}

@media (max-width: 768px) {
  .bento-grid {
    grid-template-columns: 1fr;
  }

  .bento-card,
  .bento-card.large,
  .bento-card.full {
    grid-column: 1 / -1;
  }
}
```

Reglas:

- Pensar primero en celular.
- Evitar layouts que se rompan en pantallas pequenas.
- Evitar tablas anchas.
- No sobrecargar la pantalla con graficos.
- Mantener espacio vertical suficiente.

## 4. Estilizacion de graficos Plotly/Altair

Configurar las visualizaciones para que hereden la paleta romantica.

Para Plotly:

- Fondo transparente o rosa muy suave.
- Barras o lineas en degradado rosa/fucsia cuando aplique.
- Texto en `#3a2430`.
- Gridlines muy suaves.
- Sin plantillas oscuras.
- Sin colores default de Plotly.

Ejemplo de configuracion:

```python
fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(255,247,251,0.35)",
    font=dict(color="#3a2430", family="Inter, system-ui, sans-serif"),
    margin=dict(l=20, r=20, t=48, b=24),
)

fig.update_xaxes(
    gridcolor="rgba(255,45,149,0.10)",
    zerolinecolor="rgba(255,45,149,0.12)",
)

fig.update_yaxes(
    gridcolor="rgba(255,45,149,0.10)",
    zerolinecolor="rgba(255,45,149,0.12)",
)
```

Para Altair:

- Usar escalas rosa -> fucsia.
- Fondo transparente.
- Tipografia consistente.
- Ejes discretos.
- No usar paletas tecnicas.

Ejemplo de escala:

```python
scale=alt.Scale(range=["#ffd1e5", "#ff8fc7", "#ff2d95", "#c2186a"])
```

## 5. Tipografia hibrida

Usar fuentes Sans-Serif elegantes para:

- Titulos.
- Subtitulos.
- Textos descriptivos.
- Labels.
- Copy emocional.

Usar fuente Monospace solo para:

- Numeros clave.
- Fechas.
- Metricas duras.
- Conteos.

Ejemplo CSS:

```css
:root {
  --font-sans: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  --font-mono: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
}

h1, h2, h3, p, span, div {
  font-family: var(--font-sans);
}

.metric-number,
.date-pill,
.count-value {
  font-family: var(--font-mono);
}
```

## Componentes visuales esperados

Crear o refactorizar componentes como:

### Hero romantico

Debe incluir:

- Titulo grande.
- Subtitulo emocional.
- Fondo suave con degradado rosa/blanco.
- Elementos decorativos sutiles.

### Cards de metricas

Cada card debe tener:

- Label romantico.
- Numero grande en monospace.
- Descripcion breve.
- Glow hover.

### Timeline

Debe mostrar momentos importantes con tarjetas verticales o bloques suaves.

### Frases bonitas

Mostrar mensajes originales en cards elegantes.

No mostrar texto normalizado al usuario.

### Seccion de graficos suaves

Mostrar maximo los graficos necesarios.

Los graficos deben verse integrados en la landing, no como dashboard tecnico.

## Lenguaje visual y textual

Cambiar textos tecnicos por textos romanticos.

Ejemplos:

Incorrecto:

```text
Message count by hour
```

Correcto:

```text
Nuestra hora favorita para hablar
```

Incorrecto:

```text
Keyword frequency
```

Correcto:

```text
Las palabras que mas nos representan
```

Incorrecto:

```text
Sentiment analysis
```

Correcto:

```text
La energia bonita de nuestros mensajes
```

## Reglas especificas para Streamlit

1. Usar `st.set_page_config` con titulo romantico y layout wide.
2. Ocultar o suavizar elementos default de Streamlit si afectan la estetica.
3. Inyectar CSS con `st.markdown(..., unsafe_allow_html=True)`.
4. Evitar `st.metric` default si visualmente se ve tecnico; preferir HTML cards personalizadas.
5. Evitar tablas crudas.
6. Evitar `st.dataframe` en la vista principal.
7. Usar `st.columns` solo si no rompe la responsividad.
8. Si se requiere layout complejo, preferir HTML/CSS con bento grid.
9. Mantener funciones pequenas para renderizar cada seccion.
10. No poner SQL directamente en el archivo visual principal.

## Estructura sugerida

Si el proyecto lo permite, organizar asi:

```text
app.py
ui/
  styles.py
  components.py
  charts.py
services/
  romantic_metrics.py
```

Donde:

- `ui/styles.py` contiene CSS y constantes visuales.
- `ui/components.py` contiene hero, cards, timeline y secciones.
- `ui/charts.py` contiene helpers para Plotly/Altair.
- `services/romantic_metrics.py` consume backend/queries y devuelve datos listos para pintar.

Si la estructura actual es mas simple, refactorizar sin romper imports existentes.

## Restricciones

No implementar nuevas dependencias pesadas.
No implementar NLP nuevo.
No mostrar dark mode.
No usar estilos tecnicos.
No mostrar tablas crudas en la vista principal.
No romper el ETL existente.
No mover transformaciones pesadas a Streamlit.
No exponer errores internos al usuario final.

## Resultado esperado

La app debe verse como una landing page romantica, premium y personalizada.

Debe sentirse:

- Suave.
- Limpia.
- Femenina sin ser infantil.
- Romantica.
- Moderna.
- Mobile-first.
- Visualmente consistente.

## Output esperado

Devolver unicamente:

- rutas de archivos modificados;
- contenido completo de cada archivo modificado.

No incluir explicaciones adicionales.
