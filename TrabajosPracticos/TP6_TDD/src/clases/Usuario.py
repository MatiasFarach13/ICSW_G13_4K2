from .Compra import Compra
class Usuario:
    nombre : str
    email : str
    compras : list[Compra]
    
    def __init__(self, nombre, email):
        self.nombre = nombre
        self.email = email
        self.compras = []
    
    def mostrar_compras(self):
        
        # esta mal esto (no funcionaria porque no se puede calcular el precio con categoria_edad)
        for compra in self.compras:
            print(f"Compra realizada el {compra.entradas[0].fecha_visita}:")
            for entrada in compra.entradas:
                precio = entrada.calcular_precio(entrada.categoria_edad)
                print(f" - Entrada {entrada.get_tipo()} para {entrada.categoria_edad}, Precio: ${precio}")
            total = sum(entrada.calcular_precio(entrada.categoria_edad) for entrada in compra.entradas)
            print(f" Total pagado: ${total}\n")     