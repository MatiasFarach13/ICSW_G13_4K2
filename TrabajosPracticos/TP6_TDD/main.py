import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QStackedWidget

from core.utilidades import aplicar_estilo

from paginas.PaginaInicio import PaginaInicio
from paginas.PaginaComprar import PaginaComprar
from paginas.PaginaConfirmacion import PaginaConfirmacion


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ICSW TP6")
        self.setGeometry(100, 100, 800, 900)

        # Layout principal
        main_layout = QVBoxLayout(self)
        self.stack = QStackedWidget()
        main_layout.addWidget(self.stack)

        # Página inicial
        inicio = PaginaInicio(
            callback_seleccion=self.comprar_entrada,
            callback_volver=self.volver,
            callback_cerrar=self.cerrar_aplicacion,
        )
        self.stack.addWidget(inicio)

    def comprar_entrada(self):
        comprar = PaginaComprar(
            callback_generado=self.confirmacion_compra,
            callback_volver=self.volver,
            callback_cerrar=self.cerrar_aplicacion,
        )
        self.stack.addWidget(comprar)
        self.stack.setCurrentWidget(comprar)

    def confirmacion_compra(self):
        confirmacion = PaginaConfirmacion(
            callback_volver=self.volver,
            callback_cerrar=self.cerrar_aplicacion,
        )
        self.stack.addWidget(confirmacion)
        self.stack.setCurrentWidget(confirmacion)

    def volver(self, pagina_actual):
        if isinstance(pagina_actual, PaginaResultados):
            Id().reset()
        self.stack.removeWidget(pagina_actual)
        self.stack.setCurrentIndex(self.stack.count() - 1)

    @staticmethod
    def cerrar_aplicacion(self):
        QApplication.quit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    aplicar_estilo(app, modo="oscuro")

    ventana = MainWindow()
    ventana.show()
    sys.exit(app.exec())
