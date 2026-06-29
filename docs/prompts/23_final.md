# Prompt para Codex — corregir promedio diario, reubicar KPI y arreglar pergaminos

Quiero hacer **3 ajustes puntuales** en la landing romántica. No quiero un rediseño completo, solo corregir estos comportamientos manteniendo la estética actual, la paleta rosa/fucsia/blanco, el tono romántico premium y la arquitectura existente.

---

## Objetivo general

Corregir estos tres puntos:

1. En la card del **promedio de mensajes diarios**, redondear el valor para mostrar **89** en lugar de **88,9**.
2. Reubicar la card **“Quien prendió mas veces la conversación”** para que quede **a la derecha** de la card **“Hater de tiempo completo / odio”**, ajustando ancho y layout para que se alinee visualmente con las demás cards de la sección.
3. Arreglar la sección **“Mensajes para volver a leer despacio”** para que cada contenedor **sea realmente un pergamino**, sin verse el recuadro original por debajo y sin que la imagen del pergamino quede tan transparente.

---

## 1) Redondear promedio de mensajes diarios

### Requerimiento

En la card de **promedio total de mensajes diarios**, el valor no debe mostrarse con decimal tipo:

```text
88,9
```

Quiero que se muestre redondeado al entero más cercano:

```text
89
```

### Regla

- Usar redondeo visual para presentación en UI.
- El cálculo puede seguir siendo decimal internamente si hace falta, pero el valor mostrado debe ser entero.
- Mantener el mismo estilo de tipografía y card.

### Resultado esperado

Si el promedio es `88.9`, la UI debe renderizar `89`.

---

## 2) Reubicar card “Quien prendió mas veces la conversación”

### Estado actual

La card:

```text
Quien prendió mas veces la conversación
```

está quedando sola abajo y demasiado ancha.

### Requerimiento

Quiero que esa card:

- quede ubicada **a la derecha** de la card:

```text
Hater de tiempo completo
```

- ajuste su ancho para alinearse visualmente con las demás cards de esa sección;
- no ocupe una fila completa innecesariamente;
- respete la lectura de izquierda a derecha;
- mantenga consistencia con el grid / layout actual.

### Intención visual

La composición debe verse equilibrada. La card de “odio” a la izquierda y la de “Quien prendió más veces la conversación” a la derecha, como cards hermanas dentro de la misma banda/fila.

### Restricciones

- No cambiar el contenido de la card.
- No cambiar su lógica de cálculo.
- Solo corregir posición, ancho y alineación.
- Mantener responsive layout.

---

## 3) Arreglar los pergaminos en “Mensajes para volver a leer despacio”

### Problema actual

En la sección:

```text
Mensajes para volver a leer despacio
```

sí se está renderizando la imagen/forma del pergamino, pero el resultado está mal porque:

1. **sigue viéndose el recuadro original** o card base;
2. la figura del pergamino queda **demasiado transparente**;
3. parece que hay **dos elementos solapados**: la card rectangular original + el pergamino por encima o por debajo.

### Requerimiento exacto

Quiero que **cada contenedor tome realmente la forma visual de un pergamino**.

Es decir:

- que no se vea el rectángulo original como un segundo contenedor;
- que no se sienta como “una imagen de pergamino encima de una card”;
- que el propio contenedor final sea el pergamino;
- que la estética siga usando la paleta del sitio, porque la paleta actual del contenedor original sí me gusta.

### Lo que sí quiero conservar

- la paleta rosa/fucsia/blanco del sitio;
- la legibilidad del texto;
- la estructura del mensaje, sender y fecha;
- la grilla responsiva de la sección.

### Lo que quiero corregir visualmente

- quitar el fondo/base rectangular sobrante;
- integrar el pergamino como **único** contenedor visible;
- aumentar opacidad/visibilidad del pergamino;
- lograr que cada card se vea como un pergamino romántico y no como dos capas mal montadas.

### Implementación sugerida

Codex debe revisar la clase CSS/componente que renderiza esas quote cards y hacer una de estas dos cosas (la que sea más limpia):

#### Opción A — convertir la propia card en pergamino

- usar el pergamino como `background-image` del contenedor principal;
- eliminar o neutralizar el fondo rectangular anterior;
- ajustar `background-size`, `background-repeat`, `background-position`;
- ajustar padding para que el texto quede bien posicionado;
- eliminar bordes, sombras o overlays que hagan evidente el recuadro viejo.

#### Opción B — wrapper único con skin de pergamino

- usar un wrapper pergamino como contenedor final visible;
- mover el contenido dentro de ese wrapper;
- evitar que haya una segunda card interna visible con fondo propio.

### Importante

El resultado final debe mostrar **un solo elemento visual por mensaje**: el pergamino.

No quiero:

- card + pergamino superpuestos;
- doble borde;
- transparencia excesiva;
- sensación de hack visual improvisado.

---

## Restricciones generales

- No rediseñar toda la sección.
- No cambiar ETL.
- No tocar queries salvo que haga falta solo para el redondeo de presentación.
- No cambiar mensajes ni IDs configurados.
- No modificar la lógica de featured quotes más allá de su render visual.
- Mantener consistencia con la arquitectura actual del proyecto.

---

## Documentación requerida

Además de aplicar los cambios, documenta brevemente:

1. en qué script(s) se corrigió cada punto;
2. qué clase CSS/componente controla ahora:
   - el promedio diario renderizado;
   - el layout de las cards de “Pequeños datos bonitos”; 
   - la visualización de los pergaminos;
3. qué ajuste se hizo para eliminar la doble capa en los pergaminos.

Si existe changelog/debug/session log, agrega una nota corta del cambio.

---

## Entregable

Devuélveme:

1. archivos modificados;
2. código completo por archivo;
3. explicación breve de qué cambió;
4. sin explicaciones largas ni rediseños innecesarios.
5. documentacion actualizada
