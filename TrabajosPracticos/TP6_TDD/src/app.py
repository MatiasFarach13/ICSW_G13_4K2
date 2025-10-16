from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from datetime import date, timedelta
import sys
import os

from src.clases.gestorCompraEntradas import GestorCompraEntradas, ParqueError
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

# minimal SQLAlchemy wiring (assume package mode: import from src.models)
try:
    from src.models import create_sqlite_db
    # Allow configuring a persistent DB file via env var; default to sqlite:///data.db
    DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
    engine, SessionLocal = create_sqlite_db(DATABASE_URL)
except Exception:
    # If SQLAlchemy not installed or import fails, keep app working without DB
    engine = None
    SessionLocal = None


def get_session():
    """Return a new Session instance or None if DB is not available.

    This will attempt to lazily initialize the DB if previous module-level
    initialization failed (for example different interpreter or missing env).
    """
    global SessionLocal, engine
    if SessionLocal is None:
        try:
            from src.models import create_sqlite_db
            DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
            engine, SessionLocal = create_sqlite_db(DATABASE_URL)
        except Exception:
            import traceback
            print('Failed to initialize DB in get_session():')
            traceback.print_exc()
            return None
    try:
        return SessionLocal()
    except Exception:
        import traceback
        print('Failed to create Session from SessionLocal():')
        traceback.print_exc()
        return None

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET', 'dev-secret')

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    session = get_session()
    if session is None:
        return None
    try:
        from src.models import User
        return session.query(User).get(int(user_id))
    finally:
        session.close()

# Crear instancia del gestor
gestor = GestorCompraEntradas()

@app.route('/')
@login_required
def inicio():
    return render_template('inicio.html')

@app.route('/comprar')
@login_required
def comprar():
    return render_template('comprar.html', date=date, timedelta=timedelta)

@app.route('/comprar-react')
def comprar_react():
    """Versión React del formulario de compra (sin cambiar estructura)."""
    return render_template('comprar_react.html')

@app.route('/confirmacion-react')
def confirmacion_react():
    """Pantalla de confirmación implementada en React."""
    return render_template('confirmacion_react.html')

@app.route('/procesar_compra', methods=['POST'])
@login_required
def procesar_compra():
    try:
        fecha_str = request.form['fecha_visita']
        edades = [int(edad) for edad in request.form.getlist('edades')]
        tipos_pase = request.form.getlist('tipos_pase')
        forma_pago = request.form['forma_pago']
        # deduce email from logged-in user when possible; fall back to form field for compatibility
        if current_user and getattr(current_user, 'is_authenticated', False):
            email = getattr(current_user, 'email', None)
        else:
            email = request.form.get('email')
        fecha_visita = date.fromisoformat(fecha_str)
        def enviar_email_web(email, datos):
            print(f"Email enviado a {email}: {datos}")
            # simulated email sent (logged to stdout); no flash message to keep static confirmation page
        
        # Crear entradas usando el gestor
        entradas = gestor.crear_entrada(tipos_pase, fecha_visita, edades)
        
        resultado = gestor.comprar_entradas(
            fecha_visita=fecha_visita,
            edades=edades,
            entradas=entradas,
            forma_pago=forma_pago,
            email=email,
            enviar_email=enviar_email_web
        )
        # Add simulated payment instructions/messages for the non-API flow
        if forma_pago == 'Efectivo':
            resultado['instrucciones_pago'] = 'Por favor, realizar el pago en boletería el día de la visita.'
        elif forma_pago == 'Tarjeta':
            resultado['instrucciones_pago'] = 'Integración MercadoPago simulada: pago procesado correctamente.'
        # Persist the compra if DB available and user logged in
        session = get_session()
        if session is not None:
            try:
                from src.models import Compra, get_or_create_user_by_email
                user_id = None
                if current_user and hasattr(current_user, 'id'):
                    user_id = current_user.id
                else:
                    # ensure user exists by email
                    user = get_or_create_user_by_email(session, email)
                    user_id = user.id
                c = Compra(fecha=fecha_visita, cantidad=len(entradas), total=resultado['total_pagado'], forma_pago=forma_pago, user_id=user_id)
                session.add(c)
                session.commit()
            except Exception:
                import traceback
                print('Failed to persist compra:')
                traceback.print_exc()
            finally:
                session.close()
        return render_template('confirmacion.html', resultado=resultado)
    except ParqueError as e:
        return render_template('error.html', error=str(e))
    except Exception as e:
        import traceback
        print("=== ERROR COMPLETO ===")
        print(traceback.format_exc())
        print("=== FIN ERROR ===")
        return render_template('error.html', error=f"Error inesperado: {str(e)}")


@app.route('/login', methods=['GET', 'POST'])
def login():
    from flask import flash
    # If already logged in, redirect to inicio
    if current_user and getattr(current_user, 'is_authenticated', False):
        return redirect(url_for('inicio'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        session = get_session()
        if session is None:
            flash('DB not available', 'error')
            return redirect(url_for('login'))
        try:
            from src.models import get_or_create_user_by_email
            # get or create user (seeds name later if empty)
            user = get_or_create_user_by_email(session, email)
            # if user exists and has a password, verify it
            if user.password_hash:
                if not user.check_password(password):
                    flash('Contraseña incorrecta', 'error')
                    return redirect(url_for('login'))
            else:
                # set password for first-time user (convenience)
                user.set_password(password)
                session.add(user)
                session.commit()
            login_user(user)
            return redirect(url_for('inicio'))
        finally:
            session.close()
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('inicio'))

@app.route('/api/comprar', methods=['POST'])
def api_comprar():
    try:
        data = request.get_json()
        fecha_visita = date.fromisoformat(data['fecha_visita'])
        
        # Crear entradas usando el gestor
        entradas = gestor.crear_entrada(data['tipos_pase'], fecha_visita, data['edades'])
        
        resultado = gestor.comprar_entradas(
            fecha_visita=fecha_visita,
            edades=data['edades'],
            entradas=entradas,
            forma_pago=data['forma_pago'],
            email=data.get('email')
        )
        # Simulate payment instructions
        if data.get('forma_pago') == 'Efectivo':
            mensaje_pago = 'Por favor, realizar el pago en boletería el día de la visita.'
            resultado['instrucciones_pago'] = mensaje_pago
        elif data.get('forma_pago') == 'Tarjeta':
            # simulate MercadoPago success message for credit card flows
            mensaje_pago = 'Integración MercadoPago simulada: pago procesado correctamente.'
            resultado['instrucciones_pago'] = mensaje_pago
        return jsonify({"success": True, "resultado": resultado})
    except ParqueError as e:
        return jsonify({"success": False, "error": str(e)}), 400


@app.route('/api/users', methods=['GET'])
def api_list_users():
    session = get_session()
    if session is None:
        return jsonify({'error': 'DB not available'}), 503
    try:
        from src.models import User
        users = session.query(User).all()
        return jsonify([{'id': u.id, 'email': u.email, 'name': u.name} for u in users])
    finally:
        session.close()


@app.route('/api/compras', methods=['GET'])
def api_list_compras():
    session = get_session()
    if session is None:
        return jsonify({'error': 'DB not available'}), 503
    try:
        from src.models import Compra
        compras = session.query(Compra).all()
        return jsonify([{
            'id': c.id,
            'fecha': c.fecha.isoformat(),
            'cantidad': c.cantidad,
            'total': c.total,
            'forma_pago': c.forma_pago,
            'user_id': c.user_id
        } for c in compras])
    finally:
        session.close()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
