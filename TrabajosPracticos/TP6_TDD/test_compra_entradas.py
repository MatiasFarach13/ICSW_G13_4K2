import pytest
from datetime import date, timedelta
from entradas import comprar_entradas, ParqueCerradoError, PagoInvalidoError, CantidadInvalidaError

hoy = date.today()
dia_disponible = hoy + timedelta(days=2)
dia_cerrado = hoy + timedelta(days=5)


def test_compra_exitosa():
    entradas = comprar_entradas(
        fecha_visita=dia_disponible,
        cantidad=3,
        edades=[25, 30, 40],
        tipo_pase="General",
        forma_pago="MercadoPago",
    )
    assert entradas["status"] == "confirmado"
    assert "email" in entradas


def test_sin_forma_pago():
    with pytest.raises(PagoInvalidoError):
        comprar_entradas(
            fecha_visita=dia_disponible,
            cantidad=2,
            edades=[20, 21],
            tipo_pase="General",
            forma_pago=None,
        )


def test_fecha_cerrado():
    with pytest.raises(ParqueCerradoError):
        comprar_entradas(
            fecha_visita=dia_cerrado,
            cantidad=2,
            edades=[18, 19],
            tipo_pase="General",
            forma_pago="MercadoPago",
        )


def test_cantidad_mayor_10():
    with pytest.raises(CantidadInvalidaError):
        comprar_entradas(
            fecha_visita=dia_disponible,
            cantidad=11,
            edades=[25] * 11,
            tipo_pase="General",
            forma_pago="MercadoPago",
        )
