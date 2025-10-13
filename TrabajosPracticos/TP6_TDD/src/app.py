from flask import Flask, render_template, request, jsonify, redirect, url_for
from datetime import date, timedelta
import sys
import os

# Agregar la carpeta src al path para importar entradas
sys.path.append(os.path.dirname(__file__))
from clases.gestorCompraEntradas import GestorCompraEntradas, ParqueError

app = Flask(__name__)

# Crear instancia del gestor
gestor = GestorCompraEntradas()

@app.route('/')
def inicio():
    return render_template('inicio.html')

@app.route('/comprar')
def comprar():
    return render_template('comprar.html', date=date, timedelta=timedelta)

@app.route('/procesar_compra', methods=['POST'])
def procesar_compra():
    try:
        fecha_str = request.form['fecha_visita']
        edades = [int(edad) for edad in request.form.getlist('edades')]
        tipos_pase = request.form.getlist('tipos_pase')
        forma_pago = request.form['forma_pago']
        email = request.form['email']
        fecha_visita = date.fromisoformat(fecha_str)
        def enviar_email_web(email, datos):
            print(f"Email enviado a {email}: {datos}")
        
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
        return render_template('confirmacion.html', resultado=resultado)
    except ParqueError as e:
        return render_template('error.html', error=str(e))
    except Exception as e:
        return render_template('error.html', error=f"Error inesperado: {str(e)}")

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
            email=data['email']
        )
        return jsonify({"success": True, "resultado": resultado})
    except ParqueError as e:
        return jsonify({"success": False, "error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
