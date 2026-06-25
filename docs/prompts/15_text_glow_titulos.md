# Prompt para Codex — aplicar text glow fucsia a títulos negros

Quiero aplicar una mejora visual puntual en la landing romántica sin cambiar el diseño general.

## Objetivo

Aplicar un efecto **text glow / neon glow text effect** en color fucsia a los títulos principales que actualmente se ven negros u oscuros, especialmente los títulos de secciones y títulos de gráficos.

El efecto debe parecerse al brillo que ya tiene el título principal del hero: **“Nuestra historia”**.

---

## Contexto visual

En el hero, el texto **“Nuestra historia”** tiene un brillo fucsia suave detrás de la letra. Quiero replicar esa misma técnica visual en los otros títulos negros de la página.

La técnica esperada es CSS con `text-shadow`, por ejemplo:

```css
text-shadow:
    0 0 12px rgba(212, 20, 114, 0.32),
    0 0 28px rgba(255, 95, 183, 0.22);
```

No quiero un cambio agresivo ni exagerado. Debe ser un glow elegante, romántico y sutil.

---

## Alcance

Aplicar el efecto a todos los títulos visuales principales que actualmente se ven negros/oscuros y que estén estandarizados mediante clases CSS existentes.

Prioridad de clases probables:

- títulos de sección;
- títulos de cards;
- títulos de gráficos;
- encabezados principales dentro de cada bloque visual.

Buscar clases similares a:

```css
.section-title
.chart-title
.metric-title
.card-title
.timeline-title
.quote-title
.language-title
```

No es obligatorio que existan exactamente esas clases. Codex debe inspeccionar el CSS y los componentes actuales para encontrar las clases reales.

---

## Reglas visuales

1. Mantener el color base oscuro actual de los títulos.
2. Agregar glow fucsia con `text-shadow`.
3. No cambiar tamaños de fuente.
4. No cambiar familias tipográficas.
5. No cambiar layout.
6. No cambiar márgenes ni espaciados salvo que sea estrictamente necesario.
7. No aplicar el efecto a textos largos, párrafos, captions, tooltips ni ejes de gráficos.
8. No aplicar glow a todo el body.
9. El efecto debe ser sutil y premium, no neón excesivo.

---

## Implementación esperada

Agregar una regla CSS reutilizable, por ejemplo:

```css
.romantic-title-glow {
    text-shadow:
        0 0 10px rgba(212, 20, 114, 0.30),
        0 0 24px rgba(255, 95, 183, 0.20),
        0 4px 18px rgba(63, 36, 53, 0.10);
}
```

Luego aplicarla a los selectores reales que ya usa el proyecto, por ejemplo:

```css
.section-title,
.chart-title,
.card-title,
.timeline-title {
    text-shadow:
        0 0 10px rgba(212, 20, 114, 0.30),
        0 0 24px rgba(255, 95, 183, 0.20),
        0 4px 18px rgba(63, 36, 53, 0.10);
}
```

Si el proyecto ya tiene una clase o regla para el glow del hero, reutilizarla o extraerla a una clase común para evitar duplicación.

---

## Restricciones

- No rediseñar la landing.
- No tocar la lógica ETL.
- No tocar queries.
- No modificar datos.
- No cambiar el contenido textual.
- No cambiar el orden de secciones.
- No romper `reveal-on-scroll`.
- No tocar gráficos salvo que sea necesario para el título externo renderizado en HTML/CSS.
- No aplicar glow a labels de ejes de Altair/Plotly.

---

## Accesibilidad y legibilidad

El glow debe mejorar la estética sin bajar contraste.

Si algún título queda menos legible, reducir intensidad del glow. El texto debe seguir leyéndose claro sobre fondo rosado.

Respetar `prefers-reduced-motion`. Como este cambio es estático y no animado, no hace falta agregar animaciones.

---

## Documentación requerida

Documentar el cambio en el archivo de debug o cierre de sesión del proyecto, por ejemplo:

```text
docs/codex_session_debug.md
```

o el documento equivalente existente.

Agregar una sección breve:

```md
## Ajuste visual: glow fucsia en títulos

- Se aplicó un efecto `text-shadow` fucsia suave a los títulos principales de secciones/cards/gráficos.
- El objetivo fue replicar de forma sutil el brillo visual del hero “Nuestra historia”.
- Archivos modificados: [...]
- No se modificó la lógica ETL ni la estructura de datos.
```

También documentar en qué script/archivo CSS quedó implementado el cambio.

---

## Resultado esperado

Los títulos negros/oscuros de la landing, especialmente los de la sección de gráficos como:

- “Cuando mas nos encontramos”;
- “Nuestra hora favorita para hablar”;
- “Los dias donde mas nos encontramos”;
- otros títulos equivalentes;

se deben ver con un brillo fucsia sutil, coherente con el título principal **“Nuestra historia”**.

---

## Formato de respuesta

Devuélveme:

1. archivos modificados;
2. código completo o diff claro por archivo;
3. breve explicación de qué selector CSS se modificó;
4. confirmación de que no se tocó lógica ETL ni datos.
