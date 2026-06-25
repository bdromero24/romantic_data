# Prompt para Codex — corregir inconsistencia de fechas YYYY-MM-DD vs YYYY-DD-MM

Necesito corregir un problema crítico de fechas en el proyecto.

## Contexto

La aplicación ya está prácticamente lista, pero detecté que hay fechas insertadas incorrectamente en la base de datos.

Ejemplo de fecha incorrecta:

```text
2026-12-06 11:30:00.000 -0500
2026-08-06 21:45:00.000 -0500
```

Esa fecha debería ser:

```text
2026-06-12 11:30:00.000 -0500
2026-06-08 21:45:00.000 -0500
```

El problema parece ser una inconsistencia entre formatos y como ves hay fechas del futuro, de diciembre o agosto cuando eso no ha sucedido:

```text
YYYY-MM-DD
YYYY-DD-MM
```

EL formato de whatsapp original es <4/18/26, 21:25> <MM/DD/YY, HH:MM> 
El formato de instagram original es "timestamp_ms": 1782103283941, ese formato se debe descifrar de mejor manera, porque estoy identificando que la fuente con problemas de timestamp es instagram.

Esto está afectando la lógica de la landing. Por ejemplo, el sistema está detectando el primer “te amo” como `02/05`, es decir, 5 de febrero, cuando probablemente debería interpretarse distinto según el origen real del mensaje, pues en febrero recien empecé a conocerla y el primer te amo es del '2026-04-23 23:13:00.000 -0500', fecha que si se inserto correctamente (es de whatsapp).

Necesito que todo el proyecto use **un solo formato consistente de fechas**.

---

## Objetivo

Corregir el parsing, transformación e inserción de timestamps para que todas las fechas se interpreten y almacenen de forma consistente como:

```text
YYYY-MM-DD HH:MM:SS timezone
```

Es decir:

```text
2026-06-12 11:30:00.000 -0500
```

no:

```text
2026-12-06 11:30:00.000 -0500
```

---

## Alcance

Revisar y corregir todo lo necesario en:

- extracción de WhatsApp;
- extracción de Instagram;
- transformación de mensajes;
- normalización de timestamps;
- carga a PostgreSQL;
- queries dependientes de fecha;
- tests existentes o nuevos;
- documentación técnica de la corrección.

Prioridad principal: **corregir el origen del problema en el ETL**, no solo maquillar el frontend.

---

## Requisitos técnicos

### 1. Identificar dónde se parsean las fechas

Buscar en el proyecto funciones relacionadas con:

```text
parse_date
parse_timestamp
timestamp
datetime
pd.to_datetime
strptime
dateutil
WhatsApp
Instagram
```

Determinar dónde se está interpretando mal el día y el mes.

---

### 2. Diferenciar origen WhatsApp vs Instagram

Validar si los formatos de fecha vienen de fuentes distintas:

- WhatsApp `.txt` exportado;
- Instagram JSON;
- staging parquet;
- registros ya transformados.

No asumir que todas las fuentes tienen el mismo formato si no es cierto.

---

### 3. Corregir parsing de WhatsApp e instagram

Si WhatsApp exporta fechas tipo:

```text
6/12/26, 11:30 AM
```

entonces debe interpretarse explícitamente según el formato real del archivo.

No usar parsing ambiguo si puede confundir día y mes.

Preferir formatos explícitos como:

```python
datetime.strptime(raw_date, "%m/%d/%y, %I:%M %p")
```

o el formato que corresponda realmente al archivo.

Si el archivo usa día/mes/año, usar explícitamente:

```python
datetime.strptime(raw_date, "%d/%m/%y, %I:%M %p")
```

La solución debe basarse en el formato real detectado en los archivos fuente.

---

### 4. Evitar inferencia ambigua

Evitar soluciones frágiles como:

```python
pd.to_datetime(value)
```

sin parámetros claros.

Si se usa `pd.to_datetime`, debe usarse con `format=...` o `dayfirst=...` de forma explícita y documentada.

---

### 5. Estandarizar salida transformada

Después de transformar, todos los registros deben tener `timestamp` como un datetime válido, consistente y comparable.

La salida debe representar fechas en formato ISO lógico:

```text
YYYY-MM-DD HH:MM:SS
```

Si se maneja timezone `-0500`, conservarlo de forma consistente o normalizarlo según la arquitectura actual.

No mezclar naive datetime con timezone-aware datetime sin intención explícita.

---

### 6. Validar registros existentes

Agregar una validación o script de diagnóstico para detectar posibles fechas sospechosas ya cargadas.

Ejemplos de validaciones útiles:

- listar fechas futuras inesperadas;
- listar meses con actividad anormal;
- detectar casos donde `day <= 12` y `month <= 12` que podrían ser ambiguos;
- comparar conteos mensuales antes y después de la corrección si aplica.

No modificar datos en producción sin dejar claro el procedimiento.

---

## Tests obligatorios

Crear o actualizar tests para probar que el parsing de fechas funciona correctamente.

Incluir al menos estos casos:

### Caso 1
Entrada que representa 12 de junio de 2026:

```text
6/12/26, 11:30 AM
```

Salida esperada si el formato del archivo es mes/día/año:

```text
2026-06-12 11:30:00
```

### Caso 2
Entrada que representa 5 de febrero de 2026:

```text
2/5/26
```

Debe interpretarse de acuerdo con el formato real del archivo, y el test debe dejar explícito si es:

```text
2026-02-05
```

o:

```text
2026-05-02
```

### Caso 3
Una fecha no ambigua:

```text
12/25/26
```

Debe quedar claro que no se invierte incorrectamente.

### Caso 4
Instagram JSON si aplica, usando el formato real que trae Instagram.

---

## Prueba de consistencia requerida

Necesito que el resultado demuestre que hay **un solo formato efectivo** en el pipeline.

Agregar un test o script que verifique:

1. los timestamps transformados son datetime válidos;
2. no quedan timestamps como strings ambiguos;
3. las fechas se ordenan correctamente;
4. los conteos mensuales no aparecen duplicados por inversión día/mes;
5. el primer “te amo” se calcula sobre fechas corregidas.

---

## Reprocesamiento

Si el error está en datos ya cargados, indicar claramente qué debo hacer:

- limpiar tabla `messages`;
- borrar staging corrupto si aplica;
- volver a correr ETL;
- recargar PostgreSQL;
- volver a validar.

No ejecutes acciones destructivas sin dejarlo explícito.

Si propones SQL para limpiar, que sea claro y seguro.

---

## Documentación requerida

Actualizar o crear documentación breve en:

```text
docs/codex_session_debug.md
```

o archivo equivalente, con una sección:

```text
Corrección de parsing de fechas en ETL
```

Debe explicar:

- cuál era el problema;
- qué archivo o función lo causaba;
- qué formato se definió como fuente de verdad;
- qué cambio se hizo;
- cómo probar que quedó corregido;
- cómo reprocesar datos ya cargados.

También documentar en qué script se hizo el cambio.

---

## Restricciones

- No cambiar el diseño visual de la landing.
- No modificar textos románticos ni configuración de contenido.
- No tocar gráficos salvo que sea estrictamente necesario para confirmar la corrección.
- No ocultar el problema con filtros de frontend.
- No usar parsing ambiguo.
- No usar SQL inseguro.
- No eliminar datos sin advertencia clara.

---

## Resultado esperado

Al finalizar:

1. las fechas deben parsearse de forma consistente;
2. `2026-06-12` no debe convertirse en `2026-12-06`;
3. el cálculo de primer “te amo” debe depender de timestamps corregidos;
4. los gráficos mensuales deben reflejar meses correctos;
5. debe existir una prueba automatizada o script de validación que demuestre que ya no hay mezcla de formatos;
6. debe quedar documentado qué se cambió y dónde.

---

## Formato de respuesta para Codex

Devuélveme:

1. archivos modificados;
2. código completo por archivo;
3. tests agregados/modificados;
4. comandos para correr tests;
5. comandos para reprocesar datos si aplica;
6. explicación breve, concreta y técnica del cambio.
