# Alcance solicitado - landing romantica

## Contexto general

El usuario quiere transformar la aplicacion actual, que ya procesa conversaciones de WhatsApp e Instagram con ETL, PostgreSQL y analisis, en una landing page romantica personalizada para su novia.

La intencion principal no es construir un dashboard tecnico ni un reporte de analitica, sino una experiencia emocional basada en datos reales de la relacion: mensajes, fechas, frases, palabras frecuentes y momentos compartidos.

El trabajo se dividira en dos sesiones independientes:

1. Logica de negocio.
2. Refactor visual.

## Sesion 1 - Logica de negocio

### Objetivo

Refactorizar la logica visible de la aplicacion para convertir datos tecnicos en storytelling romantico.

Esta sesion debe definir y preparar:

- Metricas romanticas.
- Queries necesarias.
- Funciones agregadoras.
- Lenguaje emocional para la interfaz.
- Separacion entre backend, analisis y frontend.
- Datos listos para ser consumidos por una landing.

### Lo que el usuario quiere mostrar

- Total de mensajes compartidos.
- Total de dias con conversacion.
- Fecha del primer mensaje registrado.
- Mes con mas mensajes.
- Dia con mas mensajes.
- Hora favorita para hablar.
- Persona que inicia mas conversaciones, si la logica existe.
- Conteos de frases romanticas.
- Primer mensaje.
- Primer "te amo".
- Primer "te extrano".
- Primer "me haces feliz".
- Dia con mas conversacion.
- Mes mas intenso.
- Frases romanticas memorables.
- Palabras o expresiones que representan a la pareja.
- Ritmo de conversacion por hora, dia y mes (histograma, serie de tiempo).

### Frases romanticas a contar

Las busquedas deben hacerse sobre `message_normalized`, pero los textos mostrados al usuario deben salir de `message`.

Patrones solicitados:

- `te amo`
- `te adoro`
- `te extrano`
- `mi amor`
- `amor mio`
- `mi vida`
- `amor`
- `preciosa`
- `hermosa`
- `hermosa`
- `linda`
- `divina`
- `me haces feliz`
- `odio`
- `hate`

### Secciones esperadas para la landing

- Hero romantico.
- Nuestra historia en numeros.
- Momentos que marcaron nuestra historia.
- Palabras que nos representan.
- Frases bonitas.
- Nuestro ritmo.
- Cierre emocional.

### Reglas funcionales importantes

- Usar `message_normalized` para busquedas, conteos y patrones.
- Usar `message` para mostrar frases.
- Excluir valores vacios, `NULL`, `NA`, `N/A`, `nan`, `none` y `null`.
- No mostrar mensajes crudos no limpiados.
- No mostrar errores tecnicos en Streamlit.
- No usar tablas crudas como componente principal.
- No recalcular transformaciones pesadas en Streamlit.
- Mantener SQL parametrizado.
- Mantener SQL dentro de `db/queries.py` o la capa de acceso a datos permitida.
- No meter logica ETL en frontend.
- No mostrar conceptos tecnicos de NLP en la interfaz.

### Arquitectura deseada

La separacion debe quedar asi:

- ETL y backend: extraccion, transformacion, carga, normalizacion, limpieza y PostgreSQL.
- Queries y metricas romanticas: consultas SQL, conteos, fechas importantes, palabras romanticas y momentos destacados.
- Frontend y landing: storytelling, cards, timeline, copy romantico y visualizacion suave.

El prompt sugiere crear o ajustar:

- `db/romantic_queries.py`, si encaja con la arquitectura.
- `services/romantic_metrics.py`, si se agrega una capa de servicios.

La app Streamlit deberia consumir una funcion de alto nivel similar a:

```python
metrics = get_romantic_landing_metrics()
```

## Sesion 2 - Refactor visual

### Objetivo

Refactorizar exclusivamente la capa visual y de experiencia de usuario de Streamlit para que la app parezca una landing romantica premium, no un dashboard tecnico.

Esta sesion debe enfocarse en:

- CSS personalizado.
- Paleta romantica.
- Layout visual.
- Cards.
- Bento grid.
- Glassmorphism.
- Tipografia.
- Espaciado.
- Responsividad mobile-first.
- Estilizacion de graficos Plotly o Altair.

### Restricciones de esta sesion

- No implementar ETL nuevo.
- No implementar NLP nuevo.
- No mover logica pesada al frontend.
- No cambiar arquitectura backend salvo que sea estrictamente necesario para renderizar.
- No agregar dependencias pesadas.
- No mostrar dark mode.
- No mostrar tablas crudas en la vista principal.
- No exponer errores internos al usuario.

### CSS obligatorio

El prompt pide inyectar CSS personalizado con:

```python
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
```

El CSS debe centralizarse en una constante clara, o en un modulo dedicado si la estructura lo permite, por ejemplo:

```text
ui/styles.py
```

### Sistema visual esperado

La interfaz debe sentirse:

- Suave.
- Limpia.
- Femenina sin ser infantil.
- Romantica.
- Moderna.
- Premium.
- Mobile-first.
- Visualmente consistente.

La paleta base solicitada usa blanco, rosa suave, fucsia y texto marron/rosa oscuro, evitando negro puro, dark mode, grises corporativos y azules de dashboard.

### Componentes visuales esperados

- Hero romantico con titulo grande, subtitulo emocional y fondo suave.
- Cards de metricas con label romantico, numero grande y descripcion breve.
- Bento grid responsiva.
- Timeline de momentos importantes.
- Cards elegantes para frases bonitas.
- Graficos suaves integrados visualmente.

### Lenguaje de interfaz

Los textos tecnicos deben reemplazarse por lenguaje emocional.

Ejemplos de intencion:

- "Message count by hour" debe convertirse en "Nuestra hora favorita para hablar".
- "Keyword frequency" debe convertirse en "Las palabras que mas nos representan".
- "Sentiment analysis" debe convertirse en "La energia bonita de nuestros mensajes".

### Estructura sugerida

Si el proyecto lo permite, la estructura visual puede organizarse asi:

```text
ui/
  styles.py
  components.py
  charts.py
services/
  romantic_metrics.py
```

Responsabilidades:

- `ui/styles.py`: CSS y constantes visuales.
- `ui/components.py`: hero, cards, timeline y secciones.
- `ui/charts.py`: helpers para Plotly o Altair.
- `services/romantic_metrics.py`: datos listos para pintar, consumiendo backend o queries.

## Resultado esperado final

La aplicacion debe dejar de sentirse como dashboard tecnico y pasar a sentirse como una landing romantica personalizada, basada en datos reales de la relacion.

La primera sesion prepara los datos y la narrativa. La segunda sesion transforma la experiencia visual.
