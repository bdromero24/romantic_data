# Sesion 13: card Hater de tiempo completo

## Fecha

```text
2026-06-19
```

## Objetivo

Agregar una card en `Pequeños datos bonitos` para mostrar el inside joke:

- `Hater de tiempo completo`
- `odio`
- `Utilizaste la palabra odio X veces`

## Archivos modificados

- `app/content_config.py`
- `db/queries.py`
- `db/romantic_queries.py`
- `services/romantic_metrics.py`
- `tests/test_romantic_metrics.py`
- `tests/test_romantic_queries.py`
- `docs/sessions/13_hater_card_odio_20260619.md`
- `README.MD`

## Cambios aplicados

### Configuracion

`app/content_config.py` define `HER_SENDER_NAME` para centralizar el sender de ella.

### Consulta

`db/queries.py` agrega `ROMANTIC_HATER_WORD_COUNT_QUERY`.

La query:

- filtra por `sender = :sender_name`;
- usa `message_normalized`;
- descarta nulos, vacios y marcadores invalidos;
- cuenta ocurrencias reales con `regexp_count(message_normalized, :pattern, 1, 'i')`;
- usa regex por palabra con `\m(odio|hate)\M`;
- recibe parametros, sin interpolacion insegura.

### Helper

`db/romantic_queries.py` agrega:

```python
count_hater_word_occurrences(sender_name: str) -> int
```

### Servicio

`services/romantic_metrics.py` agrega `hater_full_time` al payload y lo inserta como card pequena en `summary_cards`.

La ubicacion elegida es `Pequeños datos bonitos` porque la grilla tenia espacio para una card pequena adicional y no requiere cambiar el layout general.

## Validacion

```powershell
.\venv\Scripts\python.exe -m pytest tests/test_romantic_metrics.py tests/test_romantic_queries.py
```
