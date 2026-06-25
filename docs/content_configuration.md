# Configuracion manual de contenido romantico

## Archivo principal

La configuracion manual vive en:

```text
app/content_config.py
```

Ese archivo contiene `ROMANTIC_CONTENT`, `DISPLAY_LABELS` y el helper `get_reserved_message_ids()`.

Regla general:

```text
message_normalized -> busquedas, filtros y conteos
message            -> textos originales visibles en la UI
DISPLAY_LABELS     -> labels visibles para palabras normalizadas
```

## Configuracion visual del hero

La fresa 8-bit del hero se carga desde:

```text
ui/assets/strawberry_8bit.png
```

La ruta se define en `ui/components.py` con `Path(__file__).parent`, sin rutas absolutas de maquina.

Para cambiar la imagen, reemplaza ese PNG por otro asset con fondo transparente. Si cambias el nombre del archivo, actualiza:

```python
STRAWBERRY_IMAGE = ASSETS_DIR / "strawberry_8bit.png"
```

El circulo decorativo y la imagen se controlan en `ui/styles.py` con:

```css
.hero-orb
.hero-strawberry
```

Este ajuste no modifica ETL, consultas ni logica de datos.

## Como editar "Un mensaje que quiero guardar"

La seccion se configura en:

```python
ROMANTIC_CONTENT["special_message"]["blocks"]
```

La estructura permite varios bloques manuales. Si `blocks` no tiene IDs validos, la app conserva el fallback heredado de:

```python
ROMANTIC_CONTENT["special_message"]["message_id"]
```

### Varios mensajes de ella

Edita `message_ids` con IDs reales de la tabla `messages`:

```python
{
    "type": "her_messages",
    "title": "Cosas bonitas que ella me dijo",
    "message_ids": [123, 456, 789],
}
```

La app consulta esos mensajes por `id`, mantiene el orden de la lista y los renderiza como burbujas de ella dentro de un solo recuadro visual para ese bloque.

### Conversacion mio + respuesta de ella

Edita cada `message_id` dentro de `messages`:

```python
{
    "type": "conversation_pair",
    "title": "Una conversacion que quiero recordar",
    "messages": [
        {"role": "me", "message_id": 111},
        {"role": "her", "message_id": 222},
    ],
}
```

Reglas de rol:

```text
role = "me"  -> burbuja alineada a la derecha
role = "her" -> burbuja alineada a la izquierda
```

Si aparece un rol no reconocido, la app lo trata como `"her"`.

Cada bloque `conversation_pair` se renderiza en su propio recuadro visual, separado de los bloques `her_messages`, y conserva el orden manual de `messages`.

## Como editar "Mensajes para volver a leer despacio"

La seccion se configura en:

```python
ROMANTIC_CONTENT["featured_quotes"]["message_ids"]
```

Ejemplo:

```python
"message_ids": [123, 456, 789]
```

Si la lista contiene IDs, la app muestra exactamente esos mensajes disponibles, en el orden configurado. Si la lista queda vacia, se activa el fallback automatico con `fallback_limit`.

El fallback automatico solo se usa cuando `message_ids` esta vacio. Si la lista tiene valores invalidos o IDs inexistentes, esos valores se ignoran de forma segura y no se muestra una seccion vacia con solo titulo.

## Que ID usar

Usa el valor de la columna `id` de la tabla `messages`.

No uses el numero de fila visual del visor de base de datos, porque ese numero puede cambiar segun filtros, ordenamientos o paginacion.

## Que pasa si dejo IDs vacios o None

- `None` significa no usar mensaje manual en ese campo.
- Una lista vacia en `blocks[*]["message_ids"]` omite ese bloque.
- Una lista vacia en `featured_quotes["message_ids"]` activa el fallback automatico.
- La app no debe fallar si un ID no existe o si un bloque queda sin mensajes validos.

## Evitar duplicados

`get_reserved_message_ids()` recolecta IDs manuales usados en:

```python
ROMANTIC_CONTENT["special_message"]["message_id"]
ROMANTIC_CONTENT["special_message"]["blocks"][*]["message_ids"]
ROMANTIC_CONTENT["special_message"]["blocks"][*]["messages"][*]["message_id"]
ROMANTIC_CONTENT["first_te_amo"]["message_id"]
ROMANTIC_CONTENT["timeline"][*]["message_id"]
ROMANTIC_CONTENT["featured_quotes"]["message_ids"]
```

Cuando `featured_quotes["message_ids"]` esta vacio, el fallback automatico excluye esos IDs reservados para evitar repeticiones en frases bonitas.

## Separador visual de metadata

La metadata de burbujas de mensaje se renderiza con un separador HTML seguro:

```html
<span class="message-meta-separator">-</span>
```

Esto evita mojibake visible como `Ã‚Â·` en la UI.

## Seguridad HTML

Los mensajes que vienen de la base de datos se escapan con `html.escape` antes de renderizarse.

No metas HTML en mensajes crudos de la tabla `messages`; se mostrara como texto seguro, no como HTML.

En textos manuales de `app/content_config.py`, la app permite solamente `<strong>...</strong>` limpio mediante el sanitizador de componentes.

## Como cambiar labels visibles

`message_normalized` puede contener texto sin tildes ni `ñ`, por ejemplo `te extrano`, porque se usa para busquedas y conteos.

Para mostrar el label correcto en la UI, edita:

```python
DISPLAY_LABELS = {
    "te extrano": "te extraño",
}
```

## Como editar el timeline

El timeline se controla en:

```python
ROMANTIC_CONTENT["timeline"]
```

Para agregar un hito manual:

```python
{
    "title": "Un mensaje que quiero recordar",
    "message_id": 40210,
    "mode": "manual_message",
}
```

Modos automaticos disponibles:

```text
auto_first_message
auto_first_te_amo
auto_first_te_extrano
auto_first_happy_message
auto_peak_day
auto_peak_month
```
