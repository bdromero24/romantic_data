# Prompt para Codex — pergaminos en frases bonitas + corazón 8-bit en primer te amo

Necesito hacer un ajuste visual puntual en la landing romántica, sin rediseñar toda la app.

## Objetivo

Aplicar dos cambios visuales:

1. Renderizar una imagen de pergamino que voy a ubicar dentro de la raíz del proyecto bajo el nombre  `perrgamino.png`  y usarla como forma/fondo de todos los contenedores de la sección **“Mensajes para volver a leer despacio”**.
2. Renderizar un corazón en 8-bit que también voy a ubicar dentro de la raíz del proyecto, y colocarlo como objeto bien ubicado dentro de los contenedores/cards relacionados con **“Primer te amo”**. `corazon.png`

Ambos cambios deben mantener la paleta actual rosa/fucsia/blanco y el estilo romántico premium de la landing.

---

## 1. Pergamino en “Mensajes para volver a leer despacio”

### Contexto

La sección actual muestra varios mensajes en cards/recuadros. Quiero que esos contenedores adopten la forma visual de un pergamino usando una imagen que estará guardada en la raíz del proyecto.

### Requerimiento

- Localizar la imagen de pergamino en la raíz del proyecto.
- Si es conveniente, moverla a la carpeta de assets correspondiente, por ejemplo `ui/assets/`, `page/assets/` o la carpeta que ya use el proyecto.
- Renderizarla únicamente en los contenedores/cards de la sección:

```text
Mensajes para volver a leer despacio
```

- Los mensajes deben seguir siendo texto HTML/CSS real encima del pergamino, no texto incrustado en la imagen.
- La imagen debe funcionar como fondo o marco visual del contenedor.
- Mantener buena legibilidad.
- Mantener responsive grid.
- No aplicar este estilo a otras secciones.

### Resultado visual esperado

Cada mensaje de esa sección debe verse como un pergamino romántico, pero integrado al look actual:

- paleta rosa/fucsia/blanco;
- texto legible;
- sombra suave;
- sin colores marrones pesados si desentonan;
- sin romper el tamaño de los cards;
- sin scroll horizontal.

### Implementación sugerida

Preferir CSS limpio, usando algo similar a:

```css
.featured-quote-card {
    background-image: url("...");
    background-size: 100% 100%;
    background-repeat: no-repeat;
    background-position: center;
    position: relative;
}
```

Ajustar padding interno para que el texto no choque con los bordes del pergamino.

Si el nombre de clase real es otro, usar el existente y evitar duplicar estilos innecesarios.

---

## 2. Corazón 8-bit en “Primer te amo”

### Contexto

Voy a ubicar una imagen de corazón 8-bit dentro de la raíz del proyecto. Quiero que se renderice dentro de los contenedores o cards relacionados con:

```text
Primer te amo
```

### Requerimiento

- Localizar el asset del corazón 8-bit en la raíz del proyecto.
- Si es conveniente, moverlo a la carpeta de assets correspondiente.
- Renderizarlo dentro de los contenedores/cards donde aparezca **“Primer te amo”**.
- Debe quedar bien ubicado, como detalle visual/coqueto, no como elemento invasivo.
- Mantener el estilo pixel art.
- No deformar la imagen.
- No romper responsive.

### Ubicación visual sugerida

Ubicar el corazón 8-bit como detalle decorativo:

- esquina superior derecha del card; o
- lateral derecho del contenido; o
- como pequeño badge/ornamento dentro del card.

Debe verse intencional y equilibrado.

### Restricciones

- No renderizar el corazón en todos los cards, solo donde corresponda a **Primer te amo**.
- No cambiar la lógica del cálculo del primer te amo.
- No cambiar IDs configurados.
- No tocar ETL ni queries.
- No cambiar el diseño global de la landing.

---

## Documentación requerida

Documentar brevemente:

1. qué asset de pergamino se usó y dónde quedó ubicado;
2. qué asset de corazón 8-bit se usó y dónde quedó ubicado;
3. qué archivo renderiza la sección “Mensajes para volver a leer despacio”;
4. qué clase CSS controla los pergaminos;
5. qué archivo/render controla el card de “Primer te amo”;
6. qué clase CSS controla el corazón 8-bit;
7. agregar una nota corta en el debug/changelog de sesión si existe.

---

## Restricciones generales

- No rediseñar la landing completa.
- No tocar otras secciones visuales.
- No modificar el contenido configurado manualmente.
- No eliminar mensajes.
- No exponer errores técnicos en UI.
- Mantener `st.markdown(..., unsafe_allow_html=True)` si el render usa HTML visual.
- Escapar texto dinámico de base de datos cuando aplique.

---

## Entregable

Devuélveme:

1. archivos modificados;
2. código completo por archivo;
3. explicación breve de qué cambió;
4. indicación clara de dónde quedaron los assets.
