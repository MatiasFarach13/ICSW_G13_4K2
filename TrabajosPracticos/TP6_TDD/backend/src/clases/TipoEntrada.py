class TipoEntrada:
    nombre: str
    PrecioBase: float
    
    def __init__(self, nombre: str):
        self.nombre = nombre
        self.set_precio_base(nombre)
        
    
    def sos_tipo(self, nombre: str) -> bool:
        return self.nombre == nombre
    
    def get_precio_base(self) -> float:
        return self.PrecioBase
    
    def get_nombre(self) -> str:
        return self.nombre
    
    def set_precio_base(self, nombre):
        if nombre.upper() == "REGULAR":
            self.PrecioBase = 5000.0
        elif nombre.upper() == "VIP":
            self.PrecioBase = 10000.0
        else:
            raise ValueError(f"Tipo de entrada desconocido: {nombre}")
    
    