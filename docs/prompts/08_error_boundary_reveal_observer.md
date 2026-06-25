# Prompt para Codex: corregir import de reveal observer y agregar manejo seguro de errores en Streamlit

Actúa como un desarrollador Python/Streamlit senior con foco en robustez, seguridad, logging y experiencia de usuario.

## Contexto

Proyecto:

```text
C:\Users\User\OneDrive\Escritorio\landing_page
```

App principal:

```text
app/main.py
```

Error actual:

```text
ImportError: cannot import name 'render_reveal_observer' from 'ui.components'
(C:\Users\User\OneDrive\Escritorio\landing_page\ui\components.py)
```

La app intenta importar `render_reveal_observer` desde `ui.components`, pero esa función no existe, fue renombrada, quedó en otro archivo o no fue agregada.

Además, necesito implementar manejo serio de errores:

- cualquier excepción debe registrarse únicamente en logs;
- no se deben mostrar tracebacks en la UI;
- no se deben exponer credenciales, rutas internas sensibles, variables de entorno ni detalles técnicos;
- en la UI solo debe mostrarse un mensaje genérico:

```text
Oops... Algo falló. Contacta al administrador.
```

---

# Objetivo

1. Corregir el error de importación de `render_reveal_observer`.
2. Mantener o desactivar de forma segura la animación reveal-on-scroll si hace falta.
3. Agregar manejo global de errores en la app Streamlit.
4. Registrar errores completos en logs.
5. Mostrar en UI solo un mensaje genérico y seguro.
6. Documentar el bug y la corrección.

---

# Parte 1: corregir `render_reveal_observer`

## Tarea

Inspeccionar:

```text
app/main.py
ui/components.py
ui/styles.py
```

y cualquier archivo relacionado con animaciones reveal-on-scroll.

Buscar:

```powershell
Get-ChildItem -Recurse -Filter *.py | Select-String -Pattern "render_reveal_observer|reveal|IntersectionObserver|components.html"
```

## Corrección esperada

Hay dos opciones válidas.

### Opción A: agregar la función faltante

Si `app/main.py` necesita llamar `render_reveal_observer`, agregar esta función en `ui/components.py` o moverla al módulo correcto y ajustar imports.

La función debe inyectar el observer de reveal-on-scroll de forma segura.

Ejemplo esperado:

```python
def render_reveal_observer() -> None:
    """Inject reveal-on-scroll observer script."""
    import streamlit.components.v1 as components

    observer_script = """
    <script>
    (function () {
        function initRevealObserver() {
            const revealElements = window.parent.document.querySelectorAll('.reveal-on-scroll');

            if (!('IntersectionObserver' in window.parent)) {
                revealElements.forEach((element) => element.classList.add('is-visible'));
                return;
            }

            const observer = new window.parent.IntersectionObserver((entries, observerInstance) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('is-visible');
                        observerInstance.unobserve(entry.target);
                    }
                });
            }, {
                threshold: 0.14,
                rootMargin: '0px 0px -40px 0px'
            });

            revealElements.forEach((element) => observer.observe(element));
        }

        setTimeout(initRevealObserver, 250);
    })();
    </script>
    """

    components.html(observer_script, height=0)
```

Adaptar si el proyecto ya tiene una implementación mejor.

### Opción B: eliminar el import y la llamada si no se va a usar

Si la animación reveal-on-scroll no quedó estable, eliminar:

```python
render_reveal_observer
```

del import en `app/main.py` y eliminar su llamada.

Pero si se elimina, dejar la app funcionando sin romper.

## Validación obligatoria

Ejecutar:

```powershell
python -c "import ui.components as c; print(c.__file__); print(hasattr(c, 'render_reveal_observer'))"
```

Si `app/main.py` importa `render_reveal_observer`, el resultado debe ser:

```text
True
```

Si el import fue eliminado, verificar que ya no aparezca:

```powershell
Get-ChildItem -Recurse -Filter *.py | Select-String -Pattern "render_reveal_observer"
```

---

# Parte 2: manejo global y seguro de errores en Streamlit

## Problema

Actualmente Streamlit muestra tracebacks técnicos en pantalla.

Eso no es aceptable para una landing romántica.

## Requerimiento

La UI nunca debe mostrar:

- traceback;
- rutas locales;
- nombres de archivos internos;
- credenciales;
- `DATABASE_URL`;
- usuario/contraseña de PostgreSQL;
- variables de entorno;
- detalles de conexión;
- SQL completo con parámetros sensibles;
- excepciones técnicas completas.

La UI solo debe mostrar:

```text
Oops... Algo falló. Contacta al administrador.
```

Opcionalmente se puede mostrar un subtítulo genérico:

```text
La página no pudo cargarse correctamente.
```

No mostrar detalles del error.

---

# Parte 3: crear helper de errores para Streamlit

Crear un módulo si no existe, por ejemplo:

```text
ui/error_boundary.py
```

o:

```text
app/error_boundary.py
```

Debe incluir funciones similares a:

```python
def log_app_exception(error: BaseException, context: str | None = None) -> None:
    ...

def render_safe_error_message() -> None:
    ...

def sanitize_error_message(message: str) -> str:
    ...
```

## Logging

Usar el logger existente si existe, por ejemplo:

```python
from logger.logger import log_critical_error
```

Si el logger existente no soporta traceback completo, usar además `logging.exception`.

El log debe capturar:

- tipo de excepción;
- mensaje;
- traceback completo;
- contexto, por ejemplo `"app.main"`;
- timestamp si el sistema de logging lo permite.

## Sanitización

Antes de escribir logs, se puede guardar error completo, pero nunca mostrarlo en UI.

Si algún mensaje se llega a usar en documentación o warning interno, sanitizar:

- URLs con credenciales;
- `postgresql://user:password@host/db`;
- `postgresql+psycopg2://user:password@host/db`;
- variables tipo `PASSWORD=...`;
- rutas locales si se decide no mostrarlas.

Pero en UI no mostrar ningún detalle técnico.

---

# Parte 4: envolver la app principal en error boundary

Refactorizar `app/main.py` para que la lógica principal quede en una función:

```python
def run_app() -> None:
    ...
```

y el entrypoint haga:

```python
def main() -> None:
    try:
        run_app()
    except Exception as error:
        log_app_exception(error, context="app.main")
        render_safe_error_message()

if __name__ == "__main__":
    main()
```

Si Streamlit ejecuta el archivo directamente, asegurar que este patrón se active.

## Importante

El `try/except` debe envolver la lógica de ejecución de la app, pero los imports superiores pueden seguir fallando antes de entrar al `try`.

Por eso:

1. Corregir primero imports rotos como `render_reveal_observer`.
2. Evitar imports opcionales frágiles en top-level.
3. Si hay imports opcionales, moverlos dentro de funciones y manejarlos con fallback seguro.

---

# Parte 5: configuración de Streamlit para no mostrar detalles al usuario

Verificar si existe:

```text
.streamlit/config.toml
```

Si no existe, crearla.

Agregar o ajustar:

```toml
[client]
showErrorDetails = false
```

Si la versión de Streamlit usa otra clave compatible, usar la correcta.

Esto ayuda a que Streamlit no muestre tracebacks detallados en la UI.

---

# Parte 6: UI del mensaje de error

El mensaje de error debe mantener estética romántica y limpia.

Crear una tarjeta visual simple, por ejemplo:

```python
def render_safe_error_message() -> None:
    import streamlit as st

    st.markdown(
        """
        <section class="safe-error-card">
            <h1>Oops... Algo falló</h1>
            <p>Contacta al administrador.</p>
        </section>
        """,
        unsafe_allow_html=True,
    )
```

CSS sugerido:

```css
.safe-error-card {
    max-width: 680px;
    margin: 6rem auto;
    padding: 2rem;
    border-radius: 28px;
    background: rgba(255, 255, 255, 0.72);
    border: 1px solid rgba(212, 20, 114, 0.28);
    box-shadow: 0 24px 70px rgba(212, 20, 114, 0.18);
    text-align: center;
}

.safe-error-card h1 {
    margin: 0 0 0.8rem;
    color: #3f2435;
    font-weight: 800;
}

.safe-error-card p {
    margin: 0;
    color: #8a5872;
    font-weight: 650;
}
```

Integrar en el CSS centralizado si existe.

---

# Parte 7: no ocultar bugs durante desarrollo interno

Aunque la UI oculte el traceback, el log debe tener suficiente detalle.

El objetivo es:

```text
UI limpia y segura
logs completos para depuración
```

No hacer `except: pass`.

No silenciar errores sin logging.

---

# Parte 8: documentación obligatoria

Actualizar o crear:

```text
docs/codex_session_debug.md
```

Agregar secciones:

```md
## Bug: ImportError de `render_reveal_observer`

### Síntoma

La app fallaba al iniciar porque `app/main.py` importaba `render_reveal_observer` desde `ui.components`, pero esa función no existía en el módulo real.

### Causa raíz

Indicar causa real encontrada.

### Archivos afectados

Listar rutas relativas.

### Corrección aplicada

Explicar si:
- se agregó `render_reveal_observer`;
- se movió al módulo correcto;
- se eliminó el import y la llamada;
- se dejó fallback seguro.

### Verificación

Indicar comando ejecutado:

```powershell
python -c "import ui.components as c; print(c.__file__); print(hasattr(c, 'render_reveal_observer'))"
```

### Resultado

Indicar resultado.
```

Agregar otra sección:

```md
## Mejora de seguridad: manejo global de errores en Streamlit

### Motivo

La UI no debe exponer tracebacks, rutas locales, credenciales ni detalles técnicos.

### Cambio aplicado

Indicar:
- módulo creado o modificado;
- patrón `run_app()` / `main()`;
- logger usado;
- configuración Streamlit aplicada.

### Comportamiento final

- Excepciones completas quedan en logs.
- UI muestra solo: `Oops... Algo falló. Contacta al administrador.`
- No se exponen credenciales ni detalles técnicos.

### Archivos afectados

Listar rutas relativas.
```

---

# Validaciones obligatorias

Ejecutar:

```powershell
streamlit run app/main.py
```

Validar:

1. La app no falla por `ImportError: render_reveal_observer`.
2. Si ocurre una excepción en runtime, la UI no muestra traceback.
3. La UI muestra solo:
   ```text
   Oops... Algo falló. Contacta al administrador.
   ```
4. El error queda registrado en logs.
5. No se muestran credenciales ni rutas sensibles en UI.
6. `.streamlit/config.toml` tiene `showErrorDetails = false` o configuración equivalente.
7. No se usa `except: pass`.

---

# Restricciones

No modificar ETL.

No modificar schema de base de datos.

No cambiar queries de negocio.

No cambiar mensajes configurados.

No cambiar secciones de contenido.

No instalar librerías nuevas.

No exponer tracebacks en UI.

No exponer credenciales.

No silenciar errores sin logging.

---

# Formato de respuesta esperado

Devuelve únicamente:

1. Rutas de archivos modificados.
2. Contenido completo de cada archivo modificado.
3. Contenido actualizado de `docs/codex_session_debug.md`.

No agregues explicaciones adicionales fuera de los archivos.
