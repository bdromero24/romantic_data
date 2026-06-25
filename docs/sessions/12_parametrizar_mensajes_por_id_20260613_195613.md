# Sesion 12: parametrizar mensajes por ID

## Fecha

```text
2026-06-13 19:56:13
```

## Objetivo

Parametrizar por ID las secciones:

- `Un mensaje que quiero guardar`
- `Mensajes para volver a leer despacio`

sin hacer cambios visuales generales.

## Archivos modificados

- `app/content_config.py`
- `db/queries.py`
- `db/romantic_queries.py`
- `services/romantic_metrics.py`
- `ui/components.py`
- `tests/test_romantic_metrics.py`
- `tests/test_romantic_queries.py`
- `tests/test_ui_components.py`
- `docs/content_configuration.md`
- `docs/codex_session_debug.md`
- `docs/sessions/12_parametrizar_mensajes_por_id_20260613_195613.md`

## Cambios aplicados

### Configuracion

`ROMANTIC_CONTENT["special_message"]` ahora soporta:

```python
"blocks": [
    {
        "type": "her_messages",
        "title": "Cosas bonitas que ella me dijo",
        "message_ids": [],
    },
    {
        "type": "conversation_pair",
        "title": "Una conversacion que quiero recordar",
        "messages": [
            {"role": "me", "message_id": None},
            {"role": "her", "message_id": None},
        ],
    },
]
```

Se mantiene `special_message["message_id"]` como fallback si no hay bloques validos.

### Consultas

Se agrego `ROMANTIC_MESSAGES_BY_IDS_QUERY` en `db/queries.py`.

Se agrego `fetch_messages_by_ids(message_ids: list[int])` en `db/romantic_queries.py`.

El helper:

- ignora `None`;
- retorna lista vacia si no hay IDs;
- usa SQL parametrizado;
- reordena en Python para respetar el orden configurado.

### Servicio

`services/romantic_metrics.py` ahora construye:

- bloques `her_messages`;
- bloques `conversation_pair`;
- frases bonitas manuales con `featured_quotes["message_ids"]`;
- fallback automatico excluyendo IDs reservados.

### Render

`ui/components.py` renderiza bloques configurados con las clases existentes:

- `ig-bubble-her`
- `ig-bubble-me`
- `ig-message-list`

Los mensajes de base de datos siguen escapandose antes de enviarse a `st.markdown(..., unsafe_allow_html=True)`.

### Documentacion

`docs/content_configuration.md` explica:

- donde editar los IDs;
- como configurar varios mensajes de ella;
- como configurar una conversacion;
- como configurar frases bonitas;
- que pasa con `None` y listas vacias;
- como se evitan duplicados;
- reglas de seguridad HTML.

`docs/codex_session_debug.md` registra el ajuste.

## Validacion

```powershell
.\venv\Scripts\python.exe -m pytest tests/test_romantic_metrics.py tests/test_ui_components.py tests/test_romantic_queries.py tests/test_streamlit_entrypoint.py
```

Resultado:

```text
16 passed
```
