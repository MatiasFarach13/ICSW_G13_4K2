from flask import Flask, request, jsonify
from datetime import date, timedelta
import os
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)

# Importar tu lógica de negocio (imports relativos, porque este módulo está dentro del paquete `src`)
from .clases.gestorCompraEntradas import GestorCompraEntradas, ParqueError

# ============================================================
# 🔧 CONFIGURACIÓN INICIAL
# ============================================================

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET", "dev-secret")
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "super-secret")

# Permitir peticiones desde el frontend React
CORS(app, supports_credentials=True)

jwt = JWTManager(app)
# 🔧 Ajuste para compatibilidad con Flask-JWT-Extended >= 4.7
@jwt.user_identity_loader
def user_identity_lookup(user_id):
    # Se asegura de que siempre se use string como subject en el token
    return str(user_id)

gestor = GestorCompraEntradas()

# Base de datos
try:
    from .models import create_sqlite_db
    DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
    engine, SessionLocal = create_sqlite_db(DATABASE_URL)
except Exception:
    engine = None
    SessionLocal = None


def get_session():
    """Devuelve una sesión SQLAlchemy o None si no hay base."""
    global SessionLocal, engine
    if SessionLocal is None:
        try:
            from .models import create_sqlite_db
            DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
            engine, SessionLocal = create_sqlite_db(DATABASE_URL)
        except Exception:
            import traceback
            print('❌ Error inicializando DB:')
            traceback.print_exc()
            return None
    try:
        return SessionLocal()
    except Exception:
        import traceback
        print('❌ Error creando sesión:')
        traceback.print_exc()
        return None


# ============================================================
# 🔐 AUTENTICACIÓN JWT
# ============================================================

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    session = get_session()
    if session is None:
        return jsonify({'error': 'DB not available'}), 503

    try:
        from .models import get_or_create_user_by_email
        user = get_or_create_user_by_email(session, email)

        if user.password_hash and user.check_password(password):
            token = create_access_token(identity=user.id)
            return jsonify({
                "success": True,
                "token": token,
                "user": {"id": user.id, "email": user.email}
            }), 200
        else:
            return jsonify({"success": False, "error": "Credenciales inválidas"}), 401
    finally:
        session.close()

@app.route('/api/register', methods=['POST'])
def api_register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    session = get_session()
    if session is None:
        return jsonify({'error': 'DB not available'}), 503

    try:
        # ✅ Importamos antes de usar
        from .models import User

        # Verificar si ya existe el correo
        existing_user = session.query(User).filter_by(email=email).first()
        if existing_user:
            return jsonify({
                "success": False,
                "error": "El correo ya está registrado."
            }), 400

        # Crear nuevo usuario
        new_user = User(email=email)
        new_user.set_password(password)
        session.add(new_user)
        session.commit()

        # Generar token JWT
        token = create_access_token(identity=new_user.id)

        return jsonify({
            "success": True,
            "token": token,
            "user": {"id": new_user.id, "email": new_user.email}
        }), 201

    except Exception as e:
        import traceback
        print("❌ Error en registro:")
        print(traceback.format_exc())
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
    finally:
        session.close()



# ============================================================
# 🧾 API COMPRAS / ENTRADAS
# ============================================================

@app.route('/api/comprar', methods=['POST'])
@jwt_required()
def api_comprar():
    try:
        data = request.get_json()
        print("🟢 Datos recibidos:", data)
        fecha_visita = date.fromisoformat(data['fecha_visita'])
        edades = data['edades']
        tipos_pase = data['tipos_pase']
        forma_pago = data['forma_pago']
        email = data.get('email')

        entradas = gestor.crear_entrada(tipos_pase, fecha_visita, edades)
        resultado = gestor.comprar_entradas(
            fecha_visita=fecha_visita,
            edades=edades,
            entradas=entradas,
            forma_pago=forma_pago,
            email=email
        )

        # 🧮 Agregar detalle por participante (tipo, edad, precio final)
        detalle = [
            {
                "tipo": e.tipo_entrada.get_nombre(),
                "categoria": e.categoria_edad,
                "precio": e.precio
            }
            for e in entradas
        ]
        resultado["detalle"] = detalle


        session = get_session()
        if session is not None:
            from .models import Compra
            user_id = int(get_jwt_identity())
            compra = Compra(
                fecha=fecha_visita,
                cantidad=len(entradas),
                total=resultado['total_pagado'],
                forma_pago=forma_pago,
                user_id=user_id
            )
            session.add(compra)
            session.commit()
            session.close()

        return jsonify({"success": True, "resultado": resultado}), 200

    except ParqueError as e:
        print("⚠️ Error de negocio:", e)
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        import traceback
        print("❌ Error inesperado:")
        print(traceback.format_exc())
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/comprar-detalle', methods=['POST'])
@jwt_required()
def api_comprar_detalle():
    """Devuelve cálculo de precios y categorías sin registrar la compra."""
    try:
        data = request.get_json()
        print("📦 Datos recibidos:", data)  # debug

        # 🧩 Validar claves necesarias
        required = ['fecha_visita', 'edades', 'tipos_pase']
        for campo in required:
            if campo not in data:
                return jsonify({
                    "success": False,
                    "error": f"Falta el campo obligatorio '{campo}'"
                }), 400

        # 🗓️ Conversión y limpieza
        fecha_visita = date.fromisoformat(data['fecha_visita'])
        edades = [int(e) if isinstance(e, (int, float, str)) and str(e).isdigit() else 0 for e in data['edades']]
        tipos_pase = data['tipos_pase']

        # ⚙️ Crear instancia del gestor (clave del problema)
        gestor = GestorCompraEntradas()

        # 🎟️ Crear entradas con sus precios y categorías
        entradas = gestor.crear_entrada(tipos_pase, fecha_visita, edades)
        total = gestor.calcular_monto_total(edades, entradas)

        detalle = [
            {
                "tipo": e.get_tipo(),
                "categoria": e.categoria_edad,
                "precio": e.precio
            }
            for e in entradas
        ]

        print("✅ Cálculo exitoso:", detalle, "TOTAL:", total)

        return jsonify({
            "success": True,
            "resultado": {
                "total_pagado": total,
                "detalle": detalle
            }
        }), 200

    except Exception as e:
        import traceback
        print("❌ Error en cálculo de detalle:")
        print(traceback.format_exc())
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/compras', methods=['GET'])
@jwt_required()
def api_list_compras():
    """Lista todas las compras del usuario autenticado"""
    session = get_session()
    if session is None:
        return jsonify({'error': 'DB not available'}), 503

    user_id = int(get_jwt_identity())
    try:
        from .models import Compra
        compras = session.query(Compra).filter_by(user_id=user_id).all()
        return jsonify([
            {
                'id': c.id,
                'fecha': c.fecha.isoformat(),
                'cantidad': c.cantidad,
                'total': c.total,
                'forma_pago': c.forma_pago
            } for c in compras
        ])
    finally:
        session.close()


@app.route('/api/users', methods=['GET'])
@jwt_required()
def api_list_users():
    """Solo para pruebas o admin."""
    session = get_session()
    if session is None:
        return jsonify({'error': 'DB not available'}), 503
    try:
        from .models import User
        users = session.query(User).all()
        return jsonify([{'id': u.id, 'email': u.email, 'name': u.name} for u in users])
    finally:
        session.close()


# ============================================================
# 🔍 TEST ROUTE
# ============================================================

@app.route('/api/protegida')
@jwt_required()
def api_protegida():
    user_id = int(get_jwt_identity())
    return jsonify({"message": f"Ruta protegida. Usuario ID: {user_id}"})


# ============================================================
# 🚀 MAIN
# ============================================================

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
