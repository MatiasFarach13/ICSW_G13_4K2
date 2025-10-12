import pytest
from datetime import date, timedelta
from src.entradas import (
    comprar_entradas,
    ParqueCerradoError,
    PagoInvalidoError,
    CantidadInvalidaError,
    FechaInvalidaError,
    EmailInvalidoError
)
from unittest.mock import patch, Mock

# --- Variables de apoyo ---
hoy = date.today()

# calcula una fecha proxima valida

def proxima_fecha_valida():
    hoy = date.today()
    dias = 1
    while True:
        f = hoy + timedelta(days=dias)
        if f.weekday() != 0 and (f.month, f.day) not in [(12, 25), (1, 1)]:
            return f
        dias += 1
# ---------------------------------------------
# ✅ Casos exitosos
# ---------------------------------------------
def test_compra_hoy_parcheado():
    """Compra de entradas simulando que hoy es 08/10/2025."""
    fecha_simulada = date(2025, 10, 8)  # "hoy" fijo para el test
    edades = [25, 10, 70, 2]
    tipos = ["VIP", "Regular", "VIP", "Regular"]

    with patch("src.entradas.date") as mock_date:
        mock_date.today.return_value = fecha_simulada
        mock_date.side_effect = lambda *args, **kwargs: date(*args, **kwargs)

        # Comprobamos si hoy sería un día cerrado
        if fecha_simulada.weekday() == 0 or (fecha_simulada.month, fecha_simulada.day) in [(12, 25), (1, 1)]:
            # Debe fallar si intenta comprar para hoy (día cerrado)
            with pytest.raises(ParqueCerradoError):
                comprar_entradas(
                    fecha_visita=fecha_simulada,
                    edades=edades,
                    tipos_pase=tipos,
                    forma_pago="MercadoPago",
                    email="valido@example.com"
                )
        else:
            # Debe poder comprar normalmente
            resultado = comprar_entradas(
                fecha_visita=fecha_simulada,
                edades=edades,
                tipos_pase=tipos,
                forma_pago="MercadoPago",
                email="valido@example.com"
            )

            assert resultado["status"] == "confirmado"
            assert "email" in resultado
            assert resultado["cantidad"] == 4
            assert resultado["total_pagado"] == 10000 + 2500 + 5000 + 0

def test_compra_exitosa_con_fecha_valida_parcheada():
    """Compra válida en un día que el parque está abierto, simulando hoy 07/10/2025."""
    fecha_simulada = date(2025, 10, 7)  # "hoy" fijo para el test

    with patch("src.entradas.date") as mock_date:
        mock_date.today.return_value = fecha_simulada
        mock_date.side_effect = lambda *args, **kwargs: date(*args, **kwargs)

        # Buscamos el próximo día abierto que NO sea lunes
        dias_hasta_abierto = 1  # empezamos desde el día siguiente
        while (fecha_simulada + timedelta(days=dias_hasta_abierto)).weekday() == 0:
            dias_hasta_abierto += 1

        fecha_abierta = fecha_simulada + timedelta(days=dias_hasta_abierto)

        resultado = comprar_entradas(
            fecha_visita=fecha_abierta,
            edades=[25, 10],
            tipos_pase=["VIP", "Regular"],
            forma_pago="MercadoPago",
            email="valido@example.com"
        )

        # Comprobaciones
        assert resultado["status"] == "confirmado"
        assert "email" in resultado
        assert resultado["cantidad"] == 2
        assert resultado["total_pagado"] == 10000 + 2500


def test_compra_con_tipos_combinados_y_varias_edades_parcheada():
    """Compra válida con diferentes tipos y edades, usando fecha fija para test determinista."""
    fecha_simulada = date(2025, 10, 8)  # "hoy" fijo para el test
    edades = [10, 30, 65]
    tipos = ["Regular", "VIP", "Regular"]

    with patch("src.entradas.date") as mock_date:
        mock_date.today.return_value = fecha_simulada
        mock_date.side_effect = lambda *args, **kwargs: date(*args, **kwargs)

        # Elegimos un día abierto fijo (por ejemplo 09/10/2025)
        fecha_valida = date(2025, 10, 9)

        resultado = comprar_entradas(
            fecha_visita=fecha_valida,
            edades=edades,
            tipos_pase=tipos,
            forma_pago="MercadoPago",
            email="valido@example.com"
        )

        # Comprobaciones
        assert resultado["status"] == "confirmado"
        assert "email" in resultado
        assert resultado["cantidad"] == 3
        assert resultado["total_pagado"] == 2500 + 10000 + 2500


def test_dos_compras_en_el_mismo_dia():
    """El límite de 10 entradas es por compra, no por día."""
    edades = [25] * 10
    tipos = ["Regular"] * 10

    compra1 = comprar_entradas(hoy, edades, tipos, "MercadoPago", email="valido@example.com")
    compra2 = comprar_entradas(hoy, edades, tipos, "MercadoPago", email="valido@example.com")

    assert compra1["status"] == compra2["status"] == "confirmado"
    assert compra1["cantidad"] == compra2["cantidad"] == 10

def test_envio_email_confirmacion():
    mock_enviar = Mock()
    edades = [30, 10]
    tipos = ["VIP", "Regular"]
    resultado = comprar_entradas(
        fecha_visita= proxima_fecha_valida(),  # día abierto
        edades=edades,
        tipos_pase=tipos,
        forma_pago="MercadoPago",
        email="valido@example.com",
        enviar_email=mock_enviar
    )
    mock_enviar.assert_called_once_with("valido@example.com", resultado)

# ---------------------------------------------
# ❌ Casos que deben fallar
# ---------------------------------------------
def test_compra_dia_anterior():
    with pytest.raises(FechaInvalidaError):
        comprar_entradas(
            fecha_visita=hoy - timedelta(days=1),
            edades=[30],
            tipos_pase=["Regular"],
            forma_pago="MercadoPago",
            email="valido@example.com"
        )

def test_compra_mas_de_30_dias():
    with pytest.raises(FechaInvalidaError):
        comprar_entradas(
            fecha_visita=hoy + timedelta(days=31),
            edades=[30],
            tipos_pase=["Regular"],
            forma_pago="MercadoPago",
            email="valido@example.com"
        )


def test_compra_para_feriado():
    """Intentar comprar entrada el 10/12/2025 para Navidad (25/12/2025) debe fallar."""
    fecha_compra = date(2025, 12, 10)
    fecha_visita = date(2025, 12, 25)

    with patch("src.entradas.date") as mock_date:
        mock_date.today.return_value = fecha_compra
        mock_date.side_effect = lambda *args, **kwargs: date(*args, **kwargs)

        with pytest.raises(ParqueCerradoError):
            comprar_entradas(
                fecha_visita=fecha_visita,
                edades=[25],
                tipos_pase=["VIP"],
                forma_pago="MercadoPago",
                email="valido@example.com"
            )

def test_compra_para_lunes():
    """Intentar comprar entrada el 10/12/2025 para un lunes (15/12/2025) debe fallar."""
    fecha_compra = date(2025, 12, 10)
    fecha_visita = date(2025, 12, 15)

    with patch("src.entradas.date") as mock_date:
        mock_date.today.return_value = fecha_compra
        mock_date.side_effect = lambda *args, **kwargs: date(*args, **kwargs)

        with pytest.raises(ParqueCerradoError):
            comprar_entradas(
                fecha_visita=fecha_visita,
                edades=[25],
                tipos_pase=["VIP"],
                forma_pago="MercadoPago",
                email="valido@example.com"
            )


def test_compra_mas_de_10_entradas():
    """No se pueden comprar más de 10 entradas en una sola compra."""
    with pytest.raises(CantidadInvalidaError):
        comprar_entradas(
            fecha_visita=proxima_fecha_valida(),
            edades=[25] * 11,
            tipos_pase=["Regular"] * 11,
            forma_pago="MercadoPago",
            email="valido@example.com"
        )


def test_sin_forma_pago():
    """Debe fallar si no se especifica forma de pago."""
    with pytest.raises(PagoInvalidoError):
        comprar_entradas(
            fecha_visita=proxima_fecha_valida(),
            edades=[20, 21],
            tipos_pase=["Regular", "VIP"],
            forma_pago=None,
            email="valido@example.com"
        )

def test_compra_email_invalido():
    """Debe fallar si el formato del email es inválido."""
    with pytest.raises(EmailInvalidoError):
        comprar_entradas(
            fecha_visita=proxima_fecha_valida(),
            edades=[20, 21],
            tipos_pase=["Regular", "VIP"],
            forma_pago="MercadoPago",
            email="email_invalido"  # Formato inválido
        )

def test_compra_email_vacio():
    """Debe fallar si el email está vacío."""
    with pytest.raises(EmailInvalidoError):
        comprar_entradas(
            fecha_visita=proxima_fecha_valida(),
            edades=[20, 21],
            tipos_pase=["Regular", "VIP"],
            forma_pago="MercadoPago",
            email=""
        )

def test_compra_email_sin_arroba():
    """Debe fallar si el email no contiene '@'."""
    with pytest.raises(EmailInvalidoError):
        comprar_entradas(
            fecha_visita=proxima_fecha_valida(),
            edades=[20, 21],
            tipos_pase=["Regular", "VIP"],
            forma_pago="MercadoPago",
            email="email.invalido.com"
        )

