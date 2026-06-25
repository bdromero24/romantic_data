# Prompt para Codex — renderizar fresa 8-bit en el hero

Quiero hacer una adición visual mínima en la landing romántica, sin cambiar el diseño general ni la arquitectura.

## Objetivo

En la primera sección / hero de la página hay un círculo decorativo vacío. Quiero que ahí se renderice una **fresa estilo 8-bit / pixel art**, sin fondo, como detalle visual coqueto.

La idea es que la fresa aparezca dentro o sobre ese espacio circular, manteniendo el look romántico/premium actual de la landing.

---

## Contexto visual

Actualmente el hero tiene:

- fondo rosa claro;
- card grande con borde redondeado;
- título grande: `Nuestra historia`;
- subtítulo romántico;
- un círculo decorativo vacío a la derecha.

Ese círculo debe dejar de estar vacío y debe mostrar una fresa 8-bit.

La fresa debe verse como un detalle fino, no como un elemento invasivo.

---

## Requerimiento principal

Renderizar una imagen de fresa pixel art / 8-bit en el círculo decorativo del hero.

Preferencia de implementación:

1. Si ya existe una carpeta de assets estáticos, usarla.
2. Si no existe, crear una carpeta clara, por ejemplo:

```text
page/assets/
```

3. Colocar allí la imagen de la fresa, por ejemplo:

```text
page/assets/strawberry_8bit.png
```

4. Renderizarla desde el componente o script que construye el hero.

---

## Imagen

Tengo una imagen de fresa 8-bit/pixel art que puedo guardar en el proyecto.

Necesito que la app pueda cargarla desde una ruta local del repositorio.

Usa una ruta robusta basada en `Path(__file__).parent` o equivalente, evitando rutas absolutas de mi máquina.

Ejemplo de enfoque esperado:

```python
from pathlib import Path

ASSETS_DIR = Path(__file__).parent / "assets"
STRAWBERRY_IMAGE = ASSETS_DIR / "strawberry_8bit.png"
```

No usar rutas tipo:

```text
C:\Users\...
```

---

## Fondo transparente

La fresa debe renderizarse **sin fondo visible**.

Si la imagen original tiene fondo, intentar una de estas opciones:

1. usar una versión PNG con transparencia;
2. documentar que la imagen debe guardarse con fondo transparente;
3. si el proyecto ya tiene utilidades de procesamiento o assets, usar una versión limpia.

No quiero que se vea un rectángulo azul, blanco o de otro color detrás de la fresa.

---

## Alternativa si no se usa imagen

Si ves que es más conveniente, puedes renderizar la fresa mediante HTML/CSS o SVG inline, siempre que:

- mantenga estilo pixel art / 8-bit;
- no requiera librerías externas nuevas;
- no rompa Streamlit;
- sea fácil de mantener.

Pero mi preferencia es usar imagen PNG transparente desde assets.

---

## Requerimientos visuales

La fresa debe:

- ubicarse en el círculo decorativo vacío del hero;
- mantenerse proporcional y centrada;
- verse como pixel art / 8-bit;
- no deformarse;
- no romper responsive;
- mantener el diseño romántico actual;
- tener un tamaño equilibrado respecto al hero;
- verse bien en desktop y móvil.

Sugerencia CSS:

```css
.hero-strawberry {
    width: clamp(96px, 12vw, 160px);
    height: auto;
    object-fit: contain;
    image-rendering: pixelated;
    filter: drop-shadow(0 18px 28px rgba(212, 20, 114, 0.20));
}
```

Si se usa dentro del círculo:

```css
.hero-orb {
    display: flex;
    align-items: center;
    justify-content: center;
}
```

Puedes ajustar nombres de clases según la estructura actual.

---

## Restricciones

- No cambiar el diseño general de la landing.
- No cambiar textos principales del hero.
- No modificar ETL, queries ni base de datos.
- No agregar dependencias innecesarias.
- No usar rutas absolutas.
- No exponer errores técnicos en UI.
- No romper reveal-on-scroll ni animaciones existentes.
- No cambiar la paleta general.
- No reemplazar el hero completo: solo insertar/renderizar la fresa donde está el círculo vacío.

---

## Archivos a revisar

Revisa los scripts/componentes que renderizan el hero o la primera sección de la landing. Probablemente estén en alguno de estos lugares:

```text
page/main.py
page/ui/components.py
page/styles/
app/main.py
app/components/
```

Identifica exactamente dónde se define:

- el hero;
- el círculo decorativo vacío;
- las clases CSS asociadas.

Haz el cambio en el sitio correcto, respetando la arquitectura existente.

---

## Documentación requerida

Además del cambio visual, documenta la sesión y el cambio técnico.

Actualizar o crear documentación en un archivo existente de debug/sesiones si ya existe, por ejemplo:

```text
docs/codex_session_debug.md
```

Agregar una sección con título:

```text
## Ajuste visual: fresa 8-bit en hero
```

Debe indicar:

- qué se agregó;
- en qué script/componente se agregó;
- en qué ruta quedó el asset de la imagen;
- qué clase CSS o bloque visual se modificó;
- cómo cambiar la imagen en el futuro;
- que no se modificó ETL ni lógica de datos.

También actualizar documentación de configuración visual si existe, por ejemplo:

```text
docs/content_configuration.md
```

o crear una nota breve en el archivo de documentación más apropiado.

---

## Resultado esperado

Al abrir la landing, en el hero debe verse la fresa 8-bit dentro del círculo decorativo vacío.

Debe sentirse como un detalle de fina coquetería, integrado al diseño actual.

---

## Validación manual

Después del cambio, validar:

1. La app inicia sin errores.
2. La imagen carga correctamente.
3. La fresa no muestra fondo rectangular.
4. La fresa está centrada en el círculo del hero.
5. El diseño se mantiene en desktop.
6. El diseño no se rompe en móvil.
7. No se modificaron secciones ajenas.

---

## Formato de respuesta esperado

Devuélveme:

1. archivos modificados;
2. rutas creadas;
3. código completo o diff claro;
4. breve explicación técnica del cambio;
5. confirmación de qué documentación se actualizó.

No hagas explicaciones largas.
