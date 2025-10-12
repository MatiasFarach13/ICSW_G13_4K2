from .PaginaBase import PaginaBase


class PaginaInicio(PaginaBase):
    def __init__(self, callback_seleccion, callback_volver, callback_cerrar):
        super().__init__("Bienvenido a la US Comprar entrada del Grupo 13",
                         callback_volver, callback_cerrar)
        self.callback = callback_seleccion

        self.boton_volver.hide()
        self.set_boton_extra_texto("Continuar")
        self.conectar_boton_extra(self.callback)
