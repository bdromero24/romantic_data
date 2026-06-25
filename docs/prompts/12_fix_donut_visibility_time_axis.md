# Prompt para Codex: mejorar visibilidad del chart donut y corregir eje X de la serie mensual

## Contexto

Estoy trabajando en una landing romántica hecha con Python + Streamlit. Los gráficos están en el script `charts.py` y usan Altair. La app debe mantener el diseño visual actual: fondo rosa/blanco, paleta fucsia, cards redondeadas, estilo romántico premium y reveal-on-scroll.

Ya existe un gráfico donut/pie para mostrar cuántos mensajes escribió cada persona. El problema actual es visual: la leyenda y/o textos del donut se ven demasiado claros sobre el fondo rosa, casi ilegibles.

También existe una serie de tiempo mensual titulada aproximadamente:

```text
Como fue creciendo nuestra historia mes a mes
```

El problema actual de la serie mensual es que el eje X repite varias veces el mismo mes, por ejemplo:

```text
10/2025 10/2025 11/2025 11/2025 11/2025 12/2025 ...
```

Necesito que el eje X muestre cada mes una sola vez.

---

## Objetivo

Modificar únicamente lo necesario en `charts.py` para:

1. Mejorar la legibilidad del gráfico donut de mensajes por persona.
2. Hacer que los labels, leyenda y porcentajes del donut sean visibles sobre el fondo rosa.
3. Corregir la serie de tiempo mensual para que el eje X no repita el mismo mes varias veces.
4. Mantener la paleta romántica actual y el estilo visual existente.
5. No rediseñar toda la landing.
6. No cambiar el orden general de secciones.
7. No tocar contenido romántico, textos configurables, timeline ni mensajes destacados.

---

## Archivos a revisar

Revisar principalmente:

```text
charts.py
```

Si la agregación mensual se hace fuera de `charts.py`, revisar también el archivo donde se construye el diccionario `rhythm`, probablemente en algún módulo de queries o helpers de datos, por ejemplo:

```text
db/queries.py
page/main.py
app/dashboard.py
```

No asumir rutas exactas sin verificar el proyecto.

---

## Requisitos para el gráfico donut

El gráfico donut actual debe seguir usando la misma lógica, pero mejorar la visibilidad.

### Problemas a corregir

- La leyenda se ve blanca o demasiado clara.
- Los nombres de personas no tienen contraste suficiente.
- Los porcentajes pueden perderse sobre las porciones rosadas.
- El gráfico debe verse bien sobre fondo rosa claro.

### Cambios esperados

En la función que construye el donut, por ejemplo `_build_sender_pie_chart(...)`, ajustar:

1. Color de texto de leyenda a un tono oscuro de la paleta:

```python
ROMANTIC_COLORS["text"]
```

o, si hace falta más contraste:

```python
ROMANTIC_COLORS["fuchsia_deep"]
```

2. Peso de fuente de la leyenda:

```python
labelFontWeight="bold"
```

3. Tamaño de fuente de la leyenda:

```python
labelFontSize=14
```

4. Color de porcentaje dentro del donut:

```python
color=ROMANTIC_COLORS["text"]
```

5. Peso del porcentaje:

```python
fontWeight="bold"
```

6. Si el porcentaje aún se pierde visualmente, usar una capa de texto con fondo o desplazar el label fuera del arco con `radius` mayor.

7. Mantener tooltip con:

- nombre/persona;
- cantidad de mensajes;
- porcentaje.

Ejemplo esperado del tooltip:

```text
Persona: David
Mensajes: 12,345
Porcentaje: 56.7%
```

8. Mantener la paleta actual:

```python
ROMANTIC_SCALE
ROMANTIC_COLORS
```

9. No usar colores ajenos a la identidad visual, salvo tonos oscuros ya definidos en la paleta.

---

## Implementación sugerida para la leyenda del donut

Usar una configuración similar a esta en `alt.Legend`:

```python
legend=alt.Legend(
    title=None,
    orient="bottom",
    labelColor=ROMANTIC_COLORS["text"],
    labelFont="Nunito, Inter, system-ui, sans-serif",
    labelFontSize=14,
    labelFontWeight="bold",
    symbolSize=140,
    symbolStrokeColor=ROMANTIC_COLORS["text"],
    symbolStrokeWidth=1,
)
```

Si `symbolStrokeColor` o `symbolStrokeWidth` genera incompatibilidad con la versión instalada de Altair, omitir esos argumentos y dejar documentado en comentario.

---

## Implementación sugerida para porcentajes visibles

Usar una capa `mark_text` más legible:

```python
percentage_labels = base.mark_text(
    radius=96,
    font="Nunito, Inter, system-ui, sans-serif",
    fontSize=16,
    fontWeight="bold",
    color=ROMANTIC_COLORS["text"],
).encode(
    text=alt.Text("percentage:Q", format=".1%"),
    tooltip=[
        alt.Tooltip("label:N", title="Persona"),
        alt.Tooltip("value:Q", title="Mensajes", format=","),
        alt.Tooltip("percentage:Q", title="Porcentaje", format=".1%"),
    ],
)
```

Si se ve mejor fuera del donut, aumentar `radius` a `130` o `140` y ajustar `outerRadius`.

---

## Requisitos para la serie mensual

La función de serie de tiempo, probablemente `_build_time_series_chart(...)`, debe corregir el eje X para que cada mes aparezca una sola vez.

### Problema actual

El eje X muestra el mismo mes varias veces porque Altair está renderizando múltiples ticks automáticos para fechas dentro del mismo mes o porque los datos contienen varias fechas dentro del mismo periodo mensual.

### Resultado esperado

El eje X debe mostrar una sola etiqueta por mes, por ejemplo:

```text
10/2025  11/2025  12/2025  01/2026  02/2026  03/2026  04/2026
```

No debe mostrar:

```text
10/2025 10/2025 11/2025 11/2025 11/2025
```

---

## Corrección esperada de la serie de tiempo

En `_build_time_series_chart(rows)`, normalizar la fecha a nivel mensual antes de graficar.

La idea es:

1. Convertir `date` a datetime.
2. Eliminar fechas inválidas.
3. Aplicar `CHARTS_MAX_DATE` si existe.
4. Crear una columna mensual única.
5. Agrupar por mes.
6. Sumar `value` por mes.
7. Crear un label visible `MM/YYYY`.
8. Usar ese label como eje X nominal/ordinal para evitar ticks duplicados.
9. Mantener orden cronológico real.

Implementación sugerida:

```python
def _build_time_series_chart(rows: list[dict[str, Any]]) -> alt.Chart:
    data = pd.DataFrame(rows).copy()

    data["date"] = pd.to_datetime(data["date"], errors="coerce")
    data = data.dropna(subset=["date"])

    if CHARTS_MAX_DATE is not None:
        max_date = pd.to_datetime(CHARTS_MAX_DATE)
        data = data[data["date"] <= max_date]

    data["month"] = data["date"].dt.to_period("M").dt.to_timestamp()

    data = (
        data.groupby("month", as_index=False)["value"]
        .sum()
        .sort_values("month")
    )

    data["month_label"] = data["month"].dt.strftime("%m/%Y")

    chart = (
        alt.Chart(data)
        .mark_line(point=True, color=ROMANTIC_COLORS["fuchsia"], strokeWidth=4)
        .encode(
            x=alt.X(
                "month_label:N",
                title=None,
                sort=list(data["month_label"]),
                axis=alt.Axis(labelAngle=0),
            ),
            y=alt.Y("value:Q", title=None),
            tooltip=[
                alt.Tooltip("month_label:N", title="Mes"),
                alt.Tooltip("value:Q", title="Mensajes", format=","),
            ],
        )
        .properties(height=280)
    )

    return apply_altair_romantic_theme(chart)
```

Si prefieres mantener eje temporal real, también puedes usar `yearmonth(date)` y configurar el eje con ticks mensuales, pero la solución nominal con `month_label` es aceptable porque evita duplicados y mantiene orden cronológico.

---

## Mantener cutoff hardcodeado

Verificar que siga existiendo arriba del archivo:

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

No mover esta constante a configuración externa. Por ahora debe quedar hardcodeada en `charts.py`.

---

## Validaciones

Después de los cambios, validar:

1. La app corre sin errores:

```bash
streamlit run app/main.py
```

o el entrypoint real del proyecto.

2. El gráfico donut muestra nombres legibles.
3. La leyenda del donut se ve clara sobre el fondo rosa.
4. Los porcentajes del donut se ven en bold y con buen contraste.
5. El tooltip del donut muestra nombre, cantidad de mensajes y porcentaje.
6. La serie mensual no repite etiquetas del mismo mes en el eje X.
7. La serie mensual sigue respetando `CHARTS_MAX_DATE`.
8. No se rompe la paleta romántica ni el diseño actual.
9. No se modifican secciones no relacionadas.

---

## Restricciones

- No hacer rediseño general.
- No tocar el contenido romántico.
- No tocar `content_config.py` salvo que sea estrictamente necesario, y en principio no debería serlo.
- No cambiar textos de otras secciones.
- No eliminar reveal-on-scroll.
- No exponer errores técnicos en UI.
- No usar tablas crudas para reemplazar el gráfico.
- No usar SQL concatenado con f-strings si se toca alguna query.
- Mantener funciones modulares.

---

## Resultado esperado

El resultado debe ser un cambio puntual donde:

- el donut “Cuanto escribio cada uno” se vea correctamente;
- los nombres y porcentajes tengan contraste suficiente;
- el tooltip mantenga cantidad de mensajes y persona;
- el gráfico mensual muestre cada mes una sola vez en el eje X;
- el cutoff `CHARTS_MAX_DATE` siga funcionando.
