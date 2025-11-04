from datetime import date, timedelta
from .entradasclase import Entrada
# --- Definición de Excepciones ---
class ParqueError(Exception): pass
class ParqueCerradoError(ParqueError): pass
class PagoInvalidoError(ParqueError): pass
class CantidadInvalidaError(ParqueError): pass
class FechaInvalidaError(ParqueError): pass
class EmailInvalidoError(ParqueError): pass

# --- Constantes de Reglas de Negocio ---
EDAD_INFANTE_MAX = 3
EDAD_NINO_MAX = 15
EDAD_SENIOR_MIN = 60
DESCUENTO_PORCENTAJE = 0.5
DIAS_ANTICIPACION_MAX = 30
FECHAS_CERRADO_FERIADO = [(12, 25), (1, 1)]  # (mes, día)
# --- Clase GestorCompraEntradas ---
class GestorCompraEntradas:
    cantidad: int
    edades: list[str]
    # init
    def __init__(self, cantidad, edades):
        self.cantidad = cantidad
        self.edades = edades
    
    def __init__(self):
        pass
    
    # metodos
    def comprar_entradas(self, fecha_visita, edades, entradas, forma_pago, email, enviar_email=None):
        self.validar_fecha(fecha_visita)
        self.validar_edades(edades)
        self.validar_cantidad(len(edades))
        self.validar_forma_pago(forma_pago)
        self.validar_email(email)
        
        
        resultado = {
        "status": "confirmado",
        "email": f"confirmacion_{fecha_visita.isoformat()}@parque.com",
        "cantidad": len(entradas),
        "total_pagado": self.calcular_monto_total(edades, entradas),
        "fecha": fecha_visita.isoformat(),
        }
        if enviar_email:
            enviar_email(email, resultado)
        return resultado 
    
    def validar_email(self, email):
        import re
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(patron, email):
            raise EmailInvalidoError("El formato del email es inválido.")
        return True

    def validar_edades(self, edades):
        if not edades:
            raise CantidadInvalidaError("Debe incluir al menos una edad.")
        for edad in edades:
            if not isinstance(edad, int) or edad < 0:
                raise CantidadInvalidaError("Cada edad debe ser un número positivo.")
        return True

    
    def validar_cantidad(self, cantidad):
        if 1<= cantidad <= 10:
            return True
        else:
            raise CantidadInvalidaError("La cantidad de entradas debe ser entre 1 y 10.")
        
    def validar_forma_pago(self, forma_pago):
        if forma_pago not in ["Efectivo", "Tarjeta"]:
            raise PagoInvalidoError("Debe seleccionar una forma de pago válida (Efectivo o Tarjeta).")
        return True

    def validar_fecha(self, fecha_visita):
        hoy = date.today()
        
        if fecha_visita < hoy:
            raise FechaInvalidaError("La fecha de visita no puede ser en el pasado.")
        if fecha_visita > (hoy + timedelta(days=DIAS_ANTICIPACION_MAX)):
            raise FechaInvalidaError(f"Solo se puede comprar con hasta {DIAS_ANTICIPACION_MAX} días de anticipación.")
        if fecha_visita.weekday() == 0: 
            raise ParqueCerradoError("El parque está cerrado los lunes.")
        if (fecha_visita.month, fecha_visita.day) in FECHAS_CERRADO_FERIADO:
            raise ParqueCerradoError("El parque está cerrado por feriado.") 
    
    def calcular_monto_total(self, edades, entradas):
        total = 0
        if len(edades) != len(entradas):
            raise ValueError("La cantidad de edades y las entradas debe coincidir.")
        for edad, entrada in zip(edades, entradas):
            total += entrada.calcular_precio(edad)
        return total  
    def crear_entrada(self, tipos, fecha_visita, edades):
        entradas = []
        for tipo, edad in zip(tipos, edades):
            entrada = Entrada(tipo, fecha_visita, edad)
            entradas.append(entrada)
        return entradas
    