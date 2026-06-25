# Prompt 01 - Logica de negocio para landing page romantica basada en datos

## Rol

Actua como arquitecto de software Python, data engineer y product designer orientado a storytelling romantico basado en datos.

Tengo una aplicacion en Python que procesa conversaciones de WhatsApp e Instagram mediante un pipeline ETL con PostgreSQL. El backend ya extrae, transforma, normaliza y carga mensajes. Tambien puede existir NLP o analisis adicional, pero la interfaz actual se siente demasiado tecnica.

El objetivo no es construir un dashboard analitico para usuarios tecnicos. El objetivo es construir una landing page romantica para mi novia, usando nuestros mensajes como fuente de recuerdos, datos bonitos e historia compartida.

## Objetivo de esta sesion

Refactorizar la logica de negocio visible de la app para que los datos se presenten como una historia romantica, no como analisis tecnico.

Esta sesion se enfoca en:

- Que metricas mostrar.
- Que consultas o funciones crear.
- Que lenguaje usar en la interfaz.
- Que elementos tecnicos ocultar.
- Como separar backend, NLP y frontend.
- Como convertir datos en storytelling emocional.

No te enfoques aun en CSS detallado, glassmorphism, bento grid ni estilos visuales avanzados. Eso se resolvera en otro prompt.

## Principios de producto

La app debe sentirse como:

- Una pagina romantica personalizada.
- Una capsula de recuerdos.
- Una historia interactiva.
- Un regalo digital.
- Una experiencia emocional basada en datos.

La app no debe sentirse como:

- Dashboard BI.
- Panel empresarial.
- Notebook tecnico.
- Sistema de auditoria.
- Reporte de NLP.
- Dashboard de sentimiento.

## Separacion de responsabilidades

Mantener claramente separadas estas capas:

```text
ETL / backend
  - extract
  - transform
  - load
  - normalizacion
  - limpieza de datos
  - PostgreSQL

Queries / metricas romanticas
  - consultas SQL
  - funciones agregadas
  - conteos de frases
  - fechas importantes
  - palabras romanticas
  - momentos destacados

Frontend / landing
  - storytelling
  - cards
  - timeline
  - copy romantico
  - visualizacion suave
  - experiencia para mi novia
```

## Regla sobre NLP

Evitar mostrar NLP como concepto dentro de la app.

Permitido:

- Usar NLP en backend si ya existe.
- Usar resultados de NLP para enriquecer datos.
- Usar palabras frecuentes si se presentan como parte de nuestra historia.

No permitido en la interfaz principal:

- sentiment analysis
- polarity
- subjectivity
- score
- positive sentiment
- negative sentiment
- NLP pipeline
- tokenization
- model output
- metricas tecnicas de clasificacion

Si una metrica viene de NLP, debe traducirse a lenguaje emocional.

Ejemplo incorrecto:

```text
Sentiment score promedio: 0.83
```

Ejemplo correcto:

```text
Nuestros mensajes estuvieron llenos de palabras bonitas.
```

## Metricas romanticas recomendadas

Crear o exponer funciones/queries para calcular metricas como:

### Resumen general

- Total de mensajes compartidos.
- Total de dias con conversacion.
- Fecha del primer mensaje registrado.
- Fecha del ultimo mensaje registrado.
- Mes con mas mensajes.
- Dia con mas mensajes.
- Hora en la que mas hablamos.
- Persona que inicio mas conversaciones, si existe esa logica.

### Frases romanticas

Contar apariciones en `message_normalized` de patrones como:

- `te amo`
- `te adoro`
- `te extrano`
- `mi amor`
- `amor mio`
- `mi vida`
- `amor`
- `preciosa`
- `hermosa`
- `linda`
- `divina`
- `me haces feliz`.
- `odio`. 
- `hate`.

Importante: usar texto normalizado para contar y texto original para mostrar.

Ejemplo:

```sql
WHERE message_normalized ~* '\mte\s+amo+\M'
```

Para `te extraño`, consultar como:

```sql
WHERE message_normalized ~* '\mte\s+extrano+\M'
```

### Momentos importantes

Crear funciones para obtener:

- Primer mensaje registrado.
- Primer `te amo`.
- Primer `te extrano`.
- Primer `me haces feliz`.
- Dia con mas conversacion.
- Mes mas intenso.
- Frases romanticas memorables.

### Nuestro lenguaje

Crear metricas para:

- Palabras romanticas mas usadas.
- Expresiones unicas de la pareja.
- Frases recurrentes.

Evitar presentar esto como `word frequency` tecnica. Presentarlo como:

```text
Las palabras que mas nos representan
```

### Ritmo de conversacion

Crear datos para:

- Horas favoritas para hablar.
- Dias de la semana con mas mensajes.
- Meses con mas conversacion.
- Evolucion mensual de mensajes.

Presentarlo como narrativa:

```text
Nuestra hora favorita para hablar
```

En lugar de:

```text
Distribucion horaria de mensajes
```

## Secciones sugeridas para la landing

### 1. Hero

Debe mostrar:

- Titulo romantico.
- Subtitulo emocional.
- Rango temporal de la historia si esta disponible.
- Mensaje breve de bienvenida.

Ejemplo de copy:

```text
Nuestra historia, contada con mensajes, recuerdos y pequenos datos bonitos.
```

### 2. Nuestra historia en numeros

Mostrar cards con metricas simples:

- Mensajes compartidos.
- Dias hablando.
- Veces que dijimos te amo.
- Veces que dijimos te extrano.
- Mes mas especial.
- Hora favorita para hablar.

### 3. Momentos que marcaron nuestra historia

Mostrar una linea de tiempo con:

- Primer mensaje.
- Primer te amo.
- Dia mas conversado.
- Mes mas intenso.
- Frases especiales.

### 4. Palabras que nos representan

Mostrar palabras o expresiones romanticas frecuentes.

No mostrar tablas tecnicas por defecto.

### 5. Frases bonitas

Mostrar mensajes originales, no normalizados, en cards romanticas como: 
1- ¿Por qué eres tan lindo conmigo?.
2- Me siento muy amada mi vida
3- Me gusta que me abraces y que me des muchos besitos en la carita
4- Me gusta sentirme tranquila a tu lado y poder dormirme a tu lado
5- Me gusta estar contigo, te amo demasiado mi amor

Cada card puede incluir:

- Texto del mensaje.
- Fecha.
- Remitente.

### 6. Nuestro ritmo

Mostrar visualizaciones simples y esteticas sobre:

- Horas favoritas.
- Dias favoritos.
- Meses con mas mensajes.

No usar graficos complejos ni sobrecargar la pantalla.

### 7. Cierre emocional

Agregar una seccion final con copy romantico.

Ejemplo:

```text
Estos datos no son solo numeros. Son pedacitos de nosotros.
```

## Reglas sobre datos

1. Usar `message_normalized` para busquedas, conteos y patrones.
2. Usar `message` para mostrar frases al usuario.
3. Excluir valores vacios, NULL, NA, N/A, nan, none y null.
4. No mostrar mensajes crudos no limpiados.
5. No exponer errores tecnicos en frontend.
6. No usar tablas crudas como componente principal.
7. No recalcular transformaciones pesadas dentro de Streamlit.
8. Mantener queries SQL parametrizadas.
9. Mantener SQL dentro de modulos de queries o capa de acceso a datos.
10. No meter logica ETL en el frontend.

## Backlog tecnico solicitado

Implementar o ajustar, segun la estructura existente:

1. Modulo de metricas romanticas.
2. Queries para conteos de frases romanticas.
3. Query para primer mensaje.
4. Query para primer `te amo`.
5. Query para primer `te extrano`.
6. Query para dia con mas mensajes.
7. Query para mes con mas mensajes.
8. Query para hora favorita.
9. Query para frases bonitas destacadas.
10. Funcion agregadora que devuelva un diccionario listo para la landing.

## Ejemplo de estructura deseada

Si el proyecto ya tiene una carpeta `db/`, agregar o modificar:

```text
db/romantic_queries.py
```

Si el proyecto tiene una capa de servicios, agregar:

```text
services/romantic_metrics.py
```

La app Streamlit debe consumir funciones de alto nivel, por ejemplo:

```python
metrics = get_romantic_landing_metrics()
```

No debe tener SQL complejo incrustado directamente en la pantalla principal.

## Output esperado

Devolver unicamente:

- rutas de archivos modificados;
- contenido completo de cada archivo modificado.

No incluir explicaciones adicionales.
