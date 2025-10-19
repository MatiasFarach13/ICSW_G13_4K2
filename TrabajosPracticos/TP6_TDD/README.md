```markdown
# TP6 - Sistema de Compra de Entradas

Breve guía para ejecutar, probar y preparar este repositorio para push.

## Resumen
Proyecto de ejemplo para la compra de entradas con reglas de negocio y una pequeña API en Flask y una interfaz frontend (React).

```markdown
# TP6 - Sistema de Compra de Entradas (TDD)

Este repositorio contiene un pequeño sistema para la compra de entradas, desarrollado con un backend en Flask y un frontend en React. El proyecto fue desarrollado con la metodología TDD (Test-Driven Development); más abajo explico cómo se aplicó y cómo escribir/ejecutar tests.

Tabla de contenidos
- Requisitos
- Cómo ejecutar (backend + frontend)
- Tests y TDD (cómo están organizados y flujo recomendado)
- Estructura del proyecto (breve descripción)
- Buenas prácticas y notas

## Requisitos
- Python 3.11+
- Node.js 18+
- npm o yarn
- virtualenv (recomendado para el backend)

## Ejecutar la aplicación (desarrollo)
La aplicación se compone de dos partes: el backend (Flask) que expone la API y sirve plantillas, y el frontend (React) que contiene la interfaz. Arranca ambos en dos terminales separados.

1) Backend (Flask)

```bash
# desde la raíz del repo
cd backend/src
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r ../../requirements.txt

# arrancar servidor en modo desarrollo
export FLASK_APP=src.app
export FLASK_ENV=development
export DATABASE_URL="sqlite:///./data.db"  # opcional
python -m src.app
```

El backend quedará escuchando en http://localhost:5000

2) Frontend (desarrollo)

```bash
cd frontend
npm install
# arrancar dev server (Vite / CRA según configuración)
npm run dev
```

Por defecto el dev server sirve la UI en http://localhost:5173 (o el puerto que Vite/CRA asigne). Asegúrate de que las llamadas al backend apunten a http://localhost:5000 (usa `proxy` en `frontend/package.json` o configura CORS en el backend).

3) Credenciales de desarrollo

Si usas la base de datos en archivo, el sistema crea usuarios seed para pruebas:
- juan@example.com / juanpass
- ana@example.com / anapass

## Tests y TDD
Este proyecto sigue un flujo TDD básico: primero se escriben tests unitarios para la regla o función deseada, luego se implementa la mínima lógica para que pase el test, y finalmente se refactoriza.

Dónde están los tests
- Los tests de backend están en `backend/src/test/` (por ejemplo `test_compraEntradas.py`, `test_models.py`).

Cómo correr los tests

```bash
# desde la raíz del repo
pip install -r requirements-dev.txt
pytest -v
```

Flujo recomendado para TDD (pasos concretos)
1. Escribe un test pequeño que describa la nueva función o regla (fallará al principio).
2. Ejecuta `pytest -q` y verifica que el test falla por la razón esperada.
3. Implementa la mínima lógica para que el test pase.
4. Ejecuta de nuevo los tests y confirma que pasan.
5. Refactoriza el código y los tests según sea necesario.

Consejos prácticos de TDD para este repo
- Crea tests unitarios para `clases/` (gestor de compras, validaciones) sin tocar el backend HTTP.
- Para endpoints HTTP, usa `Flask` test client desde los tests (o requests hacia el servidor si prefieres tests de integración).
- Mantén tests pequeños y enfocadas a una sola responsabilidad.

## Estructura del proyecto (breve)
- `backend/src/` — Código backend en Flask, modelos SQLAlchemy, y lógica de negocio.
	- `clases/` — clases del dominio (Compra, Usuario, entradas, etc.).
	- `templates/` y `static/` — plantillas Jinja y recursos estáticos que usa el backend.
	- `test/` — tests unitarios del backend.
- `frontend/` — aplicación React (src, public, package.json).
- `requirements.txt` — dependencias runtime del backend.
- `requirements-dev.txt` — dependencias de desarrollo (tests).

## Buenas prácticas y notas
- No subir `data.db` ni archivos con credenciales; usa `.env` local y añade `.env.example` con claves de ejemplo.
- Mantén `node_modules/` y artefactos de build (`dist/`, `build/`) en `.gitignore`.
- Para trabajar en TDD, crea ramas pequeñas por cada historia y abre PRs con referencia a los tests que agregaste.

## Cómo contribuir
- Fork -> branch -> cambios -> tests -> PR.
- Incluye tests para cualquier cambio de lógica y documenta decisiones importantes en el PR.

---

Trabajo Práctico 6 - Grupo 13
``` 