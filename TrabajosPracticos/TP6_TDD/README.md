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
npm run dev
```

- juan@example.com / juanpass
- ana@example.com / anapass

Por defecto el dev server (Vite/CRA) servirá la UI en http://localhost:5173 (u otro puerto que el configurado). Asegúrate de que las llamadas al backend apunten a http://localhost:5000 (puedes configurar un proxy en `frontend/package.json` o en el dev server).

## Ejecutar sólo backend (modo producción mínimo)
```bash
# con virtualenv activado y variables seteadas
python -m src.app
```

## Ejecutar tests (Python)
```bash
# desde la raíz del repo
pytest -v
```

## Notas rápidas
- Usuarios seed (si usas archivo DB): `juan@example.com / juanpass`, `ana@example.com / anapass`.
- El sistema simula el envío de emails por consola.
- En desarrollo no hay protecciones completas (CSRF, recuperación de contraseña, etc.).

## Recomendaciones/ayudas
- Si el frontend hace requests a otro puerto, añade un proxy en `frontend/package.json` o configura CORS en el backend.
- Si quieres migrar a TypeScript o separar carpetas, revisa `frontend/src` y decide entre `.jsx` y `.tsx`.

## Checklist antes de push
- [ ] Asegurar que `data.db` o credenciales de desarrollo no se suben al repositorio
- [ ] Actualizar `requirements.txt` si agregaste nuevas dependencias
- [ ] Añadir instrucciones específicas si cambias puertos o proxys

---

Trabajo Práctico 6 - Grupo 13
````

---

Trabajo Práctico 6 - Grupo 13