# Prompt para Codex: parametrizar mensajes especiales y frases bonitas por ID sin cambios visuales

Actúa como un desarrollador Python/Streamlit senior con foco en configuración de contenido, mantenibilidad y documentación técnica.

## Contexto

Estoy trabajando en una landing romántica en Streamlit ubicada en:

```text
C:\Users\User\OneDrive\Escritorio\landing_page
```

La landing ya funciona visualmente y el frontend ya está en un estado satisfactorio. No necesito más ajustes visuales generales.

El backend/ETL, la base de datos, la normalización y el diseño visual principal ya están listos.

Ahora necesito retomar únicamente la parte de **parametrización de mensajes por ID** y la **documentación**, porque en la sesión anterior no se implementó correctamente.

---

# Objetivo único

Modificar la configuración y la lógica de renderizado para que pueda controlar manualmente por ID:

1. La sección:

```text
Un mensaje que quiero guardar
```

para mostrar:

- varios mensajes de ella;
- una conversación compuesta por un mensaje mío y una respuesta de ella;
- esos mensajes deben renderizarse usando el estilo visual ya existente tipo burbuja/chat/Instagram si ya fue implementado.

2. La sección:

```text
Mensajes para volver a leer despacio
```

para mostrar mensajes cortos seleccionados manualmente por ID.

3. Actualizar documentación para explicar exactamente dónde y cómo cambiar esos IDs.

---

# Importante

No hacer nuevos cambios visuales generales.

No rediseñar la landing.

No tocar el look and feel actual.

No modificar colores, degradados, fuentes, reveal-on-scroll, cards generales ni gráficos.

Solo usar clases visuales ya existentes si están disponibles.

Si faltan clases mínimas para burbujas tipo chat, agregarlas solo si son estrictamente necesarias para que los mensajes configurados se vean correctamente, pero no hacer una refactorización visual grande.

---

# Archivos esperados a revisar

Revisar primero estos archivos o sus equivalentes reales:

```text
app/content_config.py
app/main.py
ui/components.py
ui/styles.py
docs/content_configuration.md
docs/codex_session_debug.md
```

Si la estructura real usa otras rutas, adaptar, pero documentar las rutas exactas.

---

# Regla de datos

La tabla `messages` tiene al menos:

```text
id
sender
message
message_normalized
timestamp
source
```

Para mostrar mensajes en la UI usar siempre:

```text
message
```

No usar:

```text
message_normalized
```

`message_normalized` solo debe usarse para búsquedas, filtros y conteos.

---

# Tarea 1: actualizar `ROMANTIC_CONTENT` para mensajes especiales

Buscar el archivo de configuración actual, probablemente:

```text
app/content_config.py
```

Modificar la estructura de configuración para que la sección `special_message` permita bloques manuales.

La configuración debe quedar conceptualmente así:

```python
ROMANTIC_CONTENT = {
    ...
    "special_message": {
        "title": "Un mensaje que quiero guardar",
        "subtitle": "Algunas palabras merecen quedarse aquí.",
        "blocks": [
            {
                "type": "her_messages",
                "title": "Cosas bonitas que ella me dijo",
                "message_ids": [
                    # IDs editables de mensajes de ella.
                ],
            },
            {
                "type": "conversation_pair",
                "title": "Una conversación que quiero recordar",
                "messages": [
                    {
                        "role": "me",
                        "message_id": None,
                    },
                    {
                        "role": "her",
                        "message_id": None,
                    },
                ],
            },
        ],
    },
    ...
}
```

## Reglas

- Los IDs deben ser fáciles de cambiar.
- No dejar lógica visual o queries dentro de `content_config.py`.
- `content_config.py` solo debe ser configuración.
- Si ya existe `special_message["message_id"]`, migrar sin romper compatibilidad o dejar fallback.
- Si `blocks` está vacío o los IDs son `None`, la app no debe fallar.
- Debe mostrarse un fallback amigable o simplemente omitir el bloque vacío.

---

# Tarea 2: soportar varios mensajes de ella

Implementar soporte para bloques:

```python
{
    "type": "her_messages",
    "title": "Cosas bonitas que ella me dijo",
    "message_ids": [123, 456, 789],
}
```

## Comportamiento esperado

La app debe:

1. Leer los IDs de `message_ids`.
2. Consultar esos mensajes por ID.
3. Mantener el orden definido en la lista.
4. Renderizarlos en la sección “Un mensaje que quiero guardar”.
5. Mostrar:
   - mensaje original;
   - sender;
   - fecha si está disponible.
6. Usar estilo de burbuja de ella si existe:
   - izquierda;
   - blanco/rosa claro;
   - borde rosa/fucsia.

---

# Tarea 3: soportar conversación tipo mensaje mío + respuesta de ella

Implementar soporte para bloques:

```python
{
    "type": "conversation_pair",
    "title": "Una conversación que quiero recordar",
    "messages": [
        {"role": "me", "message_id": 111},
        {"role": "her", "message_id": 222},
    ],
}
```

## Comportamiento esperado

La app debe:

1. Leer cada `message_id`.
2. Consultar los mensajes.
3. Mantener el orden configurado.
4. Renderizar el mensaje con `role = "me"` como burbuja mía.
5. Renderizar el mensaje con `role = "her"` como burbuja de ella.
6. Mostrar ambos dentro de un mismo bloque/contenedor de conversación.

## Reglas de roles

```text
role = "me"  -> burbuja alineada a la derecha
role = "her" -> burbuja alineada a la izquierda
```

Si aparece un role no reconocido, tratarlo como `"her"` o documentar el fallback.

---

# Tarea 4: helper para consultar mensajes por IDs

Buscar si ya existe una función para consultar mensajes por ID.

Si no existe, crear una función reutilizable en el módulo de queries/data access que corresponda.

Nombre sugerido:

```python
get_messages_by_ids(message_ids: list[int]) -> list[dict]
```

o equivalente según convenciones existentes.

## Requisitos

1. Debe consultar por la columna `id`.
2. Debe devolver:
   - `id`
   - `sender`
   - `message`
   - `timestamp`
   - opcionalmente `source`
3. Debe mantener el orden configurado en `message_ids`.
4. Debe ignorar IDs `None`.
5. Debe manejar listas vacías sin fallar.
6. Debe usar SQL parametrizado.
7. No usar f-strings SQL con input del usuario.
8. No concatenar SQL inseguro.

## Orden

Si PostgreSQL no devuelve el orden de la lista, reordenar en Python:

```python
records_by_id = {record["id"]: record for record in records}
ordered_records = [
    records_by_id[message_id]
    for message_id in message_ids
    if message_id in records_by_id
]
```

---

# Tarea 5: actualizar sección “Mensajes para volver a leer despacio”

En `ROMANTIC_CONTENT["featured_quotes"]`, debe existir una configuración manual por IDs:

```python
"featured_quotes": {
    "title": "Mensajes para volver a leer despacio",
    "message_ids": [
        # IDs editables de mensajes cortos bonitos.
    ],
    "fallback_limit": 5,
}
```

## Comportamiento esperado

1. Si `message_ids` contiene IDs, mostrar exactamente esos mensajes.
2. Mantener el orden configurado.
3. Si `message_ids` está vacío, usar el fallback automático actual.
4. En fallback automático, excluir IDs ya usados en:
   - `special_message`;
   - `first_te_amo`;
   - `timeline`;
   - conversation pairs;
   - her messages blocks.
5. Mostrar `message`, no `message_normalized`.
6. No repetir mensajes ya usados manualmente en secciones principales.

---

# Tarea 6: función para obtener IDs reservados

Actualizar o crear una función en `content_config.py` o en un helper asociado:

```python
def get_reserved_message_ids() -> set[int]:
    ...
```

Debe recolectar IDs usados en:

- `special_message["message_id"]`, si todavía existe;
- `special_message["blocks"][*]["message_ids"]`;
- `special_message["blocks"][*]["messages"][*]["message_id"]`;
- `first_te_amo["message_id"]`;
- `timeline[*]["message_id"]`;
- cualquier otro bloque manual existente.

Debe ignorar:

- `None`;
- strings vacíos;
- valores no enteros.

---

# Tarea 7: renderizado seguro

Todo mensaje proveniente de base de datos debe escaparse con:

```python
from html import escape
```

Correcto:

```python
safe_message = escape(str(row["message"]))
safe_sender = escape(str(row["sender"]))
```

No escapar todo el HTML estructural.

Incorrecto:

```python
st.markdown(escape(html), unsafe_allow_html=True)
```

Renderizar HTML visual con:

```python
st.markdown(html, unsafe_allow_html=True)
```

No usar:

```python
st.write(html)
st.code(html)
st.text(html)
```

para HTML visual.

---

# Tarea 8: no tocar ajustes visuales ya terminados

No cambiar:

- fondo;
- paleta;
- gradientes;
- reveal-on-scroll;
- errores globales;
- gráficos;
- tipografías generales;
- pesos de fuentes;
- layout de secciones;
- orden general de la landing.

Solo modificar lo necesario para que las secciones consuman configuración por ID.

---

# Tarea 9: documentación obligatoria

Actualizar o crear:

```text
docs/content_configuration.md
```

Debe explicar clara y detalladamente cómo modificar estas secciones.

Agregar o actualizar estas secciones:

```md
# Configuración manual de contenido romántico

## Archivo principal

Indicar ruta real del archivo, por ejemplo:

```text
app/content_config.py
```

## Cómo editar “Un mensaje que quiero guardar”

Explicar que se edita y mostrar un ejemplo con un id random:

```python
ROMANTIC_CONTENT["special_message"]["blocks"]
```

### Varios mensajes de ella

Ejemplo:

```python
{
    "type": "her_messages",
    "title": "Cosas bonitas que ella me dijo",
    "message_ids": [123, 456, 789],
}
```

### Conversación mío + respuesta de ella

Ejemplo:

```python
{
    "type": "conversation_pair",
    "title": "Una conversación que quiero recordar",
    "messages": [
        {"role": "me", "message_id": 111},
        {"role": "her", "message_id": 222},
    ],
}
```

## Cómo editar “Mensajes para volver a leer despacio”

Explicar que se edita:

```python
ROMANTIC_CONTENT["featured_quotes"]["message_ids"]
```

Ejemplo:

```python
"message_ids": [123, 456, 789]
```

## Qué ID usar

Aclarar:

Usar el valor de la columna `id` de la tabla `messages`, no el número de fila visual del visor de base de datos.

## Qué pasa si dejo IDs vacíos o None

Explicar:
- `None` significa no usar mensaje manual;
- lista vacía activa fallback automático si existe;
- la app no debe fallar.

## Evitar duplicados

Explicar que los IDs usados en bloques especiales se consideran reservados para evitar repetición automática en frases bonitas.

## Seguridad HTML

Explicar que mensajes de base de datos se escapan y que no se debe meter HTML en mensajes crudos.
```

---

# Tarea 10: actualizar documentación de sesión

Actualizar:

```text
docs/codex_session_debug.md
```

Agregar una sección:

```md
## Ajuste de configuración: mensajes especiales y frases bonitas por ID

### Motivo

La landing ya estaba visualmente correcta, pero faltaba parametrizar correctamente qué mensajes aparecen en “Un mensaje que quiero guardar” y “Mensajes para volver a leer despacio”.

### Cambio aplicado

Indicar:
- archivos modificados;
- estructura nueva de `special_message["blocks"]`;
- soporte para varios mensajes de ella;
- soporte para conversación mío + respuesta de ella;
- soporte para `featured_quotes["message_ids"]`.

### Cómo se configura

Indicar que los IDs se editan en el archivo de configuración de contenido.

### Resultado esperado

- Se pueden mostrar varios mensajes de ella.
- Se puede mostrar una conversación con mensaje mío y respuesta de ella.
- Se pueden seleccionar frases bonitas cortas por ID.
- Se mantiene fallback automático si no hay IDs configurados.
- No se repiten IDs reservados en fallback automático.
```

---

# Validaciones obligatorias

Ejecutar:

```powershell
streamlit run app/main.py
```

Validar:

1. La app carga sin errores.
2. La sección “Un mensaje que quiero guardar” funciona aunque `blocks` esté vacío.
3. Si configuro IDs en `her_messages`, aparecen esos mensajes.
4. Si configuro `conversation_pair`, aparecen los mensajes en el orden configurado.
5. Si configuro IDs en `featured_quotes["message_ids"]`, aparecen exactamente esos mensajes.
6. Si `featured_quotes["message_ids"]` está vacío, funciona fallback automático.
7. No aparece `message_normalized` en UI.
8. No aparece HTML crudo en UI.
9. No se duplican IDs reservados en fallback.
10. Los cambios visuales existentes no se rompen.

---

# Restricciones

No modificar ETL.

No modificar schema.

No modificar carga de datos.

No modificar normalización.

No cambiar `message_normalized`.

No hacer más ajustes visuales generales.

No tocar reveal-on-scroll.

No cambiar orden de secciones.

No instalar librerías nuevas.

No renderizar HTML como texto.

No usar SQL inseguro.

---

# Formato de respuesta esperado

Devuelve únicamente:

1. Rutas de archivos modificados.
2. Contenido completo de cada archivo modificado.
3. Contenido actualizado de `docs/content_configuration.md`.
4. Contenido actualizado de `docs/codex_session_debug.md`.
4. Sesion trabajada en `docs/sessions/#number_sesion_timestamp.md`.

No agregues explicaciones adicionales fuera de los archivos.
