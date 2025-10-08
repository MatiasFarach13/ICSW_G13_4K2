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
EDAD_SENIOR_MIN = 60
DESCUENTO_PORCENTAJE = 0.5
DIAS_ANTICIPACION_MAX = 30
FECHAS_CERRADO_FERIADO = [(12, 25), (1, 1)]  # (mes, día)

# --- Funciones de Validación (Helpers) ---

def _validar_fecha(fecha_visita):
    hoy = date.today()
    if fecha_visita < hoy:
        raise FechaInvalidaError("La fecha de visita no puede ser en el pasado.")
    if fecha_visita > (hoy + timedelta(days=DIAS_ANTICIPACION_MAX)):
        raise FechaInvalidaError(f"Solo se puede comprar con hasta {DIAS_ANTICIPACION_MAX} días de anticipación.")
    if fecha_visita.weekday() == 0:  # lunes
        raise ParqueCerradoError("El parque está cerrado los lunes.")
    if (fecha_visita.month, fecha_visita.day) in FECHAS_CERRADO_FERIADO:
        raise ParqueCerradoError("El parque está cerrado por feriado.")


def _validar_cantidad(cantidad):
    if not (1 <= cantidad <= 10):
        raise CantidadInvalidaError("La cantidad de entradas debe ser entre 1 y 10.")


def _validar_pago(forma_pago):
    if forma_pago is None:
        raise PagoInvalidoError("Debe seleccionar una forma de pago.")


# --- Cálculo de precios considerando edades y tipos ---
def _calcular_monto_total(edades, tipos_pase):
    """
    Calcula el total combinando edades y tipos de pase.
    Cada elemento de 'edades' tiene un tipo correspondiente en 'tipos_pase'.
    """
    if len(edades) != len(tipos_pase):
        raise ValueError("La cantidad de edades y tipos de pase debe coincidir.")

    total = 0
    for edad, tipo in zip(edades, tipos_pase):
        precio_base = PRECIOS_PASE.get(tipo, 0)
        if edad <= EDAD_INFANTE_MAX:
            precio = 0
        elif 4 <= edad <= EDAD_NINO_MAX or edad >= EDAD_SENIOR_MIN:
            precio = precio_base * DESCUENTO_PORCENTAJE
        else:
            precio = precio_base
        total += precio
    return total


# --- Función principal ---
def comprar_entradas(fecha_visita, edades, tipos_pase, forma_pago):
    cantidad = len(edades)

    # Validaciones
    _validar_cantidad(cantidad)
    _validar_pago(forma_pago)
    _validar_fecha(fecha_visita)

    # Cálculo del monto total
    total_pagado = _calcular_monto_total(edades, tipos_pase)

    # Resultado simulado
    return {
        "status": "confirmado",
        "email": f"confirmacion_{fecha_visita.isoformat()}@parque.com",
        "cantidad": cantidad,
        "total_pagado": total_pagado,
        "fecha": fecha_visita.isoformat(),
    }
