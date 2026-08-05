# Analisis de migracion a message_key

## Hallazgos del proyecto

1. La tabla `messages` esta definida en `db/schema.sql`.
2. `INSERT_MESSAGE_QUERY` esta definido en `db/queries.py`.
3. El ETL se ejecuta desde `scripts/run_etl.py`; la carga final vive en
   `etl/load.py`.
4. La configuracion manual esta en `app/content_config.py`.
5. Bloques que usan `message_id`:
   - `ROMANTIC_CONTENT["special_message"]["message_id"]`
   - `ROMANTIC_CONTENT["special_message"]["blocks"][*]["message_ids"]`
   - `ROMANTIC_CONTENT["special_message"]["blocks"][*]["messages"][*]["message_id"]`
   - `ROMANTIC_CONTENT["first_te_amo"]["message_id"]`
   - `ROMANTIC_CONTENT["timeline"][*]["message_id"]`
   - `ROMANTIC_CONTENT["featured_quotes"]["message_ids"]`
6. Funciones que recuperan mensajes por ID:
   - `db/romantic_queries.py`: `fetch_message_by_id()` y
     `fetch_messages_by_ids()`
   - `services/romantic_metrics.py`: `_fetch_configured_message()`,
     `_fetch_manual_timeline_message()`, `_build_her_messages_block()`,
     `_build_conversation_pair_block()` y `_build_manual_featured_messages()`
7. Ya existe constraint unica:
   `uq_messages_source_sender_message_timestamp` sobre
   `(source, sender, message, timestamp)`.
8. El `ON CONFLICT DO NOTHING` anterior hacia idempotente la carga frente a
   duplicados exactos por `(source, sender, message, timestamp)`, pero no
   completaba campos derivados nuevos como `message_key`.
9. Para este proyecto si es suficiente dejar de hacer `TRUNCATE` y usar carga
   incremental/idempotente con `ON CONFLICT`, porque conserva los IDs actuales
   y evita que `content_config.py` apunte a mensajes equivocados.
10. Riesgos de seguir usando solo `message_id`:
    - un `TRUNCATE ... RESTART IDENTITY` cambia IDs;
    - una restauracion parcial puede desplazar IDs;
    - una carga en otro ambiente puede asignar IDs distintos;
    - la landing puede renderizar mensajes incorrectos sin fallar.
11. Recomendacion tecnica: no hacer `TRUNCATE`; mantener la constraint
    actual; agregar `message_key`; backfillear registros existentes; crear
    indice unico solo si no hay duplicados; migrar `content_config.py`
    gradualmente agregando `message_key` junto a `message_id`.

## Evaluacion de UPSERT

El ETL anterior ya era idempotente para duplicados exactos porque usaba
`ON CONFLICT (source, sender, message, timestamp) DO NOTHING`.

La diferencia con un UPSERT es que `DO NOTHING` ignora el registro conflictivo,
mientras que `DO UPDATE` permite completar o refrescar campos derivados sin
crear duplicados.

Es suficiente dejar de hacer `TRUNCATE` y ejecutar el ETL completo con
`ON CONFLICT`, siempre que la fuente mantenga los mismos campos de identidad.
Esto conserva IDs existentes e inserta solo mensajes nuevos.

Conviene cambiar `DO NOTHING` por `DO UPDATE` de forma conservadora para:

- actualizar `message_normalized`;
- completar `message_key` cuando el registro existente lo tenga en `NULL`.

No conviene actualizar:

- `source`;
- `sender`;
- `message`;
- `timestamp`;
- `id`;
- `created_at`.

Actualizar `message`, `timestamp` o `sender` puede romper la identidad del
mensaje, cambiar el hash esperado y hacer que una referencia manual apunte a
otro contenido.

Estrategia recomendada:

1. Ejecutar backup de mensajes parametrizados.
2. Agregar columna `message_key`.
3. Ejecutar backfill.
4. Validar duplicados.
5. Crear indice unico si aplica.
6. Modificar ETL para generar `message_key`.
7. Modificar INSERT/UPSERT.
8. Agregar soporte `message_key` en recuperacion manual.
9. Exportar mapping `message_id -> message_key`.
10. Probar.
11. Solo despues considerar migrar `content_config.py` manualmente.

## SQL/migraciones necesarias

```sql
ALTER TABLE messages
ADD COLUMN IF NOT EXISTS message_key TEXT;
```

Despues del backfill, y solo si la validacion no muestra duplicados:

```sql
CREATE UNIQUE INDEX IF NOT EXISTS ux_messages_message_key
ON messages (message_key);
```

No se debe marcar `message_key` como `NOT NULL` en esta fase.

## Comandos

```powershell
python scripts/backup_configured_messages.py
python scripts/backfill_message_keys.py
python scripts/export_content_config_message_keys.py
pytest tests/
```

Prueba de app:

```powershell
$env:USE_STATIC_DATA="true"
streamlit run app/main.py

$env:USE_STATIC_DATA="false"
streamlit run app/main.py
```

## Resultado esperado

`scripts/backup_configured_messages.py` genera:

```text
data/backups/configured_messages_backup_YYYYMMDD_HHMMSS.csv
data/backups/configured_messages_backup_YYYYMMDD_HHMMSS.json
```

Resumen esperado:

```text
Total IDs configurados encontrados: X
Total encontrados en DB: Y
Total no encontrados: Z
Backup generado en: ...
```

`scripts/backfill_message_keys.py` actualiza solo filas con
`message_key IS NULL`, valida duplicados y crea
`ux_messages_message_key` solo si no hay duplicados.

Resumen esperado:

```text
Registros sin message_key: X
Registros actualizados: Y
Duplicados detectados: Z
```

`scripts/export_content_config_message_keys.py` genera:

```text
data/backups/content_config_message_key_mapping_YYYYMMDD_HHMMSS.csv
```

## Migracion gradual de content_config.py

1. Ejecutar el backup.
2. Ejecutar backfill.
3. Exportar el mapping.
4. Para cada mensaje manual, agregar `message_key` sin borrar `message_id`:

```python
{
    "message_id": 18729,
    "message_key": "hash_sha256",
}
```

5. Para listas, agregar una lista paralela `message_keys` en el mismo orden:

```python
{
    "message_ids": [123, 456],
    "message_keys": ["hash_123", "hash_456"],
}
```

La app primero busca por `message_key`; si no existe o no encuentra fila, usa
`message_id` como fallback.
