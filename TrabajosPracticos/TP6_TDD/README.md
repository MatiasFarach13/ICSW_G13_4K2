```markdown
# TP6 - Sistema de Compra de Entradas

Breve guía para ejecutar, probar y preparar este repositorio para push.

## Resumen
Proyecto de ejemplo para la compra de entradas con reglas de negocio y una pequeña API en Flask y una interfaz frontend (React).

## Requisitos
- Python 3.11+
- Node.js 18+ (para el frontend)
- npm o yarn
- virtualenv (recomendado para el backend)

## Instalación (backend)

```bash
# desde la raíz del repo
cd backend/src
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r ../../requirements.txt
```


## Instalación (frontend)
```bash
cd frontend
npm install
# o si usas yarn:
# yarn
```

## Ejecutar la aplicación completa (desarrollo)
Arrancar el backend y el frontend en dos terminales separados.

1) Backend (Flask)

```bash
# desde backend/src con el virtualenv activado
export FLASK_APP=src.app
export FLASK_ENV=development
# opcional: usar base de datos en archivo
export DATABASE_URL="sqlite:///./data.db"
python -m src.app
```

La API/servidor estará disponible en http://localhost:5000

2) Frontend (desarrollo)

```bash
# desde la carpeta frontend
cd frontend
npm run dev
```

- juan@example.com / juanpass
- ana@example.com / anapass

Por defecto el dev server (Vite/CRA) servirá la UI en http://localhost:5173 (u otro puerto que el configurado). Asegúrate de que las llamadas al backend apunten a http://localhost:5000 (puedes configurar un proxy en `frontend/package.json` o en el dev server).

## Ejecutar sólo backend (modo producción mínimo)
```bash
# con virtualenv activado y variables seteadas
python  backend/src/app.py
# o
cd backend/src
python  app.py
```

## Ejecutar tests (Python)
```bash
# desde la raíz del repo
pytest -v
```
---

Trabajo Práctico 6 - Grupo 13