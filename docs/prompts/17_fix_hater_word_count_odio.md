# Prompt para Codex — corregir conteo de ocurrencias de “odio” en card Hater

## Contexto

La landing romántica ya tiene una card nueva tipo KPI/metric card con el inside joke:

- título: `Hater de tiempo completo`
- palabra central: `odio`
- texto inferior: `Utilizaste la palabra odio X veces`

Actualmente la UI está mostrando:

```text
Utilizaste la palabra odio 0 veces
```

Esto es incorrecto. En DBeaver confirmé que existen muchos registros en `messages.message_normalized` que contienen la palabra `odio`, por ejemplo:

```text
odio
odio todo
los odio
ay como los odio
como odio
como odio la vainilla
lo odio
odio hate
odio madrugar
pero por que ese odio
como la odio
como odio coser
como odio el aluminio de eso
```

Por tanto, el bug no es de ausencia de datos. Puede estar en:

- el patrón regex enviado como parámetro;
- el valor de `sender_name`;
- la función que ejecuta la query;
- el mapeo del resultado hacia la métrica;
- el render de la card;
- el uso incorrecto de `message` vs `message_normalized`;
- diferencias entre sender visible y sender real en base de datos.
- Tambien en el  :pattern

---

## Query actual

La query actual es esta:

```python
ROMANTIC_HATER_WORD_COUNT_QUERY: TextClause = text(
    """
    SELECT COUNT(*) AS total_odio
    FROM messages
    WHERE sender = :sender_name
      AND message_normalized IS NOT NULL
      AND BTRIM(message_normalized) <> ''
      AND LOWER(BTRIM(message_normalized)) NOT IN (
          'null',
          'none',
          'nan',
          'na',
          'n/a'
      )
      AND message_normalized ~* :pattern
    """
)
```

No asumas que la query está mal sin verificar todo el flujo. El problema visible es que la card recibe o renderiza `0` aunque la base sí contiene ocurrencias.

---

## Objetivo

Corregir el bug para que la card **Hater de tiempo completo** cuente correctamente todas las ocurrencias de la palabra `odio` dichas por ella.

Debe contar la ocurrencia de `odio` como palabra dentro del mensaje, no solo mensajes exactamente iguales a `odio`.

Ejemplos que deben contar:

```text
odio
odio todo
los odio
como odio
lo odio
como la odio
como odio coser
odio madrugar
```

Ejemplos que no deberían contar si no contienen la palabra completa `odio`:

```text
odioso
odiosamente
```

---

## Requisitos técnicos

### 1. Validar el sender real

Antes de modificar la lógica, verifica cómo se está definiendo el `sender_name` usado para ella.

Debes comprobar:

- cuál es el sender exacto de ella en `messages.sender`;
- si la configuración usa el mismo string exacto;
- si hay diferencias por emojis, espacios, mayúsculas, alias o caracteres invisibles;
- si la función está recibiendo `sender_name=None`, vacío o un nombre distinto.

Agrega una corrección limpia si el problema es el sender.

No hardcodees el nombre de ella dentro de la query si ya existe configuración para eso.

---

### 2. Corregir el patrón regex

El patrón debe contar la palabra `odio` como palabra completa en PostgreSQL.

Usa una de estas alternativas robustas:

```python
pattern = r"\modio\M"
```

O, si se decide contar `odio` y `hate` como parte del mismo inside joke:

```python
pattern = r"\m(odio|hate)\M"
```

Importante:

- el patrón debe llegar correctamente a PostgreSQL;
- no debe quedar doblemente escapado de forma incorrecta;
- no debe buscar el string literal `\\modio\\M` si eso rompe la coincidencia;
- no debe usar `%odio%` si se puede resolver con regex por palabra completa.

---

### 3. Confirmar que se usa `message_normalized`

La búsqueda debe hacerse sobre:

```text
message_normalized
```

No usar `message` para la búsqueda.

---

### 4. Contar ocurrencias, no solo mensajes si aplica

Quiero contar cuántas veces aparece la palabra `odio`.

Si un mensaje contiene `odio` una vez, cuenta 1.

Si un mensaje contiene `odio` varias veces, preferiblemente debe contar cada ocurrencia.

Ejemplo:

```text
odio odio odio
```

Resultado esperado: 3 ocurrencias.

Si el proyecto ya venía contando mensajes y cambiar esto implica demasiada complejidad, implementa correctamente al menos el conteo de mensajes que contienen `odio`, pero deja documentada la diferencia. Preferencia: **contar ocurrencias reales**.

Para contar ocurrencias reales en PostgreSQL, puedes usar una estrategia como:

```sql
SELECT COALESCE(SUM(
    array_length(
        regexp_matches(message_normalized, :pattern, 'gi'),
        1
    )
), 0) AS total_odio
```

Pero valida la sintaxis correcta, porque `regexp_matches` retorna set y puede requerir `regexp_count` si la versión de PostgreSQL lo soporta, o un `CROSS JOIN LATERAL`.

Alternativa recomendada si PostgreSQL tiene `regexp_count`:

```sql
SELECT COALESCE(SUM(regexp_count(message_normalized, :pattern, 1, 'i')), 0) AS total_odio
FROM messages
WHERE sender = :sender_name
  AND message_normalized IS NOT NULL
  AND BTRIM(message_normalized) <> ''
  AND LOWER(BTRIM(message_normalized)) NOT IN ('null', 'none', 'nan', 'na', 'n/a');
```

Si `regexp_count` no está disponible, usa una alternativa compatible con la versión del proyecto.

---

### 5. Validar el mapeo del resultado

Revisar que la función que ejecuta la query esté leyendo exactamente:

```text
total_odio
```

y no otro alias.

Validar que el valor se convierta correctamente a `int`.

Evitar que un `None` o un error silencioso termine en `0` sin logging.

---

### 6. Revisar el render de la card

Verificar que la card esté leyendo la métrica correcta y no un campo equivocado.

Debe renderizar:

```text
Utilizaste la palabra odio {count} veces
```

Donde `{count}` sea el valor real devuelto por la query.

---

## Debug mínimo requerido

Agrega logs o prints temporales solo si el proyecto tiene una forma segura de logging. No mostrar debug técnico en UI.

Necesito que puedas verificar internamente:

- sender usado;
- patrón usado;
- resultado crudo de la query;
- valor final enviado a la card.

Si agregas logs, que sean seguros y no expongan credenciales.

---

## Pruebas requeridas

Agregar o actualizar pruebas si el proyecto tiene tests.

Mínimo validar con casos unitarios o integración controlada:

1. `odio` cuenta 1.
2. `odio todo` cuenta 1.
3. `los odio` cuenta 1.
4. `odio odio` cuenta 2 si se implementa conteo de ocurrencias.
5. `odioso` no cuenta.
6. mensajes de otro sender no cuentan.
7. valores `null`, `none`, `nan`, `na`, `n/a` no cuentan.
8. el valor final llega a la card como entero mayor que 0 cuando hay datos.

---

## Documentación

Actualizar la documentación de sesión correspondiente, por ejemplo:

```text
docs/codex_session_debug.md
```

o el documento de debug equivalente del proyecto.

Debe explicar brevemente:

- bug detectado: card Hater mostraba 0 aunque existían mensajes con `odio`;
- causa raíz encontrada;
- archivos modificados;
- query/helper corregido;
- cómo se valida el conteo;
- si se cuentan mensajes que contienen `odio` o ocurrencias reales de `odio`.

---

## Restricciones

- No modificar el diseño general de la landing.
- No cambiar el copy visual de la card salvo que sea estrictamente necesario.
- No usar `message` para la búsqueda.
- No hardcodear credenciales ni datos sensibles.
- No silenciar errores con `except: pass`.
- No mostrar errores técnicos en UI.
- No romper otras métricas románticas.
- Mantener SQL parametrizado.

---

## Resultado esperado

La card debe dejar de mostrar `0` y mostrar el conteo real de `odio` dicho por ella.

Ejemplo visual esperado:

```text
Hater de tiempo completo
odio
Utilizaste la palabra odio 37 veces
```

El número debe provenir de una query real sobre `messages.message_normalized`, filtrada por el sender de ella.

---

## Formato de respuesta esperado

Devuélveme:

1. archivos modificados;
2. código completo o diff claro por archivo;
3. pruebas ejecutadas y resultado;
4. causa raíz del bug en una explicación corta;
5. documentación actualizada.
