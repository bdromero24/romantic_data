# Prompt para Codex: cutoff de fecha, arreglo de serie mensual y gráfico circular por persona

## Contexto

El proyecto es una landing romántica en Streamlit. Los gráficos se renderizan en `charts.py` usando Altair y una paleta rosa/fucsia ya definida en `ROMANTIC_COLORS` y `ROMANTIC_SCALE`.

Actualmente existe un gráfico de línea mensual titulado aproximadamente:

```text
Como fue creciendo nuestra historia mes a mes
```

Ese gráfico está mostrando algunos puntos con fechas incorrectas. Quiero poder truncar la serie mensual usando una fecha máxima hardcodeada en el código.

También quiero agregar un gráfico circular/donut que muestre cuántos mensajes envió cada persona.

## Objetivo

Implementar tres cambios:

1. Agregar una constante hardcodeada `CHARTS_MAX_DATE` en `charts.py` para truncar gráficos basados en tiempo.
2. Corregir la construcción del gráfico mensual para que convierta fechas correctamente, descarte fechas inválidas y filtre todo lo posterior a `CHARTS_MAX_DATE`.
3. Crear la query y la lógica de datos necesaria para contar mensajes por persona y alimentar un nuevo gráfico circular/donut.

---

## 1. Agregar constante de fecha máxima en `charts.py`

En `charts.py`, cerca de la definición de `ROMANTIC_COLORS`, agregar exactamente esta constante y comentarios:

```python
# Fecha maxima visible en graficos basados en tiempo.
# Cambiala manualmente cuando quieras truncar la serie mensual.
#
# Ejemplos validos:
# CHARTS_MAX_DATE = "2026-05-31"
# CHARTS_MAX_DATE = "2026-04-30"
# CHARTS_MAX_DATE = None  # desactiva el truncamiento
CHARTS_MAX_DATE: str | None = "2026-05-31"
```

Reglas:

- Si `CHARTS_MAX_DATE` es `None`, no filtrar la serie.
- Si tiene una fecha string, filtrar todo dato posterior a esa fecha.
- No mover esta configuración a variables de entorno.
- Debe quedar editable manualmente en código.

---

## 2. Arreglar la serie mensual

En `charts.py`, localizar la función que construye el gráfico mensual, probablemente `_build_time_series_chart(rows)`.

Modificarla para que:

- Cree un `DataFrame` defensivo con `.copy()`.
- Convierta la columna `date` usando:

```python
data["date"] = pd.to_datetime(data["date"], errors="coerce")
```

- Elimine filas con fechas inválidas:

```python
data = data.dropna(subset=["date"])
```

- Aplique el filtro por `CHARTS_MAX_DATE`:

```python
if CHARTS_MAX_DATE is not None:
    max_date = pd.to_datetime(CHARTS_MAX_DATE)
    data = data[data["date"] <= max_date]
```

- Ordene por fecha:

```python
data = data.sort_values("date")
```

- Mantenga el diseño actual:
  - línea fucsia;
  - puntos visibles;
  - mismo `ROMANTIC_COLORS`;
  - mismo `apply_altair_romantic_theme`;
  - altura similar;
  - tooltips con mes y mensajes.

No cambiar el diseño general de la landing.

---

## 3. Crear query para contar mensajes por persona

Buscar el archivo donde están las queries o helpers que construyen el diccionario `rhythm`. Puede estar en alguno de estos lugares:

```text
db/queries.py
page/main.py
app/dashboard.py
analysis/metrics.py
```

Agregar una función nueva para contar mensajes por persona.

### Query SQL esperada

La query debe ser parametrizada y debe devolver esta estructura lógica:

```sql
SELECT
    sender AS label,
    COUNT(*) AS value
FROM messages
WHERE sender IS NOT NULL
  AND TRIM(sender) <> ''
  AND (:max_date IS NULL OR timestamp <= :max_date)
GROUP BY sender
ORDER BY value DESC;
```

### Requisitos de seguridad

- No usar f-strings para construir SQL con valores externos.
- Usar parámetros.
- Si el proyecto usa SQLAlchemy, usar `text()`.
- Si el proyecto usa psycopg o cursor directo, usar placeholders compatibles con ese driver.
- No exponer errores técnicos en UI.

### Ejemplo con SQLAlchemy

Adaptar al estilo real del proyecto:

```python
from sqlalchemy import text


def count_messages_by_sender_until(engine, max_date: str | None = None) -> list[dict]:
    query = text(
        """
        SELECT
            sender AS label,
            COUNT(*) AS value
        FROM messages
        WHERE sender IS NOT NULL
          AND TRIM(sender) <> ''
          AND (:max_date IS NULL OR timestamp <= :max_date)
        GROUP BY sender
        ORDER BY value DESC
        """
    )

    with engine.connect() as connection:
        rows = connection.execute(query, {"max_date": max_date}).mappings().all()

    return [dict(row) for row in rows]
```

Si ya existe una función central que arma `rhythm`, integrarla ahí.

El resultado final debe incluir:

```python
rhythm = {
    "hours": hours_rows,
    "weekdays": weekdays_rows,
    "months": months_rows,
    "senders": sender_rows,
}
```

La clave nueva debe llamarse:

```python
"senders"
```

Y cada fila debe tener esta forma:

```python
{"label": "Nombre", "value": 1234}
```

---

## 4. Agregar gráfico circular/donut en `charts.py`

En `charts.py`, agregar soporte para un nuevo `chart_type="pie"`.

Modificar `_render_chart_card(...)` para que pueda hacer:

```python
if chart_type == "time_series":
    chart = _build_time_series_chart(rows)
elif chart_type == "pie":
    chart = _build_sender_pie_chart(rows)
else:
    chart = _build_bar_chart(rows)
```

Agregar una función nueva:

```python
def _build_sender_pie_chart(rows: list[dict[str, Any]]) -> alt.LayerChart:
    ...
```

### Requisitos del gráfico circular

El gráfico debe:

- Ser donut, no pie sólido.
- Usar la misma paleta `ROMANTIC_SCALE`.
- Mostrar el porcentaje en el gráfico con texto en bold.
- Mostrar en tooltip:
  - nombre/persona;
  - cantidad de mensajes;
  - porcentaje.
- Respetar `apply_altair_romantic_theme`.
- No usar Plotly si el resto de gráficos está en Altair.
- No introducir CSS adicional salvo que sea imprescindible.

### Estructura de datos esperada

Debe aceptar esta estructura:

```python
[
    {"label": "Persona 1", "value": 1200},
    {"label": "Persona 2", "value": 980},
]
```

Opcionalmente, hacerlo tolerante a:

```python
[
    {"sender": "Persona 1", "total_messages": 1200},
    {"sender": "Persona 2", "total_messages": 980},
]
```

En ese caso renombrar columnas internamente:

```python
if "sender" in data.columns and "label" not in data.columns:
    data = data.rename(columns={"sender": "label"})

if "total_messages" in data.columns and "value" not in data.columns:
    data = data.rename(columns={"total_messages": "value"})
```

### Implementación sugerida

```python
def _build_sender_pie_chart(rows: list[dict[str, Any]]) -> alt.LayerChart:
    data = pd.DataFrame(rows).copy()

    if "sender" in data.columns and "label" not in data.columns:
        data = data.rename(columns={"sender": "label"})

    if "total_messages" in data.columns and "value" not in data.columns:
        data = data.rename(columns={"total_messages": "value"})

    data = data[["label", "value"]].dropna()
    data["value"] = pd.to_numeric(data["value"], errors="coerce")
    data = data.dropna(subset=["value"])
    data = data[data["value"] > 0]

    total_messages = data["value"].sum()
    data["percentage"] = data["value"] / total_messages

    base = alt.Chart(data).encode(
        theta=alt.Theta("value:Q", stack=True),
        color=alt.Color(
            "label:N",
            scale=ROMANTIC_SCALE,
            legend=alt.Legend(title=None, orient="bottom"),
        ),
        tooltip=[
            alt.Tooltip("label:N", title="Persona"),
            alt.Tooltip("value:Q", title="Mensajes", format=","),
            alt.Tooltip("percentage:Q", title="Porcentaje", format=".1%"),
        ],
    )

    pie = base.mark_arc(
        innerRadius=58,
        outerRadius=120,
        cornerRadius=5,
        stroke=ROMANTIC_COLORS["bg"],
        strokeWidth=3,
    )

    percentage_labels = base.mark_text(
        radius=92,
        font="Nunito, Inter, system-ui, sans-serif",
        fontSize=15,
        fontWeight="bold",
        color=ROMANTIC_COLORS["text"],
    ).encode(
        text=alt.Text("percentage:Q", format=".1%"),
    )

    chart = (pie + percentage_labels).properties(height=310)

    return apply_altair_romantic_theme(chart)
```

Agregar control defensivo para evitar división por cero si no hay mensajes válidos.

---

## 5. Renderizar el nuevo gráfico en la sección de ritmo

En `render_rhythm_charts(...)`, después del gráfico mensual o dentro de la sección de ritmo, agregar:

```python
_render_chart_card(
    title="Cuanto escribio cada uno",
    rows=rhythm.get("senders", []),
    chart_type="pie",
    reveal_delay=90,
)
```

No cambiar el orden general de la landing. Solo agregar el nuevo gráfico dentro de la sección actual de gráficos.

---

## 6. Usar el mismo cutoff en query y gráfico

El cutoff debe aplicarse en dos niveles:

1. En el gráfico mensual, para evitar que Altair muestre fechas posteriores.
2. En la query de mensajes por persona, para que el donut no cuente mensajes posteriores a la fecha máxima.

Si el módulo que construye `rhythm` puede importar `CHARTS_MAX_DATE` sin generar ciclos de importación, usarlo.

Si importar desde `charts.py` genera ciclo, crear la constante en un módulo de configuración compartida, por ejemplo:

```text
page/chart_config.py
```

con:

```python
CHARTS_MAX_DATE: str | None = "2026-05-31"
```

Y luego importarla desde `charts.py` y desde el módulo de queries/datos.

Preferencia:

- Si no hay ciclo de importación, dejar la constante en `charts.py`.
- Si hay ciclo de importación, crear `chart_config.py`.

---

## 7. Validación esperada

Después del cambio:

- El gráfico mensual no debe mostrar puntos posteriores a `CHARTS_MAX_DATE`.
- Fechas inválidas deben descartarse y no romper el render.
- El gráfico circular debe aparecer en la sección de ritmo.
- El gráfico circular debe mostrar porcentajes en bold.
- El tooltip del gráfico circular debe mostrar persona, mensajes y porcentaje.
- La query debe contar mensajes por `sender`.
- La query debe respetar el mismo cutoff de fecha.
- La app no debe mostrar tracebacks en UI.
- No modificar el diseño general de la landing.

---

## 8. Archivos probables a modificar

Modificar solo los necesarios:

```text
charts.py
```

Y uno de estos, según dónde esté la lógica de datos:

```text
db/queries.py
page/main.py
app/dashboard.py
analysis/metrics.py
```

Si hace falta evitar ciclos de importación, crear:

```text
page/chart_config.py
```

---

## Output esperado

Aplicar los cambios directamente en el código.

No cambiar textos generales ni diseño visual de la landing fuera de los gráficos solicitados.