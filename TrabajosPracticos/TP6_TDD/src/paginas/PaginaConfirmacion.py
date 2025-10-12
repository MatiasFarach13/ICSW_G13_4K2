from PyQt5.QtWidgets import (
    QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QStackedWidget,
    QTableWidget, QTableWidgetItem, QWidget, QHeaderView,
    QAbstractScrollArea,
    QSizePolicy
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from .PaginaBase import PaginaBase


class PaginaConfirmacion(PaginaBase):
    def __init__(
        self,
        callback_volver,
        callback_cerrar
    ):
        super().__init__("Resultados", callback_volver, callback_cerrar)
        self.boton_extra.hide()
        self.dias = dias
        self.j = j
        self.i = i
        self.a_c = a_c
        self.b_c = b_c
        self.a_lc = a_lc
        self.b_lc = b_lc
        self.x = x
        self.a_dc = a_dc
        self.b_dc = b_dc
        self.c_dc = c_dc

        simulador = Simulador(
            self.x, self.a_dc, self.b_dc, self.c_dc, self.b_c)
        # Aca vamos a tener que sacar los datos para hacer los reportes sobre las consginas pedidas
        # Faltan hacer la generacion de las tablas
        # Faltan mostrar lo reportes
        # Falta poder sacar los reportes de la Simulacion
        self.iteraciones, self.max_cant_clientes = simulador.simular(
            self.dias, self.j, self.i, self.a_c, self.b_c, self.a_lc, self.b_lc)
        self.info_simulacion, self.reporte = simulador.crear_salidas()
        self.runge_kutta = simulador.get_iteraciones_runge_kutta()

        self.agregar_widget(
            QLabel(f"<h2>Simulación de Centro de Masajes Urbanos</h2>"))
        self.stack = QStackedWidget()
        self.stack.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.stack.addWidget(self._widget_vectores())
        self.stack.addWidget(self._widget_runge_kutta())

        # Botones de navegación de vistas
        botones = QHBoxLayout()
        for txt, handler in [
            ("Vectores Estado", self.mostrar_vectores),
            ("Runge Kutta", self.mostrar_runge_kutta)
        ]:
            btn = QPushButton(txt)
            btn.clicked.connect(handler)
            botones.addWidget(btn)
        self.contenedor.addLayout(botones)

        # Navegación interna de serie
        self.contenedor.addWidget(self.stack)

    def _widget_runge_kutta(self):
        contenedor = QWidget()
        layout = QVBoxLayout(contenedor)

        layout.addWidget(QLabel(f"""
            <h3>Aproximación iterativa de dC/dx = {self.a_dc}*(C(x) + {self.b_dc})^2 + {self.c_dc}</h3>
        """))

        tabla = QTableWidget(len(self.runge_kutta), 8)
        tabla.setHorizontalHeaderLabels(
            ["x i", "C i", "k1", "k2", "k3", "k4", "x i + 1", "C i + 1"]
        )
        tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        for i, it in enumerate(self.runge_kutta):
            for j, clave in enumerate(it):
                item = QTableWidgetItem(f"{it[clave]:.4f}")
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                tabla.setItem(i, j, item)
        layout.addWidget(tabla)

        return contenedor

    def _widget_vectores(self):
        contenedor = QWidget()
        layout = QVBoxLayout(contenedor)

        font = QFont()
        font.setBold(True)

        layout.addWidget(QLabel(self.info_simulacion))
        layout.addWidget(QLabel(f"""
                    <h3 style="color:#2E86C1;">📊 Parámetros Seleccionados</h3>
                    <p><strong>Distribución de tensión muscular:</strong> U({self.a_c}, {self.b_c})</p>
                    <p><strong>Distribución de llegada de clientes:</strong> U({self.a_lc}, {self.b_lc})</p>
                    <p><strong>Vectores recolectados:</strong> {self.i} a partir del minuto {self.j}</p>
                    """))
        layout.addWidget(QLabel(self.reporte))

        tabla = QTableWidget(len(self.iteraciones) + 2, 28 +
                             self.max_cant_clientes * 4)
        tabla.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Cabecera 1

        cabecera1 = [("", 0, 2),
                     ("Comienzo Jornada Laboral", 2, 2),
                     ("Llegada Cliente", 4, 5),
                     ("Fin Jornada Laboral", 9, 2),
                     ("Fin Servicio Masajista A", 11, 4),
                     ("Fin Servicio Masajista B", 15, 3),
                     ("Fin Servicio Masajista Ap", 18, 3),
                     ("Masajistas", 21, 3),
                     ("Indicadores de Simulacion", 24, 4)
                     ]
        for i in range(self.max_cant_clientes):
            cabecera1.append((f"Cliente {i + 1}", 28 + i*4, 4))

        for texto, inicio, ancho in cabecera1:
            tabla.setSpan(0, inicio, 1, ancho)
            item = QTableWidgetItem(texto)
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            item.setToolTip(item.text())
            item.setTextAlignment(Qt.AlignCenter)
            item.setFont(font)
            item.setBackground(Qt.gray)
            tabla.setItem(0, inicio, item)

        # Cabecera 2

        cabecera2 = ["Reloj", "Estado Actual", "Tiempo", "Prox Ev", "RND",
                     "Tiempo", "Prox Ev", "RND", "Masajista Asig", "Tiempo",
                     "Prox Ev", "RND", "Tension", "Tiempo",
                     "Prox Ev", "RND", "Tiempo", "Prox Ev", "RND", "Tiempo", "Prox Ev", "M A Estado",
                     "M B Estado", "M Ap Estado", "Cola Max", "Acc Recaudacion Daria", "Acc Recaudacion Total", "Cant Dias Simulados"]

        for i in range(self.max_cant_clientes):
            cabecera2.extend(["ID", "Estado", "Hora Llegada", "Tiempo Espera"])

        for i, titulo in enumerate(cabecera2):
            item = QTableWidgetItem(titulo)
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            item.setToolTip(item.text())
            item.setTextAlignment(Qt.AlignCenter)
            item.setFont(font)
            item.setBackground(Qt.gray)
            tabla.setItem(1, i, item)

        # Cabecera Vertical
        cabecera_vertical = ["", ""] + \
            [str(i + 1) for i in range(len(self.iteraciones) - 1)]
        cabecera_vertical.append("Ult Vec")
        tabla.setVerticalHeaderLabels(cabecera_vertical)

        # Datos de Iteraciones
        for i, valores in enumerate(self.iteraciones):
            for j, v in enumerate(valores):
                item = QTableWidgetItem(v)
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                item.setToolTip(item.text())
                tabla.setItem(i + 2, j, item)

        # Configuraciones adicionales a la tabla
        tabla.setMinimumHeight(500)
        tabla.resizeColumnsToContents()
        tabla.resizeRowsToContents()
        tabla.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
        tabla.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        tabla.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        tabla.horizontalHeader().setVisible(False)

        layout.addWidget(tabla)

        return contenedor

    # Vistas
    def mostrar_vectores(self):
        self.stack.setCurrentIndex(0)

    def mostrar_runge_kutta(self):
        self.stack.setCurrentIndex(1)
