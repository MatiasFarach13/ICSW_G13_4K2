from src.clases.TipoEntrada import TipoEntrada
from datetime import date as Date
EDAD_INFANTE_MAX = 3
EDAD_NINO_MAX = 15
EDAD_SENIOR_MIN = 60
DESCUENTO_PORCENTAJE = 0.5
class Entrada:
    #atributos
    tipo_entrada: TipoEntrada
    fecha_visita: Date
    categoria_edad: str
    
    #init
    def __init__(self, nombre_tipo, fecha_visita, edad):
        self.tipo_entrada = self.crear_tipo_entrada(nombre_tipo)
        self.fecha_visita = fecha_visita
        print(f"mi edad es: {edad}")
        self.categoria_edad = self.determinar_categoria_edad(edad)

    #metodos
    def calcular_precio(self, edad):
        precio_con_descuento = self.tipo_entrada.get_precio_base() * (1 - self.calcular_descuento(edad))
        return round(precio_con_descuento, 2)
    
    def get_tipo(self):
        return self.tipo_entrada.get_nombre()
    
    def sos_tipo(self, nombre):
        return self.tipo_entrada.sos_tipo(nombre)
    
    def crear_tipo_entrada(self, nombre):
        return TipoEntrada(nombre)
    
    def calcular_descuento(self, edad):
        if edad <= EDAD_INFANTE_MAX:
            return 1.0  # Gratis
        elif 4 <= edad <= EDAD_NINO_MAX or edad >= EDAD_SENIOR_MIN:
            return DESCUENTO_PORCENTAJE  # 50% de descuento
        else:
            return 0
    
    def determinar_categoria_edad(self, edad):
        if edad <= 3: return "infante"
        elif 4 <= edad <= 15: return "niño"
        elif edad >= 60: return "senior"
        else: return "adulto"