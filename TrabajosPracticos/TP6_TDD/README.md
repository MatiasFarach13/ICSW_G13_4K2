# TP6 - Sistema de Compra de Entradas

Breve guía para ejecutar, probar y preparar este repositorio para push.

## Resumen
Proyecto de ejemplo para la compra de entradas con reglas de negocio y una pequeña API/plantillas web.

## Requisitos
- Python 3.11+
- Virtualenv

## Instalación
Linux
```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```
Windows (CMD)
```
python -m venv venv
.\venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Ejecutar la aplicación (recomendado)
Ejecutar en modo paquete para que las importaciones relativas funcionen correctamente:

Linux
```bash
export DATABASE_URL="sqlite:///./data.db"  # opcional, por defecto usa data.db
python -m src.app
```
Windows
```bash
set DATABASE_URL="sqlite:///./data.db # opcional, por defecto usa data.db
python -m src.app
```
La aplicación estará disponible en http://localhost:5000

## Usuarios seed (archivo DB solamente)
Al crear una base de datos en archivo (no en memoria) el sistema crea dos usuarios de ejemplo:

- juan@example.com / juanpass
- ana@example.com / anapass

Estos son para desarrollo y pruebas; cámbialos o elimínalos antes de producción.

## Notas sobre Login
- Visita `/login` e inicia sesión con email y contraseña.
- Si el usuario no existía, se crea y la contraseña ingresada se guarda (con hashing).
- Si el usuario existía, la contraseña se verifica.
- No es seguro para producción (no hay registro formal, recuperación de contraseña ni CSRF en formularios).

## Flujo de compra
- Debes iniciar sesión antes de comprar (las rutas principales requieren autenticación).
- El campo email fue eliminado del formulario de compra en la UI: el sistema usa el email del usuario autenticado.
- El sistema simula el envío de email (se imprime en la salida estándar) y muestra instrucciones de pago en la página de confirmación.

## Preparar para push (checklist)
- [ ] Actualizar `data.db` si no quieres subir datos de prueba
- [x] Añadir `.gitignore` para ignorar virtualenv, DB y artefactos
- [x] Asegurarse de que `requirements.txt` contiene las dependencias
- [ ] Actualizar `README.md` con cualquier instrucción adicional

---

Trabajo Práctico 6 - Grupo 13
