# Prompt para Codex — tipografía de subtítulos + reordenar “Pequeños datos bonitos” + promedio diario

Necesito hacer ajustes puntuales en la landing romántica, manteniendo el diseño general intacto.

## Objetivo

Implementar dos cambios:

1. Corregir la tipografía de los subtítulos internos del bloque especial:
   - `Cosas bonitas que ella me dijo`
   - `Una conversación que quiero recordar`
2. Reordenar la sección **“Pequeños datos bonitos”** y agregar un nuevo KPI con el promedio total de mensajes diarios.

---

## 1. Tipografía de subtítulos del bloque especial

### Subtítulos a corregir

- `Cosas bonitas que ella me dijo`
- `Una conversación que quiero recordar`

### Requerimiento exacto

Estos subtítulos deben usar:

- la misma fuente que el título decorativo principal del bloque especial;
- tamaño exactamente **2 px menor** que ese título de referencia;
- estilo coherente con la landing;
- buena legibilidad.

El título de referencia es el título visual decorativo del bloque especial:

```text
Un mensaje que quiero guardar
```

Si ese título usa una fuente script/cursiva/decorativa, reutilizar esa misma familia tipográfica en los subtítulos internos.

### Restricciones

- No cambiar el copy de los subtítulos.
- No cambiar IDs de mensajes.
- No modificar el bloque de mensajes ni la conversación.
- No romper el layout del bloque especial.
- No aplicar esta fuente a textos donde no corresponda.

---

## 2. Reordenar “Pequeños datos bonitos”

### Objetivo visual

Reordenar la sección:

```text
Pequeños datos bonitos
```

La lectura debe ser clara de izquierda a derecha. Los elementos más importantes deben captarse primero.

### Regla de layout

Los contenedores/cards más grandes o importantes deben ir a la izquierda.
Los recuadros/contenedores más pequeños o secundarios deben ir a la derecha.

### Cards grandes/importantes a priorizar a la izquierda

Estos elementos deben quedar visualmente priorizados a la izquierda:

- `Mensajes compartidos`
- `Primer te amo`
- `Mes más intenso`

Si el layout usa grid, bento grid, columnas, spans o clases CSS específicas, reorganizarlo para que estos tres elementos sean los primeros y más prominentes visualmente.

### Cards pequeñas/secundarias a la derecha

Los contenedores más pequeños deben quedar a la derecha o en la zona secundaria del grid, sin romper responsive.

### Requisitos responsive

- En desktop: priorizar layout izquierda/derecha.
- En mobile/tablet: mantener orden lógico, evitando overflow horizontal.
- No romper el scroll ni la composición general.

---

## 3. Nuevo KPI: promedio total de mensajes diarios

### Requerimiento funcional

Agregar un nuevo contenedor/card dentro de **“Pequeños datos bonitos”** con el promedio total de mensajes diarios.

El promedio debe considerar **ambos sender**.

### Definición del cálculo

Calcular:

```text
promedio diario = total de mensajes / número de días con conversación
```

O, preferiblemente:

1. agrupar mensajes por día calendario;
2. contar mensajes por día;
3. calcular el promedio de esos conteos diarios.

Usar la opción más consistente con la arquitectura actual del proyecto.

### Query sugerida

Si existe módulo de queries, agregar una query parametrizada o helper equivalente:

```sql
WITH daily_messages AS (
    SELECT
        DATE(timestamp) AS conversation_day,
        COUNT(*) AS total_messages
    FROM messages
    WHERE timestamp IS NOT NULL
    GROUP BY DATE(timestamp)
)
SELECT AVG(total_messages)::numeric AS avg_daily_messages
FROM daily_messages;
```

Ajustar nombres de tabla/columna si el proyecto usa otros nombres.

### UI del nuevo KPI

El nuevo KPI debe:

- verse como parte natural de “Pequeños datos bonitos”;
- tener copy romántico o amable;
- mostrar el valor redondeado de forma legible;
- mantener paleta y tipografía actual.

Ejemplo de copy posible:

```text
Promedio diario
X mensajes al día entre los dos
```

Puedes ajustar el texto si existe una convención de copy en la sección.

---

## 4. Arreglar fondo corazon 8-bit
El elemento renderizado en los contenedores del primer te amo, el corazon 8-bit, no debe tener fondo, debe ser transparente el fondo, solo renderizar la forma y color, asi como se hace con la fresa, no es mas.

## Restricciones generales

- No tocar ETL salvo que sea estrictamente necesario.
- No modificar gráficos.
- No modificar hero.
- No modificar sección de frases bonitas.
- No modificar bloque de pergaminos ni assets en este cambio.
- No cambiar datos manuales configurados por ID.
- No usar SQL inseguro.
- No exponer errores técnicos en UI.
- Mantener separación entre queries/backend, agregación de datos y frontend.

---

## Documentación requerida

Actualizar documentación o debug/changelog del proyecto indicando:

1. qué archivo controla la tipografía de los subtítulos internos;
2. qué clase CSS fue modificada o creada;
3. qué archivo controla el layout de “Pequeños datos bonitos”;
4. qué query/helper calcula el promedio diario;
5. dónde se renderiza el nuevo KPI;
6. cómo verificar visualmente el cambio.

---

## Entregable

Devuélveme:

1. archivos modificados;
2. código completo por archivo;
3. explicación breve de qué cambió;
4. sin rediseñar toda la landing.
