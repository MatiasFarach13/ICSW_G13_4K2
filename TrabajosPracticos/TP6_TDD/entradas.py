# entradas.py (versión final refactorizada)

from datetime import date, timedelta

# --- Definición de Excepciones ---
class ParqueError(Exception): pass
class ParqueCerradoError(ParqueError): pass
class PagoInvalidoError(ParqueError): pass
class CantidadInvalidaError(ParqueError): pass
class FechaInvalidaError(ParqueError): pass

# --- Constantes de Reglas de Negocio ---
PRECIOS_PASE = {"VIP": 10000, "Regular": 5000}
EDAD_INFANTE_MAX = 3
EDAD_NINO_MAX = 15
EDAD_SENIOR_MIN = 61
DESCUENTO_PORCENTAJE = 0.5
DIAS_ANTICIPACION_MAX = 30
FECHAS_CERRADO_FERIADO = [(12, 25), (1, 1)] # (mes, día)

# --- Funciones de Validación (Helpers) ---

def _validar_fecha(fecha_visita):
    hoy = date.today()
    if fecha_visita < hoy:
        raise FechaInvalidaError("La fecha de visita no puede ser en el pasado.")
    if fecha_visita > (hoy + timedelta(days=DIAS_ANTICIPACION_MAX)):
        raise FechaInvalidaError(f"Solo se puede comprar con hasta {DIAS_ANTICIPACION_MAX} días de anticipación.")
    if fecha_visita.weekday() == 0:
        raise ParqueCerradoError("El parque está cerrado los lunes.")
    if (fecha_visita.month, fecha_visita.day) in FECHAS_CERRADO_FERIADO:
        raise ParqueCerradoError("El parque está cerrado por feriado.")

def _validar_cantidad(cantidad):
    if not (1 <= cantidad <= 10):
        raise CantidadInvalidaError("La cantidad de entradas debe ser entre 1 y 10.")

def _validar_pago(forma_pago):
    if forma_pago is None:
        raise PagoInvalidoError("Debe seleccionar una forma de pago.")

# --- Función de Cálculo de Precios ---

def _calcular_monto_total(edades, tipo_pase):
    precio_base = PRECIOS_PASE.get(tipo_pase, 0)
    monto_total = 0
    for edad in edades:
        if edad <= EDAD_INFANTE_MAX:
            precio_entrada = 0
        elif (EDAD_INFANTE_MAX < edad <= EDAD_NINO_MAX) or (edad >= EDAD_SENIOR_MIN):
            precio_entrada = precio_base * DESCUENTO_PORCENTAJE
        else:
            precio_entrada = precio_base
        monto_total += precio_entrada
    return monto_total

# --- Función Principal ---

def comprar_entradas(fecha_visita, cantidad, edades, tipo_pase, forma_pago):
    # 1. Validaciones
    _validar_cantidad(cantidad)
    _validar_pago(forma_pago)
    _validar_fecha(fecha_visita)
    
    # 2. Lógica de Negocio
    monto_total = _calcular_monto_total(edades, tipo_pase)

    # 3. Simulación de resultado
    return {
        "status": "confirmado",
        "email": f"confirmacion_{fecha_visita.isoformat()}@parque.com",
        "cantidad": cantidad,
        "tipo_pase": tipo_pase,
        "monto_total": monto_total,
    }
