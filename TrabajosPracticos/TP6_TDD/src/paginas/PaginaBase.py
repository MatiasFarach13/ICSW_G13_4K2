from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QApplication
from core.utilidades import aplicar_estilo


class PaginaBase(QWidget):
    def __init__(self, titulo=None, callback_volver=None, callback_cerrar=None):
        super().__init__()
        self.callback_volver = callback_volver
        self.callback_cerrar = callback_cerrar

        self.tema_actual = "oscuro"

        self.boton_tema = QPushButton("L")
        self.boton_tema.setFixedSize(35, 32)
        self.boton_tema.clicked.connect(self.toggle_tema)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.boton_cerrar = QPushButton("Cerrar")
        self.boton_cerrar.setFixedSize(80, 32)
        self.boton_cerrar.setStyleSheet(
            "background-color: #e57373; color: white;")
        self.boton_cerrar.clicked.connect(self.cerrar)

        header_layout = QHBoxLayout()
        header_layout.addWidget(self.boton_tema)
        header_layout.addStretch()
        header_layout.addWidget(self.boton_cerrar)

        self.layout.addLayout(header_layout)

        self.contenedor = QVBoxLayout()
        self.layout.addLayout(self.contenedor)
        self.layout.addStretch()

        if titulo:
            self.contenedor.addWidget(QLabel(f"<h1>{titulo}</h1>"))

        self.boton_volver = QPushButton("← Volver")
        self.boton_volver.setFixedHeight(30)
        self.boton_volver.clicked.connect(self.volver)

        self.boton_extra = QPushButton("")
        self.boton_extra.setFixedHeight(30)

        footer_layout = QHBoxLayout()
        footer_layout.addWidget(self.boton_volver)
        footer_layout.addStretch()
        footer_layout.addWidget(self.boton_extra)

        self.layout.addLayout(footer_layout)

    def agregar_widget(self, widget):
        self.contenedor.addWidget(widget)

    def volver(self):
        if self.callback_volver:
            self.callback_volver(self)

    def cerrar(self):
        if self.callback_cerrar:
            self.callback_cerrar(self)

    def set_boton_extra_texto(self, texto):
        self.boton_extra.setText(texto)

    def conectar_boton_extra(self, funcion):
        self.boton_extra.clicked.connect(funcion)

    def toggle_tema(self):
        app = QApplication.instance()
        if self.tema_actual == "claro":
            self.tema_actual = "oscuro"
            self.boton_tema.setText("L")
            aplicar_estilo(app, modo="oscuro")
        else:
            self.tema_actual = "claro"
            self.boton_tema.setText("D")
            aplicar_estilo(app, modo="claro")
