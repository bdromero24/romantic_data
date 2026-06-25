Necesito corregir la sección **“Un mensaje que quiero guardar”** sin romper el diseño general de la landing.

## Objetivo

Arreglar tres cosas específicas dentro del bloque especial:

1. Eliminar completamente los textos/títulos duplicados que aparecen arriba de la card principal:

   * `FRASES BONITAS`
   * `Un mensaje que quiero guardar`
   * `Me gusta saber lo que sientes.`

2. Mantener intacto el bloque visual principal donde se renderizan:

   * los 5 mensajes de ella;
   * la conversación tipo chat.

3. Hacer parametrizables/editables los subtítulos internos del bloque, por ejemplo:

   * `Cosas bonitas que ella me dijo`
   * `Una conversación que quiero recordar`

Actualmente esos subtítulos deben poder cambiarse desde configuración, es decir quemar un string, no quedar hardcodeados.

---

## Contexto actual

En `content_config.py` existe una estructura como:

```python
"special_message": {
    "title": "Un mensaje que quiero guardar",
    "subtitle": "Hay palabras que merecen quedarse <strong>aquí</strong>.",
    "blocks": [
        {
            "type": "her_messages",
            "title": "",
            "message_ids": [5038, 5039, 5040, 5041, 5042],
        },
        {
            "type": "conversation_pair",
            "title": "",
            "messages": [...]
        },
    ],
}
```

Quiero que los títulos internos de cada bloque sean editables desde esa configuración.

Por ejemplo:

```python
{
    "type": "her_messages",
    "title": "Cosas bonitas que ella me dijo",
    "message_ids": [5038, 5039, 5040, 5041, 5042],
}
```

y:

```python
{
    "type": "conversation_pair",
    "title": "Una conversación que quiero recordar",
    "messages": [...]
}
```

Si el campo `title` está vacío, no debe renderizar un título vacío ni dejar espacios raros.

---

## Requerimiento visual

Los subtítulos internos del bloque especial, como:

* `Cosas bonitas que ella me dijo`
* `Una conversación que quiero recordar`

deben renderizarse con el mismo efecto visual de títulos fucsia usado en la landing:

* `fuchsia text glow`
* `soft glow text shadow`
* CSS con `text-shadow`

No aplicar esto a todo el texto. Solo a esos subtítulos internos del bloque especial.

---

## Reglas importantes

* No modificar el diseño general de la landing.
* No tocar los IDs de mensajes configurados.
* No eliminar los 5 mensajes de ella.
* No eliminar la conversación.
* No cambiar la lógica ETL.
* No cambiar queries.
* No introducir errores técnicos visibles en UI.
* Mantener `st.markdown(..., unsafe_allow_html=True)` para HTML visual.
* Escapar contenido dinámico de base de datos si aplica.
* Mantener el estilo romántico/premium actual.

---

## Resultado esperado

La sección debe quedar así:

1. Sin los tres textos duplicados arriba:

   * sin `FRASES BONITAS`;
   * sin título repetido fuera de la card;
   * sin subtítulo repetido fuera de la card.

2. La card principal debe conservar:

   * título cursivo grande;
   * subtítulo;
   * bloque de 5 mensajes de ella;
   * bloque de conversación.

3. Los subtítulos internos deben:

   * venir desde `content_config.py`;
   * poder editarse manualmente;
   * renderizarse con `fuchsia text glow / soft glow text shadow`.

---

## Documentación

Actualizar la documentación correspondiente indicando:

* en qué archivo se parametrizan los títulos internos del bloque especial;
* qué script renderiza esa sección;
* qué cambio visual se aplicó;
* cómo dejar vacío un título si no se quiere mostrar.

También documentar la sesión/cambio en el archivo de debug o changelog del proyecto si existe.

---

## Entregable

Devuélveme:

1. archivos modificados;
2. código completo por archivo;
3. explicación breve de qué cambió;
4. sin rediseñar la landing completa.
