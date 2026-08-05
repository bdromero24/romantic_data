# Prompt para Codex — `message_key` idempotente, backup de mensajes parametrizados y evaluación de UPSERT

## 1. Contexto del problema

El proyecto es una landing romántica hecha en **Python + Streamlit**. La app usa conversaciones de WhatsApp e Instagram cargadas en PostgreSQL y luego renderiza datos/mensajes en la UI.

Actualmente hay mensajes seleccionados manualmente en `content_config.py` mediante IDs de la tabla `messages`, por ejemplo:

```python
"message_id": 18729
```

El problema es que esos IDs son autoincrementales. Si hago:

```sql
TRUNCATE TABLE messages RESTART IDENTITY;
```

y luego vuelvo a cargar las conversaciones con el ETL, los IDs pueden cambiar. Eso haría que la landing renderice mensajes incorrectos, porque `content_config.py` seguiría apuntando a IDs antiguos.

Necesito robustecer el proyecto para que los mensajes parametrizados no dependan exclusivamente del `id`.

---

## 2. Objetivo general

Implementar una llave idempotente estable llamada:

```text
message_key
```

para identificar mensajes de forma determinística aunque cambien los IDs.

Además, antes de modificar el modelo, Codex debe:

1. analizar el proyecto;
2. identificar todos los mensajes parametrizados actualmente en `content_config.py`;
3. generar un backup de esos IDs y sus mensajes reales;
4. evaluar si para este proyecto es suficiente dejar de hacer `TRUNCATE` y usar `UPSERT`;
5. modificar el proceso de inserción para que, de ahora en adelante, funcione como un `UPSERT`/insert idempotente seguro.

---

## 3. Análisis obligatorio previo

Antes de cambiar código, analiza el proyecto y responde en un archivo de documentación o reporte:

```text
docs/message_key_migration_analysis.md
```

El análisis debe incluir:

1. Dónde está la tabla `messages`.
2. Dónde está definido el `INSERT_MESSAGE_QUERY`.
3. Dónde se ejecuta el ETL/load.
4. Dónde está `content_config.py`.
5. Qué bloques de `content_config.py` usan `message_id`.
6. Si existen funciones que recuperan mensajes por ID.
7. Si ya existe una constraint única en la tabla `messages`.
8. Si el `ON CONFLICT` actual ya hace que el ETL sea idempotente.
9. Si es suficiente para este proyecto cambiar el flujo a `UPSERT`/insert idempotente y dejar de hacer `TRUNCATE`.
10. Riesgos de seguir usando `message_id`.
11. Recomendación técnica final.

---

## 4. Backup obligatorio de mensajes parametrizados

Antes de cualquier migración, crear un script:

```text
scripts/backup_configured_messages.py
```

Este script debe:

1. Leer `content_config.py`.
2. Extraer todos los IDs manuales configurados, incluyendo:
   - `first_te_amo`;
   - `special_message`;
   - `special_message["blocks"][*]["message_ids"]`;
   - `special_message["blocks"][*]["messages"][*]["message_id"]`;
   - `timeline[*]["message_id"]`;
   - `featured_quotes["message_ids"]`;
   - cualquier otro bloque manual que use `message_id`.
3. Ignorar `None`, strings vacíos, booleanos y valores no enteros.
4. Consultar esos IDs en la tabla `messages`.
5. Exportar un backup a:

```text
data/backups/configured_messages_backup_YYYYMMDD_HHMMSS.csv
data/backups/configured_messages_backup_YYYYMMDD_HHMMSS.json
```

Cada registro del backup debe incluir:

```text
config_path
message_id
source
sender
message
message_normalized
timestamp
created_at si existe
message_key si existe
found_in_database
```

Donde `config_path` sea algo legible, por ejemplo:

```text
ROMANTIC_CONTENT.first_te_amo.message_id
ROMANTIC_CONTENT.special_message.blocks[0].message_ids[2]
ROMANTIC_CONTENT.featured_quotes.message_ids[4]
```

Si algún ID configurado no existe en la base de datos, debe quedar en el backup con:

```text
found_in_database = false
```

El script debe imprimir un resumen:

```text
Total IDs configurados encontrados: X
Total encontrados en DB: Y
Total no encontrados: Z
Backup generado en: ...
```

---

## 5. Agregar columna `message_key`

Agregar una columna nueva a la tabla `messages`:

```sql
message_key TEXT
```

La columna debe crearse inicialmente como **nullable** para no romper registros existentes.

Actualizar `db/schema.sql` o el mecanismo equivalente del proyecto.

Ejemplo:

```sql
ALTER TABLE messages
ADD COLUMN IF NOT EXISTS message_key TEXT;
```

No marcarla como `NOT NULL` en la primera fase.

---

## 6. Construcción determinística de `message_key`

Implementar una función reutilizable, por ejemplo:

```python
def build_message_key(record: dict) -> str:
    ...
```

Ubicación sugerida:

```text
etl/message_key.py
```

o en el módulo de transformación si encaja mejor con la arquitectura actual.

La llave debe ser determinística y estable.

Usar `sha256`.

La llave debe construirse con estos campos normalizados:

```text
source
sender
timestamp en formato ISO estable
message_normalized
```

Ejemplo conceptual:

```text
source|sender|timestamp_iso|message_normalized
```

Reglas:

- `source`: `strip().lower()`
- `sender`: `strip()`
- `timestamp`: convertir a formato ISO estable
- `message_normalized`: `strip()`
- usar separador fijo `|`
- manejar `None` como string vacío
- codificar en UTF-8
- retornar hash hexadecimal

---

## 7. Backfill de `message_key` para registros existentes

Crear script:

```text
scripts/backfill_message_keys.py
```

Este script debe:

1. Buscar registros en `messages` donde `message_key IS NULL`.
2. Calcular `message_key` usando exactamente la misma función del ETL.
3. Actualizar cada registro.
4. Validar duplicados.
5. Reportar resultados.

Resumen esperado:

```text
Registros sin message_key: X
Registros actualizados: Y
Duplicados detectados: Z
```

Consulta de duplicados:

```sql
SELECT message_key, COUNT(*)
FROM messages
WHERE message_key IS NOT NULL
GROUP BY message_key
HAVING COUNT(*) > 1;
```

Si hay duplicados, no crear índice único todavía y documentar los casos.

---

## 8. Índice único sobre `message_key`

Después del backfill y solo si no hay duplicados, crear índice único:

```sql
CREATE UNIQUE INDEX IF NOT EXISTS ux_messages_message_key
ON messages (message_key);
```

Si Codex decide dejar este paso manual por seguridad, debe documentarlo claramente.

No forzar `NOT NULL` todavía.

---

## 9. Modificar ETL para guardar `message_key`

Modificar el proceso de transformación/carga para que cada registro nuevo tenga:

```python
record["message_key"]
```

Antes de llegar al `INSERT`.

El flujo ideal es:

```text
extract
transform
build_message_key
load
```

No romper el ETL actual.

---

## 10. Modificar `INSERT_MESSAGE_QUERY`

La query actual es similar a:

```python
INSERT_MESSAGE_QUERY: TextClause = text(
    """
    INSERT INTO messages (
        sender,
        message,
        message_normalized,
        timestamp,
        source
    )
    VALUES (
        :sender,
        :message,
        :message_normalized,
        :timestamp,
        :source
    )
    ON CONFLICT (source, sender, message, timestamp)
    DO NOTHING
    """
)
```

Modificarla para incluir `message_key`.

Primera opción conservadora recomendada:

```python
INSERT_MESSAGE_QUERY: TextClause = text(
    """
    INSERT INTO messages (
        sender,
        message,
        message_normalized,
        timestamp,
        source,
        message_key
    )
    VALUES (
        :sender,
        :message,
        :message_normalized,
        :timestamp,
        :source,
        :message_key
    )
    ON CONFLICT (source, sender, message, timestamp)
    DO UPDATE SET
        message_normalized = EXCLUDED.message_normalized,
        message_key = COALESCE(messages.message_key, EXCLUDED.message_key)
    """
)
```

### Importante

Codex debe analizar si conviene:

### Opción A — Mantener `ON CONFLICT (source, sender, message, timestamp)`

Esta opción es más conservadora porque respeta la constraint actual.

Ventaja:

- reduce riesgo de romper ETL;
- conserva comportamiento actual;
- permite empezar a poblar `message_key`;
- permite pasar de `DO NOTHING` a `DO UPDATE` solo para completar `message_key`.

### Opción B — Cambiar a `ON CONFLICT (message_key)`

Solo debe hacerse si:

- `message_key` ya existe para todos los registros;
- no hay duplicados;
- existe índice único;
- se validó que la key es estable.

Para esta primera implementación, preferir la **Opción A**, salvo que el análisis del proyecto demuestre que la Opción B es segura.

---

## 11. Evaluación explícita de UPSERT

Codex debe responder en `docs/message_key_migration_analysis.md`:

1. ¿El ETL actual ya es idempotente con `ON CONFLICT DO NOTHING`?
2. ¿Qué diferencia hay entre el insert actual y un UPSERT?
3. ¿Es suficiente dejar de hacer `TRUNCATE` y correr el ETL completo con `ON CONFLICT`?
4. ¿Conviene cambiar `DO NOTHING` por `DO UPDATE`?
5. ¿Qué campos deberían actualizarse en caso de conflicto?
6. ¿Qué campos NO deberían actualizarse?
7. ¿Qué riesgo hay de actualizar `message`, `timestamp` o `sender`?
8. ¿Cuál es la estrategia recomendada para este proyecto?

La recomendación esperada es algo parecido a:

```text
No hacer TRUNCATE.
Usar carga incremental/idempotente.
Mantener IDs existentes.
Insertar nuevos mensajes.
Agregar message_key para referencias estables.
Migrar gradualmente content_config.py de message_id a message_key.
```

---

## 12. Soporte en `content_config.py` para `message_key`

Modificar las funciones que recuperan mensajes manuales para soportar tanto `message_id` como `message_key`.

Regla:

```text
Si existe message_key, buscar por message_key.
Si no existe message_key, usar message_id como fallback.
```

Ejemplo:

```python
{
    "message_id": 18729,
    "message_key": "abc123..."
}
```

Esto debe aplicar a:

- `first_te_amo`;
- `special_message`;
- `special_message["blocks"][*]["message_ids"]`;
- `special_message["blocks"][*]["messages"][*]["message_id"]`;
- `timeline`;
- `featured_quotes`;
- cualquier otro bloque manual.

No eliminar soporte de `message_id`.

---

## 13. Script para ayudar a migrar `content_config.py`

Crear opcionalmente:

```text
scripts/export_content_config_message_keys.py
```

Este script debe:

1. leer los IDs configurados actuales;
2. buscar esos mensajes en DB;
3. exportar una tabla que sugiera reemplazos:

```text
config_path
message_id
message_key
sender
message
timestamp
```

No debe modificar automáticamente `content_config.py` salvo que sea muy seguro.

Mejor generar un archivo de apoyo:

```text
data/backups/content_config_message_key_mapping_YYYYMMDD_HHMMSS.csv
```

---

## 14. No romper modo estático

El proyecto usa `USE_STATIC_DATA=true` para Streamlit Cloud.

La implementación no debe romper:

```powershell
$env:USE_STATIC_DATA="true"
streamlit run app/main.py
```

El modo estático debe seguir leyendo `data/final/landing_data.json`.

---

## 15. Tests requeridos

Agregar tests para:

1. `build_message_key` es determinístico.
2. Dos registros iguales generan la misma key.
3. Si cambia `timestamp`, cambia la key.
4. Si cambia `message_normalized`, cambia la key.
5. Si cambia `source`, cambia la key.
6. Si existe `message_key`, la búsqueda manual lo prefiere sobre `message_id`.
7. Si no existe `message_key`, usa `message_id` como fallback.
8. El `INSERT_MESSAGE_QUERY` incluye `message_key`.
9. El backup de mensajes parametrizados ignora `None` y valores inválidos.

---

## 16. Documentación requerida

Actualizar o crear:

```text
docs/message_key_migration_analysis.md
docs/content_configuration.md
docs/codex_session_debug.md
```

Documentar:

- qué es `message_key`;
- por qué `id` no es suficiente;
- cómo hacer backup de mensajes configurados;
- cómo ejecutar backfill;
- cómo validar duplicados;
- cómo obtener `message_key` de un mensaje;
- cómo migrar gradualmente de `message_id` a `message_key`;
- por qué no se recomienda seguir haciendo `TRUNCATE`;
- cómo usar el ETL de ahora en adelante;
- diferencia entre insert idempotente y upsert.

---

## 17. Orden obligatorio de ejecución

Codex debe dejar claro este orden:

```text
1. Ejecutar backup de mensajes parametrizados.
2. Agregar columna message_key.
3. Ejecutar backfill.
4. Validar duplicados.
5. Crear índice único si aplica.
6. Modificar ETL para generar message_key.
7. Modificar INSERT/UPSERT.
8. Agregar soporte message_key en la recuperación de mensajes manuales.
9. Exportar mapping message_id -> message_key.
10. Probar.
11. Solo después considerar migrar content_config.py manualmente.
```

---

## 18. Comandos esperados

Incluir comandos como:

```powershell
python scripts/backup_configured_messages.py
python scripts/backfill_message_keys.py
python scripts/export_content_config_message_keys.py
pytest tests/
```

Y para probar app:

```powershell
$env:USE_STATIC_DATA="true"
streamlit run app/main.py

$env:USE_STATIC_DATA="false"
streamlit run app/main.py
```

---

## 19. Restricciones

- No hacer `TRUNCATE`.
- No borrar datos.
- No modificar visualmente la landing.
- No cambiar textos románticos.
- No modificar `landing_data.json` salvo que se solicite.
- No eliminar soporte para `message_id`.
- No forzar `message_key NOT NULL` en la primera fase.
- No cambiar a `ON CONFLICT (message_key)` sin validar duplicados e índice único.
- No hacer cambios destructivos en la base de datos.

---

## 20. Entregable

Devuélveme:

1. análisis técnico del proyecto;
2. archivos creados/modificados;
3. código completo por archivo;
4. SQL/migraciones necesarias;
5. comandos de ejecución;
6. resultado esperado de cada script;
7. explicación clara de si es suficiente usar UPSERT;
8. recomendación final sobre si debo dejar de hacer `TRUNCATE`;
9. pasos para migrar gradualmente `content_config.py` de `message_id` a `message_key`.
