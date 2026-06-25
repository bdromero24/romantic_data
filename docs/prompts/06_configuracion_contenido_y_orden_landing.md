# Prompt para Codex: parametrizar mensajes románticos, corregir labels con ñ, reordenar secciones y documentar cambios

Actúa como un desarrollador Python/Streamlit senior con foco en mantenibilidad, configuración manual, diseño de experiencia y documentación técnica.

## Contexto

Estoy trabajando en una app Streamlit ubicada en:

```text
C:\Users\User\OneDrive\Escritorio\landing_page
```

La app es una landing romántica basada en datos de WhatsApp e Instagram. El backend/ETL ya funciona y no debe reescribirse.

Actualmente la interfaz tiene cuatro problemas funcionales/de experiencia:

1. Algunos textos visibles muestran palabras normalizadas sin `ñ`, por ejemplo:
   - `te extrano`

   cuando deberían mostrarse como:
   - `te extraño`

2. Algunos mensajes aparecen repetidos en varias secciones, especialmente “el primer te amo”.

3. Quiero poder parametrizar manualmente qué mensajes aparecen en secciones como, por ejemplo, escoger un mensaje por su id en la db y mostrar ese mensaje:
   - mensaje especial;
   - timeline;
   - frases bonitas;
   - primer “te amo”.

4. La sección de gráficos “nuestro ritmo” debe cambiar de posición. Debe ir como segundo bloque de contenido, después de la sección “pequeños datos bonitos”, porque los gráficos son elementos grandes y captan más atención. La página debe presentar los elementos de mayor peso visual al inicio y avanzar hacia elementos más pequeños o secundarios.

Además, quiero saber exactamente en qué archivo se parametrizan esos mensajes, cómo cambiarlos manualmente después, y cómo agregar negritas en textos manuales.

---

# Objetivo

Implementar una configuración centralizada para controlar:

- labels visibles con tildes y `ñ`;
- mensajes destacados por `message_id`;
- exclusión de mensajes repetidos entre secciones;
- textos manuales con posibilidad de usar bold controlado;
- orden visual de secciones de la landing.

También documentar claramente:

- en qué script se modifica cada cosa;
- cómo cambiar los mensajes manualmente;
- cómo cambiar labels visibles;
- cómo agregar bold;
- cómo se corrigió el orden de secciones;
- qué bugs fueron encontrados y corregidos.

---

# Restricciones

No reescribir el ETL.

No cambiar el schema de base de datos.

No modificar la normalización backend.

No cambiar `message_normalized`.

No usar `message_normalized` para textos visibles de la UI.

No romper queries existentes.

No renderizar HTML como texto plano.

No escapar el HTML manual definido por mí, pero sí escapar todo contenido dinámico proveniente de la base de datos.

No volver a dark mode.

No exponer NLP técnico.

---

# Regla clave sobre textos visibles

La app debe respetar esta separación:

```text
message_normalized -> solo para búsquedas, filtros y conteos
message            -> para mostrar mensajes originales al usuario
labels manuales    -> para títulos, subtítulos y textos visibles
```

Por ejemplo:

```text
keyword interna: te extrano
label visible:   te extraño
```

---

# Tarea 1: crear configuración centralizada

Crear un archivo de configuración para contenido romántico.

Ruta sugerida:

```text
app/content_config.py
```

Si la estructura actual indica una mejor ubicación, usarla, pero debe ser clara y documentada.

El archivo debe incluir algo equivalente a:

```python
DISPLAY_LABELS = {
    "te amo": "te amo",
    "te extrano": "te extraño",
    "te quiero": "te quiero",
    "mi amor": "mi amor",
}

ROMANTIC_CONTENT = {
    "special_message": {
        "title": "Un mensaje que quiero guardar",
        "subtitle": "Hay palabras que merecen quedarse aquí.",
        "message_id": 39145,
    },
    "first_te_amo": {
        "title": "El primer te amo",
        "subtitle": "El primer momento donde esas palabras quedaron guardadas.",
        "message_id": 39145,
    },
    "timeline": [
        {
            "title": "El primer mensaje guardado",
            "message_id": None,
            "mode": "auto_first_message",
        },
        {
            "title": "El primer te amo",
            "message_id": 39145,
            "mode": "manual_message",
        },
    ],
    "featured_quotes": {
        "title": "Mensajes para volver a leer despacio",
        "message_ids": [
            # Agregar aquí IDs manuales de mensajes bonitos.
        ],
        "fallback_limit": 6,
    },
}
```

La estructura puede ajustarse, pero debe cumplir el objetivo: que yo pueda cambiar mensajes editando IDs y títulos en un solo archivo.

---

# Tarea 2: usar labels visibles con ñ

Buscar en el proyecto todos los lugares donde se muestren keywords o textos derivados de `message_normalized`.

Buscar patrones como:

```text
message_normalized
normalized
extrano
keyword
label
word
palabra
```

Si una keyword interna aparece como `te extrano`, debe mostrarse como `te extraño` usando `DISPLAY_LABELS`.

Implementar helper si hace falta:

```python
def get_display_label(value: str) -> str:
    return DISPLAY_LABELS.get(value, value)
```

La UI visible nunca debe mostrar `te extrano`.

---

# Tarea 3: evitar mensajes repetidos

Evitar que el mismo `message_id` aparezca repetido en varias secciones visibles.

Especialmente evitar que el mensaje `39145` aparezca repetido como:

- mensaje especial;
- primer te amo;
- frase bonita;
- timeline;
- otra card automática.

Implementar una lógica simple de exclusión.

Ejemplo:

```python
def get_reserved_message_ids() -> set[int]:
    return {
        id
        for id in [
            ROMANTIC_CONTENT["special_message"].get("message_id"),
            ROMANTIC_CONTENT["first_te_amo"].get("message_id"),
            *[
                item.get("message_id")
                for item in ROMANTIC_CONTENT.get("timeline", [])
            ],
        ]
        if isinstance(id, int)
    }
```

Luego, al renderizar `featured_quotes`, excluir esos IDs salvo que estén explícitamente definidos en `featured_quotes["message_ids"]`.

Regla:

- Los mensajes manuales tienen prioridad.
- Los mensajes automáticos no deben duplicar mensajes ya usados manualmente.

---

# Tarea 4: parametrizar mensajes de frases bonitas

Modificar la sección de frases bonitas para que funcione así:

1. Si `ROMANTIC_CONTENT["featured_quotes"]["message_ids"]` tiene IDs, mostrar exactamente esos mensajes.
2. Si está vacío, usar fallback automático con queries existentes.
3. En el fallback automático, excluir `reserved_message_ids`.
4. Mostrar `message`, no `message_normalized`.

Esto me permitirá pegar mensajes más bonitos manualmente agregando IDs.

---

# Tarea 5: parametrizar timeline

Modificar la sección timeline para que pueda mezclar:

- hitos automáticos;
- mensajes manuales por ID.

Ejemplo de configuración:

```python
"timeline": [
    {
        "title": "El primer mensaje guardado",
        "message_id": None,
        "mode": "auto_first_message",
    },
    {
        "title": "El primer te amo",
        "message_id": 39145,
        "mode": "manual_message",
    },
    {
        "title": "Un mensaje que siempre quiero recordar",
        "message_id": 40210,
        "mode": "manual_message",
    },
]
```

Si `mode == "manual_message"`, consultar el mensaje por ID.

Si `mode` es automático, mantener la lógica existente.

---

# Tarea 6: permitir bold controlado en textos manuales

Permitir usar `<strong>...</strong>` solo en textos manuales definidos en `app/content_config.py`.

Por ejemplo:

```python
"subtitle": "Este mensaje fue uno de esos que <strong>se quedan para siempre</strong>."
```

Reglas:

- Los textos manuales de configuración pueden admitir HTML controlado.
- Los mensajes provenientes de base de datos deben escaparse con `html.escape`.
- No escapar el HTML manual completo si contiene `<strong>`.
- No permitir que mensajes crudos de DB inyecten HTML.

Ejemplo correcto:

```python
safe_message = escape(row["message"])
manual_subtitle = ROMANTIC_CONTENT["special_message"]["subtitle"]

html = f'''
<p class="manual-subtitle">{manual_subtitle}</p>
<p class="quote-text">"{safe_message}"</p>
'''
st.markdown(html, unsafe_allow_html=True)
```

---

# Tarea 7: reordenar secciones de la landing

Modificar el orden visual de la landing para que la sección de gráficos “nuestro ritmo” aparezca como segundo bloque de contenido principal.

## Nuevo orden recomendado

La página debe seguir esta jerarquía visual:

1. Hero / portada romántica.
2. Pequeños datos bonitos.
3. Nuestro ritmo / gráficos.
4. Mensaje especial.
5. Lo que marcó nuestra historia / timeline.
6. Frases bonitas.
7. Nuestro lenguaje.
8. Cierre emocional.

Si la app ya tiene nombres distintos para estas secciones, adaptar el orden manteniendo esta intención:

```text
primero elementos grandes y de mayor impacto visual;
después elementos medianos;
finalmente elementos más pequeños o de lectura pausada.
```

## Justificación de UX

La sección “nuestro ritmo” tiene gráficos y ocupa más espacio visual. Debe ir cerca del inicio para captar atención después de las métricas principales.

La landing debe avanzar desde:

```text
alto impacto visual -> narrativa -> detalles -> cierre emocional
```

No debe quedar una sección gráfica pesada demasiado abajo ni mezclada entre tarjetas pequeñas.

## Reglas técnicas

- No cambiar la lógica de los gráficos.
- No rehacer las queries.
- Solo mover el orden de renderizado.
- Mantener títulos y estilos existentes.
- Si existe una función tipo `render_app()` o `main()`, reordenar llamadas ahí.
- Documentar exactamente en qué archivo se cambió el orden.

---

# Tarea 8: documentar manualmente cómo modificarlo

Crear o actualizar:

```text
docs/content_configuration.md
```

Este archivo debe explicar claramente:

## Secciones obligatorias

```md
# Configuración manual de contenido romántico

## Archivo principal de configuración

Indicar la ruta exacta, por ejemplo:

```text
app/content_config.py
```

## Cómo cambiar labels visibles

Explicar que `message_normalized` puede contener `te extrano`, pero la UI debe mostrar `te extraño`.

Ejemplo:

```python
DISPLAY_LABELS = {
    "te extrano": "te extraño",
}
```

## Cómo cambiar el mensaje especial

Explicar qué campo editar:

```python
ROMANTIC_CONTENT["special_message"]["message_id"]
```

## Cómo cambiar el primer te amo

Explicar qué campo editar:

```python
ROMANTIC_CONTENT["first_te_amo"]["message_id"]
```

## Cómo agregar mensajes bonitos

Explicar cómo agregar IDs en:

```python
ROMANTIC_CONTENT["featured_quotes"]["message_ids"]
```

## Cómo editar el timeline

Explicar cómo agregar un hito manual:

```python
{
    "title": "Un mensaje que quiero recordar",
    "message_id": 40210,
    "mode": "manual_message",
}
```

## Cómo usar bold

Explicar que en textos manuales se puede usar:

```html
<strong>texto en negrita</strong>
```

pero no en mensajes crudos de base de datos.

## Cómo evitar duplicados

Explicar que la app reserva IDs usados en secciones principales para que no se repitan automáticamente en frases bonitas.

## Cómo cambiar el orden de secciones

Explicar en qué archivo se renderiza el orden principal de la landing.

Ejemplo:

```text
app/main.py
```

Indicar que “nuestro ritmo” debe ir después de “pequeños datos bonitos” porque es un bloque visual grande.
```

---

# Tarea 9: actualizar documentación de sesión

Actualizar o crear:

```text
docs/codex_session_debug.md
```

Agregar una sección nueva:

```md
## Bug 5: Labels visibles usaban texto normalizado sin ñ y mensajes repetidos

### Síntoma

La UI mostraba valores como `te extrano` y repetía mensajes como “el primer te amo” en varias secciones.

### Causa raíz

Indicar la causa real encontrada:
- uso de `message_normalized` en UI;
- falta de labels de presentación;
- falta de configuración centralizada;
- falta de exclusión de IDs repetidos;
- otra causa real.

### Archivos afectados

Listar rutas relativas.

### Corrección aplicada

Explicar:
- creación de configuración centralizada;
- mapeo `te extrano` -> `te extraño`;
- parametrización de mensajes por ID;
- exclusión de duplicados;
- soporte de `<strong>` en textos manuales.

### Verificación

Indicar qué se revisó o qué comando se ejecutó.

### Resultado

Indicar si:
- la UI ya no muestra `te extrano`;
- los mensajes manuales se pueden parametrizar;
- el primer te amo no se repite automáticamente;
- los textos manuales soportan bold.
```

Agregar también esta sección:

```md
## Ajuste UX: reordenamiento de la sección “nuestro ritmo”

### Motivo

La sección “nuestro ritmo” contiene gráficos y tiene más peso visual, por lo que debe aparecer después de “pequeños datos bonitos”.

### Cambio aplicado

Indicar en qué archivo se cambió el orden de renderizado y cuál quedó siendo el nuevo orden.

### Resultado esperado

La landing presenta primero los elementos grandes y de mayor atención, y luego avanza hacia secciones más pequeñas, narrativas o de lectura pausada.
```

---

# Validaciones obligatorias

Ejecutar o revisar:

```powershell
Get-ChildItem -Recurse -Filter *.py | Select-String -Pattern "message_normalized|extrano|featured_quotes|timeline|special_message|first_te_amo"
```

Verificar que:

1. `message_normalized` no se use para texto visible.
2. `te extrano` no aparezca en UI visible.
3. `DISPLAY_LABELS` exista y se use.
4. `ROMANTIC_CONTENT` exista y sea fácil de modificar.
5. `39145` no aparezca duplicado automáticamente en múltiples secciones.
6. Los mensajes de DB se muestren usando `message`.
7. El HTML visual se renderice con:

```python
st.markdown(html, unsafe_allow_html=True)
```

8. Los textos manuales puedan usar `<strong>...</strong>`.
9. La sección “nuestro ritmo” aparezca después de “pequeños datos bonitos”.
10. El orden de secciones esté documentado.

---

# Formato de respuesta esperado

Devuelve únicamente:

1. Rutas de archivos modificados.
2. Contenido completo de cada archivo modificado.
3. Contenido completo de `docs/content_configuration.md`.
4. Contenido actualizado de `docs/codex_session_debug.md`.

No agregues explicaciones adicionales fuera de los archivos.
