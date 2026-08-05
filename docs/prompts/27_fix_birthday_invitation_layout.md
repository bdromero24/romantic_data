# Prompt para Codex — corregir layout de `BirthdayInvitationLetter`

Necesito corregir un problema visual en el componente `BirthdayInvitationLetter` de mi landing romántica en Streamlit.

## Contexto

La landing está hecha en **Python + Streamlit** y usa componentes personalizados con:

```python
streamlit.components.v1.html()
```

El componente `BirthdayInvitationLetter` se agregó después de `SpotifyCapsule`. La idea visual aprobada es:

```text
SpotifyCapsule
    ↓ scroll
sobre/carta cerrada con alitas y corazón
    ↓ click
carta tipo pergamino viejo con invitación y dos botones
```

La estética general de la app es:

- rosa, blanco y fucsia;
- glassmorphism;
- neon glow;
- 8-bit / pixel art;
- estilo romántico premium.

## Problema actual

El componente **no se está renderizando bien en posición/layout**.

En la captura actual se observa que:

1. La sección queda con demasiado espacio vacío arriba.
2. Los círculos/nubes/corazones decorativos ocupan una zona muy grande.
3. La carta aparece demasiado abajo.
4. El contenido de la carta queda parcialmente cortado por la parte inferior del componente.
5. El alto del `components.html()` o del contenedor interno parece insuficiente o mal distribuido.
6. Visualmente, el layout no parece centrado ni balanceado.
7. La carta debería verse completa dentro de la sección, no recortada.

## Objetivo

Corregir la estructura visual y el layout del componente para que:

- el sobre/carta cerrada se renderice centrado y proporcionado;
- al abrirse, la carta aparezca completa;
- no haya recortes en la parte inferior;
- no haya exceso de espacio vacío superior;
- los elementos decorativos no desplacen la carta hacia abajo;
- el componente se vea bien en desktop y mobile;
- el alto del iframe/componente sea suficiente y controlado.

## Requerimiento principal

Revisar y corregir el archivo del componente, probablemente:

```text
ui/birthday_invitation.py
```

y cualquier CSS/HTML/JS relacionado con `BirthdayInvitationLetter`.

La corrección debe enfocarse en:

1. `height` usado en `components.html(...)`;
2. altura del contenedor principal;
3. posición de la carta cerrada y abierta;
4. distribución vertical del escenario;
5. comportamiento responsive;
6. evitar `overflow: hidden` si está cortando la carta;
7. evitar posiciones absolutas que saquen la carta del flujo visual;
8. que la carta abierta no quede fuera del área visible.

## Comportamiento esperado

### Estado cerrado

Antes del click:

- el sobre con alitas debe aparecer centrado;
- el texto de invitación debe verse debajo o cerca del sobre;
- los elementos decorativos deben acompañar, no dominar la sección;
- el bloque debe sentirse compacto y elegante.

### Estado abierto

Después del click:

- la carta debe desplegarse con animación `slide-up` o `fade-in`;
- la carta debe verse completa;
- el título `Querida Mar:` debe aparecer bien ubicado;
- el cuerpo de la carta no debe quedar cortado;
- los botones deben quedar visibles al final;
- la firma debe quedar visible;
- si el texto es largo, el componente debe tener altura suficiente o scroll interno elegante.

## Ajustes técnicos sugeridos

Revisar si actualmente hay algo parecido a:

```python
components.html(html_content, height=...)
```

Si el `height` es muy bajo, aumentarlo o calcular uno más adecuado.

Ejemplo:

```python
components.html(html_content, height=980, scrolling=False)
```

o, si el contenido puede crecer:

```python
components.html(html_content, height=1100, scrolling=True)
```

La prioridad es que el componente se vea completo y no recortado.

## CSS sugerido

Revisar el contenedor raíz:

```css
.birthday-invitation-root {
    width: 100%;
    min-height: 900px;
    position: relative;
    overflow: visible;
}
```

Evitar que la carta quede atrapada por:

```css
overflow: hidden;
height: demasiado pequeño;
position: absolute sin control;
top demasiado alto;
transform que saque el contenido del viewport;
```

La carta abierta debería tener algo similar a:

```css
.birthday-letter {
    position: relative;
    margin: 0 auto;
    max-width: 760px;
    width: min(92vw, 760px);
    z-index: 5;
}
```

Si se usan elementos decorativos absolutos, deben quedar detrás:

```css
.birthday-decoration {
    position: absolute;
    z-index: 1;
    pointer-events: none;
}

.birthday-letter,
.birthday-envelope-stage {
    position: relative;
    z-index: 3;
}
```

## Distribución visual esperada

El bloque no debe iniciar con una zona decorativa gigante. Debe sentirse así:

```text
[pequeño espacio superior]
[sobre/carta cerrada centrada]
[texto de invitación]
[al abrir: carta completa centrada]
[botones visibles]
[espacio inferior controlado]
```

No así:

```text
[mucho espacio vacío]
[decoraciones enormes]
[carta empujada hacia abajo]
[carta recortada]
```

## Mobile responsive

En pantallas pequeñas:

- reducir tamaño del sobre;
- reducir decoraciones;
- ajustar padding;
- carta al 92%-96% del ancho;
- evitar que el texto se corte;
- botones apilados verticalmente si no caben.

## Restricciones

- No cambiar el copy de la carta salvo que sea necesario para pruebas.
- No eliminar los dos botones.
- No tocar ETL.
- No tocar queries.
- No modificar `landing_data.json`.
- No romper `SpotifyCapsule`.
- No rediseñar toda la landing.
- No cambiar la estética general.
- No introducir dependencias externas.
- Mantener `streamlit.components.v1.html()`.

## Validación local

Probar con:

```powershell
$env:USE_STATIC_DATA="true"
streamlit run app/main.py
```

Validar:

1. la landing carga;
2. `SpotifyCapsule` sigue funcionando;
3. después de SpotifyCapsule aparece `BirthdayInvitationLetter`;
4. el componente cerrado se ve centrado;
5. al hacer click, la carta se abre;
6. la carta completa se ve sin cortes;
7. los botones se ven y funcionan;
8. no hay scroll raro dentro del iframe salvo que sea intencional;
9. funciona en desktop y mobile.

## Entregable

Devuélveme:

1. archivos modificados;
2. código completo por archivo;
3. explicación breve del ajuste;
4. valor final de `height` usado en `components.html(...)`;
5. clases CSS principales modificadas.
