# Prompt para Codex — agregar card “Hater de tiempo completo”

Quiero hacer una última adición a la landing romántica sin cambiar el diseño general.

## Objetivo

Agregar **una sola card nueva** al frontend con esta intención:

- título superior: **Hater de tiempo completo**
- palabra principal en el centro: **odio**
- texto inferior: **Utilizaste la palabra odio X veces**

Esta card debe mantener el mismo lenguaje visual de las demás cards/KPIs de la landing: estilo romántico premium, paleta rosa/fucsia/blanco, tipografía consistente, bordes redondeados, glassmorphism si aplica, y sin romper la composición actual.

---

## Contexto funcional

Mi novia usa mucho la palabra **“odio”** y también **“hate”** para expresar fastidio. Esto es una inside joke entre nosotros porque yo le digo que es **“hater de tiempo completo”**.

Quiero que la card represente eso.

---

## Alcance

Implementar todo lo necesario para que la card funcione correctamente:

1. **query / helper backend** para contar cuántas veces ella dijo “odio”;
2. si es razonable y está bien encapsulado, también contemplar la variante **“hate”** como equivalente opcional;
3. integrar el dato al payload/diccionario que consume el frontend;
4. renderizar la nueva card en la landing;
5. mantener el diseño general intacto.

---

## Requerimiento principal de conteo

Necesito una query que cuente cuántas veces **ella** dijo la palabra **“odio/hate”**.

Reglas:

- contar solo mensajes cuyo `sender` sea el de ella;
- usar `message_normalized` para la búsqueda;
- hacer coincidencia por palabra, no por substring arbitrario;
- evitar contar `None`, vacíos o basura;
- SQL parametrizado, sin interpolación insegura.

Si ves conveniente, puedes implementar una variante que cuente **“odio” y “hate”** juntas, siempre que:

- quede claro en el código;
- sea fácil de mantener;
- el texto visible de la card siga mostrando **“odio”**.

Si decides incluir ambas, documenta el criterio con un comentario corto.

---

## Query esperada

Crear o actualizar el módulo de queries/helpers para incorporar una función equivalente a una de estas dos opciones.

### Opción estricta
Contar solo “odio”:

```sql
SELECT COUNT(*) AS total_odio
FROM messages
WHERE sender = :sender_name
  AND message_normalized IS NOT NULL
  AND TRIM(message_normalized) <> ''
  AND message_normalized ~* '\\modio\\M';
```

### Opción extendida
Contar “odio” o “hate”:

```sql
SELECT COUNT(*) AS total_odio
FROM messages
WHERE sender = :sender_name
  AND message_normalized IS NOT NULL
  AND TRIM(message_normalized) <> ''
  AND message_normalized ~* '\\m(odio|hate)\\M';
```

Usa la opción que consideres más alineada con el requerimiento, pero mantén el texto visual de la card centrado en **odio**.

---

## Configuración del sender de ella

No hardcodees el nombre directamente si el proyecto ya tiene una configuración para distinguir entre “me” y “her”.

Preferencias:

1. reutilizar una constante/config existente del proyecto;
2. si no existe, crear una forma simple y clara de configurar el sender de ella;
3. no romper la lógica actual.

---

## Integración al flujo de datos

Actualizar la capa donde se construyen las métricas visibles de la landing para agregar algo como:

```python
{
    "hater_full_time": {
        "title": "Hater de tiempo completo",
        "keyword": "odio",
        "count": 123,
        "description": "Utilizaste la palabra odio 123 veces"
    }
}
```

No es obligatorio usar exactamente esos nombres, pero sí una estructura clara y consistente con el resto del proyecto.

---

## Requerimiento visual de la card

Agregar una card con esta estructura visual:

- arriba: **Hater de tiempo completo**
- centro: **odio**
- abajo: **Utilizaste la palabra odio X veces**

### Reglas visuales

- debe verse como parte natural del sistema actual de cards;
- mantener paleta existente;
- mantener tipografías actuales;
- usar el mismo tratamiento visual que la card de métricas o de “palabra bonita más usada”, si existe una card similar reutilizable;
- no convertir esto en un bloque técnico;
- no agregar tablas;
- no cambiar layout general más allá de insertar esta card donde tenga sentido.
- ubicarla en la seccion de pequeños datos bonitos en el espacio vacio si es posible, sino documentar por que y que sea atractiva y coherente la ubicacion visual. 

Si existe un componente reutilizable para metric cards / keyword cards, reutilízalo.

---

## Ubicación sugerida

Insertar esta card cerca de las métricas o de la sección donde aparecen cards tipo:

- palabra bonita más usada;
- pequeños datos bonitos;
- KPIs románticos.

Usa el lugar que mejor respete la composición actual sin rediseñar la página completa.

---

## Texto visible exacto

Usar este copy:

- **Título:** `Hater de tiempo completo`
- **Palabra central:** `odio`
- **Texto inferior:** `Utilizaste la palabra odio {count} veces`

Si quieres, puedes manejar singular/plural correctamente cuando el conteo sea 1, pero no es obligatorio.

---

## Restricciones

- no cambiar el diseño general de la landing;
- no tocar otras secciones si no hace falta;
- no exponer lógica técnica al usuario final;
- no usar `message` para buscar, usar `message_normalized`;
- no romper las métricas existentes;
- no usar SQL no parametrizado;
- no mostrar errores técnicos en UI.

---

## Entregables esperados

Haz los cambios necesarios en los archivos correspondientes del proyecto, probablemente en capas equivalentes a:

- queries / db helpers;
- capa de agregación de métricas;
- frontend / render de cards;
- documentación breve si aplica.

---

## Resultado esperado

Al finalizar, la landing debe mostrar una nueva card romántica/juguetona con el inside joke:

- **Hater de tiempo completo**
- **odio**
- **Utilizaste la palabra odio X veces**

alimentada por una query real que cuenta las ocurrencias dichas por ella.

---

## Formato de respuesta

Devuélveme:

1. los archivos modificados;
2. código completo por archivo;
3. sin explicaciones largas;
4. manteniendo consistencia con la arquitectura actual del proyecto.
