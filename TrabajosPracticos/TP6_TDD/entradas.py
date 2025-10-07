#Funciones refactorizadas

from datetime import date

class ParqueError(Exception): pass
class ParqueCerradoError(ParqueError): pass
class PagoInvalidoError(ParqueError): pass
class CantidadInvalidaError(ParqueError): pass


def _validar_cantidad(cantidad):
    if not (1 <= cantidad <= 10):
        raise CantidadInvalidaError("La cantidad debe ser entre 1 y 10")


def _validar_pago(forma_pago):
    if forma_pago is None:
        raise PagoInvalidoError("Debe seleccionar una forma de pago")


def _validar_fecha(fecha_visita):
    if fecha_visita.weekday() == 6:
        raise ParqueCerradoError("El parque está cerrado los domingos")


def comprar_entradas(fecha_visita, cantidad, edades, tipo_pase, forma_pago):
    _validar_cantidad(cantidad)
    _validar_pago(forma_pago)
    _validar_fecha(fecha_visita)

    # Simula el proceso de compra y confirmación por email
    return {
        "status": "confirmado",
        "email": f"confirmacion_{fecha_visita.isoformat()}@parque.com",
        "cantidad": cantidad,
        "tipo_pase": tipo_pase,
    }
