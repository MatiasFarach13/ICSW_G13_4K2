# Estándares de Código y Buenas Prácticas

Este documento recoge las convenciones de estilo, nombrado y buenas prácticas recomendadas para este proyecto (backend en Python/Flask y frontend en JavaScript/React). También incluye principios de diseño que sugerimos seguir (SOLID, KISS, DRY, YAGNI, TDD) y una pequeña checklist para revisiones de código.

## Tecnologías utilizadas
En el proyecto se usan (entre otras) las siguientes tecnologías y librerías:

- Backend (Python):
  - Flask (servidor web / microframework)
  - SQLAlchemy (ORM)
  - flask-login (gestión de sesiones/usuarios)
  - flask-jwt-extended (JWT para endpoints protegidos)
  - flask-cors (CORS en desarrollo)

- Frontend (JavaScript / TypeScript):
  - React (UI)
  - ReactDOM
  - React Router (navegación)
  - Vite (dev server / bundler)
  - TypeScript (el proyecto contiene soporte/archivos TS)

Estas tecnologías están listadas en `requirements.txt` (backend) y `frontend/package.json` (frontend). Consulta esos archivos para las versiones exactas.

## Principios generales
- TDD (Test-Driven Development): escribe tests antes de la implementación. Los tests deben ser rápidos, determinísticos y aislados.
- KISS: Keep It Simple, Stupid — preferir soluciones simples y comprensibles.
- DRY: Don't Repeat Yourself — extraer lógica común en funciones o módulos reutilizables.
- YAGNI: You Aren't Gonna Need It — no implementes abstracciones complejas hasta que sean necesarias.
- SOLID (aplicable sobre todo en clases/servicios backend):
  - Single Responsibility: cada clase o módulo debe tener una única responsabilidad.
  - Open/Closed: componentes abiertos a extensión, cerrados a modificación.
  - Liskov Substitution: las subclases deben poder sustituir a sus superclases.
  - Interface Segregation: interfaces específicas en lugar de generales.
  - Dependency Inversion: depender de abstracciones, no de implementaciones concretas.

## Convenciones de nombrado — Backend (Python / Flask)
- Archivos y módulos: `snake_case.py` (por ejemplo: `models.py`, `gestor_compra_entradas.py`).
- Paquetes (carpetas): `lowercase` sin espacios (por ejemplo `clases`, `templates`).
- Clases: `PascalCase` (por ejemplo `Usuario`, `Compra`, `GestorCompraEntradas`).
- Métodos y funciones: `snake_case` (por ejemplo `create_user_by_email`, `calcular_precio_total`).
- Variables locales y parámetros: `snake_case` (por ejemplo `total_entradas`, `fecha_evento`).
- Constantes: `UPPER_SNAKE_CASE` (por ejemplo `DB_URL_DEFAULT`, `MAX_ENTRADAS_POR_COMPRA`).
- Endpoints / rutas: usar nombres descriptivos y sustantivos, por ejemplo `/api/compras`, `/api/usuarios/<id>`.

Tipos y anotaciones
- Añade type hints en funciones públicas y métodos (Python 3.11+). Ejemplo:

```python
def calcular_precio(cantidad: int, tipo: str) -> float:
    ...
```

Documentación y docstrings
- Usa docstrings en funciones y clases (estilo Google o reST). Incluye descripción breve, parámetros y valor de retorno.

Errores y excepciones
- Define excepciones específicas cuando tenga sentido (por ejemplo `ParqueCerradoError`). No uses excepciones genéricas salvo en casos puntuales.

Formato
- Sigue PEP8. Usa `black` para formateo automático y `flake8` para linters si es posible.

## Convenciones de nombrado — Frontend (JavaScript / React)
- Archivos: `PascalCase.jsx/tsx` para componentes React (por ejemplo `App.jsx`, `ComprarForm.jsx`). Archivos utilitarios `camelCase.js` o `snake-case.js` según preferencia del equipo, preferimos `camelCase`.
- Componentes: `PascalCase` para componentes React (por ejemplo `ComprarForm`, `ConfirmacionTarjeta`).
- Funciones y variables: `camelCase` (por ejemplo `handleSubmit`, `totalPrice`).
- Hooks personalizados: `usePascalCase`, prefijo `use` (por ejemplo `useAuth`, `useFetch`).
- Carpetas: agrupa por características (feature folders) o por tipo (`components/`, `pages/`, `services/`, `styles/`).

JSX/TSX
- PropTypes o TypeScript: si usas JS puro, valida props con `prop-types`. Si usas TS, define `Props` con interfaces.
- Componentes pequeños y enfocados: un componente debe hacer una cosa y hacerlo bien.

State y efectos
- Preferir state local por componente cuando sea posible; global state sólo cuando sea necesario.
- Mantener efectos (`useEffect`) con dependencias completas y explícitas.

Servicios/API
- Centralizar llamadas al backend en `services/api.js` o carpeta `services/`.

Estilos
- Usa CSS Modules, `styled-components`, o una convención consistente (por ejemplo `styles/` o `src/styles/`). Evitar estilos en línea salvo casos puntuales.

## Estructura recomendada (sugerencia)
- backend/src/
  - app.py
  - models.py
  - clases/
  - templates/
  - static/
  - test/
- frontend/
  - public/
  - src/
    - components/
    - pages/
    - services/
    - styles/

## Testing (cómo escribir tests en este repo)
- Tests unitarios: rápidos, aislados, sin acceso a red ni disco (usar mocks).
- Tests de integración: cubrir interacciones entre módulos (p. ej. endpoints con DB en memoria o SQLite temporal).
- Coloca tests en `backend/src/test/` y nombra archivos `test_*.py`.
- Cada test debe documentar claramente el caso y las precondiciones.

Ejemplo (pytest):

```python
def test_calcular_precio_descuento():
    # arrange
    cantidad = 3
    tipo = 'adulto'
    # act
    res = calcular_precio(cantidad, tipo)
    # assert
    assert res == 3 * 100.0  # ejemplo
```

## Revisión de código (PR checklist)
- ¿Incluye tests nuevos o actualizados que cubran la funcionalidad?
- ¿Sigue las convenciones de nombrado?
- ¿Los cambios están documentados (README o comentarios relevantes)?
- ¿Se evitaron duplicaciones (DRY)?
- ¿Las funciones tienen responsabilidades claras y cortas? (SRP)
- ¿Hay type hints / PropTypes donde corresponde?
- ¿El código pasó linters/formateadores (`black`, `eslint`)?

## Herramientas recomendadas
- Formateo: `black` (Python), `prettier` (JS)
- Lint: `flake8` / `pylint` (Python), `eslint` (JS)
- Tests: `pytest` (Python)
- CI: ejecutar linters y tests en cada PR (GitHub Actions o similar)

---

Si quieres, adapto este documento a un formato más corto u otros idiomas, o creo plantillas de PR/Issue para reforzar estas reglas. También puedo añadir un archivo `CONTRIBUTING.md` que enlace a este estándar.
