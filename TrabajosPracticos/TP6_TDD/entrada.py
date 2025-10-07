#Funciones basicas SIN REFACTORIZAR
# Si se quiere testear este se debe cambiarle  el nombre a entradas.py

from datetime import date

class ParqueCerradoError(Exception):
    pass

class PagoInvalidoError(Exception):
    pass

class CantidadInvalidaError(Exception):
    pass


def comprar_entradas(fecha_visita, cantidad, edades, tipo_pase, forma_pago):
    # Validaciones
    if cantidad > 10:
        raise CantidadInvalidaError("No se pueden comprar más de 10 entradas")

    if forma_pago is None:
        raise PagoInvalidoError("Debe seleccionar una forma de pago")

    # Supongamos que el parque cierra los domingos
    if fecha_visita.weekday() == 6:  # 6 = domingo
        raise ParqueCerradoError("El parque está cerrado ese día")

    # Simulamos compra exitosa
    return {
        "status": "confirmado",
        "email": "confirmacion@parque.com",
        "cantidad": cantidad,
        "fecha": fecha_visita.isoformat(),
    }