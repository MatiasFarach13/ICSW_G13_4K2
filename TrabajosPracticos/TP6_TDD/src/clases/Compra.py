from .entradasclase import Entrada
from .Usuario import Usuario
class Compra:
    entradas: list[Entrada]
    usuario: Usuario
    
    def __init__(self, entradas, usuario):
        self.entradas = entradas
        self.usuario = usuario
        usuario.compras.append(self)