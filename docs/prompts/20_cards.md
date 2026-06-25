Necesito modificar únicamente la sección **“Mensajes para volver a leer despacio”**.

## Objetivo

Los 9 mensajes que aparecen como cards/recuadros deben dejar de verse como cards rectangulares normales y pasar a verse como **pergaminos románticos**, inspirados en una hoja/pergamino antiguo, pero manteniendo la paleta visual actual de la landing.

La referencia visual es un pergamino, pero no quiero colores marrones pesados ni medievales. Debe sentirse integrado al diseño actual:

* rosa;
* fucsia;
* blanco;
* glassmorphism suave;
* bordes románticos;
* estética premium/coqueta.
* neon glow text effect.

---

## Alcance

Modificar solo los contenedores donde se renderizan los mensajes de la sección:

```text
Mensajes para volver a leer despacio
```

No modificar:

* hero;
* gráficos;
* bloque especial;
* timeline;
* ETL;
* queries;
* base de datos.

---

## Requerimiento visual

Cada mensaje debe renderizarse como una especie de **pergamino/card romántica**.

Características deseadas:

* fondo rosa muy claro o blanco rosado;
* bordes fucsia/rosa suaves;
* esquinas o detalles que recuerden un pergamino;
* sombra suave;
* posible textura sutil con gradientes;
* mantener buena legibilidad;
* texto oscuro/fucsia actual;
* no usar colores marrones fuertes;
* no parecer una tarjeta técnica;
* mantener responsive grid.

Se puede implementar con CSS usando:

* `border-radius`;
* `box-shadow`;
* `linear-gradient`;
* pseudo-elementos `::before` y `::after`;
* bordes decorativos;
* pequeñas curvas laterales o extremos enrollados simulados;
* sin necesidad de usar una imagen externa si se puede hacer por CSS.

Si es más estable usar CSS puro, preferir CSS puro.

---

## Estructura esperada

La sección debe seguir mostrando:

* título: `Mensajes para volver a leer despacio`;
* subtítulo si existe;
* grid de mensajes;
* texto del mensaje;
* sender;
* fecha.

Solo cambia el estilo del contenedor de cada mensaje.

---

## Restricciones

* No cambiar los IDs configurados en `content_config.py`.
* No cambiar la lógica que trae los mensajes.
* No convertir la sección en imagen.
* No usar assets externos innecesarios.
* No romper el responsive.
* No usar tablas.
* No introducir scroll horizontal.
* No perder legibilidad.
* No tocar el diseño general de la landing.

---

## CSS sugerido

Puedes crear o ajustar clases similares a:

```css
.featured-quote-card,
.quote-card,
.scroll-quote-card {
    position: relative;
    border-radius: 24px;
    background:
        radial-gradient(circle at top left, rgba(255, 255, 255, 0.92), transparent 42%),
        linear-gradient(135deg, rgba(255, 246, 251, 0.96), rgba(255, 226, 242, 0.88));
    border: 1px solid rgba(255, 95, 183, 0.35);
    box-shadow:
        0 18px 38px rgba(212, 20, 114, 0.14),
        inset 0 0 28px rgba(255, 255, 255, 0.55);
    overflow: hidden;
}
```

Y agregar pseudo-elementos para simular pergamino:

```css
.featured-quote-card::before,
.featured-quote-card::after {
    content: "";
    position: absolute;
    left: 18px;
    right: 18px;
    height: 12px;
    border-radius: 999px;
    background: linear-gradient(90deg, rgba(255, 179, 217, 0.35), rgba(255, 95, 183, 0.22));
    pointer-events: none;
}

.featured-quote-card::before {
    top: 10px;
}

.featured-quote-card::after {
    bottom: 10px;
}
```

Adapta los nombres de clases a los que ya existan en el proyecto. No duplicar CSS innecesariamente.

---

## Resultado esperado

La sección **“Mensajes para volver a leer despacio”** debe verse como una colección de pequeños pergaminos románticos personalizados, manteniendo la paleta rosa/fucsia/blanco y la estética actual.

---

## Documentación

Actualizar la documentación correspondiente indicando:

* qué script renderiza la sección de frases bonitas;
* qué clase CSS controla los pergaminos;
* qué cambio visual se aplicó;
* cómo modificar el estilo si quiero ajustar el efecto pergamino.

También documentar la sesión/cambio en el archivo de debug o changelog del proyecto si existe.

---

## Entregable

Devuélveme:

1. archivos modificados;
2. código completo por archivo;
3. explicación breve de qué cambió;
4. sin rediseñar la landing completa.
5. Adicional poner en cursiva estos dos subtitulos "Una conversacion que quiero recordar" y "Cosas bonitas que ella me dijo"
