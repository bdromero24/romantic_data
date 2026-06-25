# Prompt para Codex — corregir bloques de mensaje especial, carácter Â· y frases bonitas

## Contexto

El proyecto ya está prácticamente listo. La landing romántica tiene una sección llamada:

```text
Un mensaje que quiero guardar
```

Dentro de esa sección se está intentando renderizar:

1. un bloque de varios mensajes de ella;
2. una conversación compuesta por mensajes míos y mensajes de ella;
3. una sección posterior de frases bonitas configurada por IDs.

Actualmente hay tres problemas visuales/funcionales que deben corregirse sin rediseñar la página completa.

---

## Archivos relevantes

Revisa principalmente estos archivos, o sus equivalentes si la estructura actual cambió:

```text
page/content_config.py
page/main.py
page/ui/components.py
page/ui/styles.py
page/db/queries.py
page/db/messages.py
```

No asumas esos nombres exactos si el proyecto usa otros módulos. Localiza la lógica real por función/componente.

---

## Configuración actual relevante

En `content_config.py` existe una estructura similar a esta:

```python
ROMANTIC_CONTENT = {
    "special_message": {
        "title": "Un mensaje que quiero guardar",
        "subtitle": "Hay palabras que merecen quedarse <strong>aquí</strong>.",
        "message_id": 1440,
        "blocks": [
            {
                "type": "her_messages",
                "title": "",
                "message_ids": [5038, 5039, 5040, 5041, 5042],
            },
            {
                "type": "conversation_pair",
                "title": "",
                "messages": [
                    {"role": "me", "message_id": 6157},
                    {"role": "me", "message_id": 6156},
                    {"role": "me", "message_id": 6155},
                    {"role": "her", "message_id": 6151},
                    {"role": "her", "message_id": 6150},
                    {"role": "her", "message_id": 6141},
                    {"role": "her", "message_id": 6218},
                    {"role": "me", "message_id": 6209},
                    {"role": "her", "message_id": 6085},
                    {"role": "me", "message_id": 5498},
                    {"role": "me", "message_id": 5505},
                    {"role": "her", "message_id": 5506},
                ],
            },
        ],
    },
    "featured_quotes": {
        "title": "Mensajes para volver a leer despacio",
        "message_ids": [6180, 6190, 97, 1840, 6096, 13928, 17501],
        "fallback_limit": 5,
    },
}
```

---

## Problema 1 — bloque `her_messages` mal agrupado

Actualmente los primeros 5 mensajes de ella se están renderizando como burbujas/cards separadas.

### Comportamiento requerido

El bloque `type = "her_messages"` debe renderizarse como **un solo recuadro/contenedor visual** que agrupe todos los mensajes (todas las cards o burbujas) configurados en `message_ids`.

Dentro de ese recuadro pueden mantenerse los mensajes individuales, es decir cada una de las cards o burbujas pero encerradas en un solo recuadro.

### Reglas

- Mantener el estilo romántico actual.
- No rediseñar toda la sección.
- Reutilizar clases existentes si hay componentes de cards/burbujas.
- El bloque debe respetar el orden exacto de los IDs configurados.
- Usar la columna `message` para texto visible.
- No usar `message_normalized` para renderizar texto.
- Escapar HTML del contenido proveniente de base de datos.
- No cambiar el orden de los mensajes o los ID

---

## Problema 2 — `conversation_pair` debe ir en otro recuadro separado

El bloque `type = "conversation_pair"` actualmente aparece mezclado visualmente con el bloque anterior o sin una separación clara, es decir dentro de un solo recuadro.

### Comportamiento requerido

El bloque `conversation_pair` debe renderizarse como **otro recuadro/contenedor visual independiente**, separado del bloque `her_messages`.

Dentro de este contenedor sí deben renderizarse burbujas tipo conversación:

```text
role = "me"  -> burbuja alineada a la derecha
role = "her" -> burbuja alineada a la izquierda
```

### Reglas

- Mantener el orden exacto configurado en `messages`.
- No ordenar automáticamente por timestamp si eso cambia el orden manual.
- Si un `message_id` no existe, ignorarlo de forma segura y registrar warning/log si el proyecto ya tiene logging.
- Si `role` no es reconocido, usar fallback `"her"` o un fallback documentado.
- Mantener separación visual entre:
  - bloque de mensajes de ella;
  - bloque de conversación.

---

## Problema 3 — aparece el carácter `Â·`

En la metadata de los mensajes se está viendo este carácter:

```text
Â·
```

Ejemplo visual:

```text
Mar 🍓 Â· 27/05/2026
David Â· 19/05/2026
```

Ese carácter no debe aparecer.

### Comportamiento requerido

Debe mostrarse un separador limpio, por ejemplo:

```text
Mar 🍓 · 27/05/2026
```

O si prefieres evitar problemas de encoding:

```text
Mar 🍓 - 27/05/2026
```

### Reglas

- Revisar dónde se está construyendo el string de metadata.
- No dejar mojibake (`Â·`, `Ã`, etc.) visible en UI.
- Si existe helper de limpieza como `clean_text`, reutilizarlo si aplica.
- Para separadores visuales, preferir HTML seguro:

```html
<span class="message-meta-separator">·</span>
```

O un guion simple si el proyecto sigue teniendo problemas de encoding.

---

## Problema 4 — sección de frases bonitas no renderiza los mensajes

La sección:

```text
Mensajes para volver a leer despacio
```

está sobrando visualmente porque solo muestra el título, además repetido, y no está renderizando los mensajes configurados en `featured_quotes["message_ids"]`.

### Comportamiento requerido

Corregir la sección para que:

1. renderice los mensajes configurados en `ROMANTIC_CONTENT["featured_quotes"]["message_ids"]`;
2. mantenga el orden de esos IDs;
3. use fallback automático solo si `message_ids` está vacío;
4. no repita el título innecesariamente;
5. si hay IDs inválidos o inexistentes, los ignore de forma segura;
6. si después de resolver IDs no hay mensajes, no debe mostrar una sección vacía con solo título.

### Reglas

- Usar `message` para texto visible.
- No usar `message_normalized` para UI.
- Escapar contenido dinámico con `html.escape` o el helper equivalente.
- Mantener estilo actual de cards/frases bonitas.
- No convertirlo en tabla.

---

## Requerimientos técnicos

### Helper para obtener mensajes por ID

Si no existe un helper robusto, crear o corregir uno equivalente a:

```python
def get_messages_by_ids(message_ids: list[int]) -> list[dict]:
    ...
```

Debe cumplir:

- ignorar `None`;
- ignorar valores no enteros;
- consultar por `id`;
- devolver al menos `id`, `sender`, `message`, `timestamp`, `source` si existe;
- mantener el orden exacto de los IDs configurados;
- usar SQL parametrizado;
- no construir SQL inseguro con f-strings;
- manejar listas vacías.

Ejemplo de ordenamiento en Python:

```python
records_by_id = {record["id"]: record for record in records}
ordered_records = [
    records_by_id[message_id]
    for message_id in message_ids
    if message_id in records_by_id
]
```

---

## Validaciones esperadas

Agregar o actualizar pruebas si el proyecto ya tiene tests.

Validar al menos:

1. `her_messages` se resuelve como un bloque agrupado.
2. `conversation_pair` mantiene el orden manual de IDs.
3. `featured_quotes` renderiza mensajes por IDs cuando la lista no está vacía.
4. `featured_quotes` usa fallback solo si `message_ids` está vacío.
5. No aparece `Â·` en strings de metadata renderizados.
6. No se muestran secciones vacías con solo título.
7. `get_reserved_message_ids()` incluye también IDs de `featured_quotes`, para evitar duplicados automáticos si aplica.

---

## Documentación requerida

Actualizar documentación de sesión, preferiblemente:

```text
docs/codex_session_debug.md
```

o el archivo equivalente de bitácora del proyecto.

Agregar una sección con título similar a:

```text
Corrección de bloques especiales, frases bonitas y encoding visual
```

Documentar brevemente:

- qué archivo se modificó;
- qué componente renderiza `her_messages`;
- qué componente renderiza `conversation_pair`;
- cómo se corrige el carácter `Â·`;
- cómo se resuelven los IDs de `featured_quotes`;
- cómo editar la configuración desde `content_config.py`.

También actualizar `docs/content_configuration.md` si existe, explicando:

- cómo configurar `special_message.blocks`;
- cómo usar `her_messages`;
- cómo usar `conversation_pair`;
- cómo configurar `featured_quotes.message_ids`.

---

## Restricciones

- No cambiar el diseño general de la landing.
- No tocar ETL salvo que sea estrictamente necesario para corregir encoding visible.
- No cambiar IDs configurados por el usuario.
- No exponer errores técnicos en la UI.
- No eliminar contenido configurado.
- No renderizar HTML desde mensajes de base de datos sin escape.
- No usar `message_normalized` para mostrar texto.
- No romper reveal-on-scroll.
- No romper los gráficos ni las métricas existentes.

---

## Resultado esperado

La sección debe quedar así conceptualmente:

```text
Un mensaje que quiero guardar

[RECUADRO 1]
Cosas bonitas que ella me dijo
- mensaje 5038
- mensaje 5039
- mensaje 5040
- mensaje 5041
- mensaje 5042

[RECUADRO 2]
Una conversación que quiero recordar
        David: mensaje 6157
        David: mensaje 6156
        David: mensaje 6155
Mar: mensaje 6151
Mar: mensaje 6150
...
```

Y la sección de frases bonitas debe mostrar realmente las frases configuradas por ID, sin repetir título vacío ni dejar una sección incompleta.

---

## Formato de respuesta esperado

Devuelve:

1. lista de archivos modificados;
2. código completo solo de los archivos modificados;
3. breve resumen técnico de qué se corrigió;
4. comandos de prueba ejecutados o recomendados.
