from PyQt5.QtWidgets import QLabel, QDoubleSpinBox, QSpinBox
from .PaginaBase import PaginaBase


class PaginaComprar(PaginaBase):
    def __init__(self, callback_generado, callback_volver, callback_cerrar):
        super().__init__("Eleccion de Parametros", callback_volver, callback_cerrar)

        self.callback = callback_generado
        self.MAX_LIM = 1000000
        self.MIN_LIM = -1000000

        # Falta verificar los rangos de estas variables
        self.entrada_tiempo_sim = QSpinBox()
        self.entrada_tiempo_sim.setValue(2)
        self.entrada_tiempo_sim.setMinimum(1)
        self.entrada_tiempo_sim.setRange(0, self.MAX_LIM)

        self.entrada_j = QDoubleSpinBox()
        self.entrada_j.setDecimals(2)
        self.entrada_j.setSingleStep(0.01)
        self.entrada_j.setValue(0)
        self.entrada_j.setRange(0, self.MAX_LIM)

        self.entrada_i = QSpinBox()
        self.entrada_i.setValue(10)
        self.entrada_i.setRange(1, 100000)

        self.entrada_a_c = QDoubleSpinBox()
        self.entrada_a_c.setValue(3)
        self.entrada_a_c.setSingleStep(0.01)
        self.entrada_a_c.setRange(0.01, self.MAX_LIM)
        self.entrada_a_c.valueChanged.connect(self._actualizar_min_b_c)

        self.entrada_b_c = QDoubleSpinBox()
        self.entrada_b_c.setValue(10)
        self.entrada_b_c.setSingleStep(0.01)
        self.entrada_b_c.setRange(0.01, self.MAX_LIM)

        self.entrada_a_lc = QDoubleSpinBox()
        self.entrada_a_lc.setValue(2)
        self.entrada_a_lc.setSingleStep(0.01)
        self.entrada_a_lc.setRange(0, self.MAX_LIM)
        self.entrada_a_lc.valueChanged.connect(self._actualizar_min_b_lc)

        self.entrada_b_lc = QDoubleSpinBox()
        self.entrada_b_lc.setValue(12)
        self.entrada_b_lc.setSingleStep(0.01)
        self.entrada_b_lc.setRange(1, self.MAX_LIM)

        self.entrada_x = QDoubleSpinBox()
        self.entrada_x.setValue(0.01)
        self.entrada_x.setSingleStep(0.01)
        self.entrada_x.setRange(0.000000001, self.MAX_LIM)

        self.entrada_a_dc = QDoubleSpinBox()
        self.entrada_a_dc.setValue(2)
        self.entrada_a_dc.setSingleStep(0.01)
        self.entrada_a_dc.setRange(self.MIN_LIM, self.MAX_LIM)

        self.entrada_b_dc = QDoubleSpinBox()
        self.entrada_b_dc.setValue(0.5)
        self.entrada_b_dc.setSingleStep(0.01)
        self.entrada_b_dc.setRange(self.MIN_LIM, self.MAX_LIM)

        self.entrada_c_dc = QDoubleSpinBox()
        self.entrada_c_dc.setValue(50)
        self.entrada_c_dc.setSingleStep(0.01)
        self.entrada_c_dc.setRange(self.MIN_LIM, self.MAX_LIM)
        # Corroborar si es correcto poner este limite en el rango para la desv estandar
        # Hay que ver con cuantos decimales trabajamos

        self.set_boton_extra_texto("Simular")
        self.conectar_boton_extra(self.simular)

        self.agregar_widget(
            QLabel("<h3> Para el tiempo de simulación y muestra de iteraciones: </h3>"))

        self.agregar_widget(QLabel("Ingrese el Tiempo de Simulación (dias): "))
        self.agregar_widget(self.entrada_tiempo_sim)

        self.agregar_widget(QLabel(
            "Ingrese el minuto j a partir de la cual se mostrarán los vectores de estado (min): "))
        self.agregar_widget(self.entrada_j)

        self.agregar_widget(QLabel(
            "Ingrese la cantidad i de vectores de estado que se mostraran a partir del tiempo j: "))
        self.agregar_widget(self.entrada_i)

        self.agregar_widget(QLabel(
            "<h3>Para la distribución de tension muscular C del cliente U(A; B): </h3>"))

        self.agregar_widget(QLabel("Ingrese el valor A: "))
        self.agregar_widget(self.entrada_a_c)

        self.agregar_widget(QLabel("Ingrese el valor B: "))
        self.agregar_widget(self.entrada_b_c)

        self.agregar_widget(QLabel(
            "<h3>Para la distribución de tiempo de llegada del cliente U(A; B): </h3>"))

        self.agregar_widget(QLabel("Ingrese el valor A: "))
        self.agregar_widget(self.entrada_a_lc)

        self.agregar_widget(QLabel("Ingrese el valor B: "))
        self.agregar_widget(self.entrada_b_lc)

        self.agregar_widget(QLabel(
            "<h3>Para la derivada de duración del masaje respecto de la tensoin muscular dC/dx = a*(C(x) + b)^2 + c: </h3>"))

        self.agregar_widget(QLabel(
            "Ingrese la equivalencia de 1 minuto respecto de x de la función de tension: "))
        self.agregar_widget(self.entrada_x)

        self.agregar_widget(QLabel("Ingrese el valor de a: "))
        self.agregar_widget(self.entrada_a_dc)

        self.agregar_widget(QLabel("Ingrese el valor de b: "))
        self.agregar_widget(self.entrada_b_dc)

        self.agregar_widget(QLabel("Ingrese el valor de c: "))
        self.agregar_widget(self.entrada_c_dc)

        # terminar de pasar por paraemtro todos los valores de los distintos parametros
        # tanto dentro de esta pagina, como main, como simular, como el vector
    def simular(self):
        tiempo_sim = self.entrada_tiempo_sim.value()
        j = self.entrada_j.value()
        i = self.entrada_i.value()
        a_c = self.entrada_a_c.value()
        b_c = self.entrada_b_c.value()
        a_lc = self.entrada_a_lc.value()
        b_lc = self.entrada_b_lc.value()
        x = self.entrada_x.value()
        a_dc = self.entrada_a_dc.value()
        b_dc = self.entrada_b_dc.value()
        c_dc = self.entrada_c_dc.value()

        self.callback(tiempo_sim, j, i, a_c, b_c,
                      a_lc, b_lc, x, a_dc, b_dc, c_dc)

    def _actualizar_min_b_c(self):
        """Cuando cambia A, B debe ser ≥ A + 1."""
        nuevo_min = self.entrada_a_c.value() + 0.01
        self.entrada_b_c.setMinimum(nuevo_min)
        if self.entrada_b_c.value() < nuevo_min:
            self.entrada_b_c.setValue(nuevo_min)

    def _actualizar_min_b_lc(self):
        """Cuando cambia A, B debe ser ≥ A + 1."""
        nuevo_min = self.entrada_a_lc.value() + 0.01
        self.entrada_b_lc.setMinimum(nuevo_min)
        if self.entrada_b_lc.value() < nuevo_min:
            self.entrada_b_lc.setValue(nuevo_min)
