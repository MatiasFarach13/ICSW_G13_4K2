import pytest
from datetime import date, timedelta
from src.clases.gestorCompraEntradas import (
    GestorCompraEntradas,
    ParqueCerradoError,
    PagoInvalidoError,
    CantidadInvalidaError,
    FechaInvalidaError,
    EmailInvalidoError,
    DIAS_ANTICIPACION_MAX
)
from unittest.mock import patch, Mock

hoy = date.today()

def proxima_fecha_valida():
    hoy = date.today()
    dias = 1
    while True:
        f = hoy + timedelta(days=dias)
        if f.weekday() != 0 and (f.month, f.day) not in [(12, 25), (1, 1)]:
            return f
        dias += 1

gestor = GestorCompraEntradas()

# ---------------------------------------------
# ✅ Casos exitosos
# ---------------------------------------------
def test_compra_hoy_parcheado():
    fecha_simulada = date(2025, 10, 8)
    edades = [25, 10, 70, 2]
    tipos = ["VIP", "Regular", "VIP", "Regular"]
    ## creamos los objetos entrada
    entradas = gestor.crear_entrada(tipos, fecha_simulada, edades)
    
    
    with patch("src.clases.gestorCompraEntradas.date") as mock_date:
        mock_date.today.return_value = fecha_simulada
        mock_date.side_effect = lambda *args, **kwargs: date(*args, **kwargs)
        if fecha_simulada.weekday() == 0 or (fecha_simulada.month, fecha_simulada.day) in [(12, 25), (1, 1)]:
            with pytest.raises(ParqueCerradoError):
                gestor.comprar_entradas(
                    fecha_visita=fecha_simulada,
                    edades=edades,
                    entradas=entradas,
                    forma_pago="Tarjeta",
                    email="valido@example.com"
                )
        else:
            resultado = gestor.comprar_entradas(
                fecha_visita=fecha_simulada,
                edades=edades,
                entradas=entradas,
                forma_pago="Tarjeta",
                email="valido@example.com"
            )
            assert resultado["status"] == "confirmado"
            assert "email" in resultado
            assert resultado["cantidad"] == 4
            assert resultado["total_pagado"] == 10000 + 2500 + 5000 + 0

def test_compra_exitosa_con_fecha_valida_parcheada():
    fecha_simulada = date(2025, 10, 7)
    edades = [25, 10]
    tipos_pase=["VIP", "Regular"]
    # creacion de entradas
    entradas = gestor.crear_entrada(tipos_pase, fecha_simulada, edades)
    with patch("src.clases.gestorCompraEntradas.date") as mock_date:
        mock_date.today.return_value = fecha_simulada
        mock_date.side_effect = lambda *args, **kwargs: date(*args, **kwargs)
        dias_hasta_abierto = 1
        while (fecha_simulada + timedelta(days=dias_hasta_abierto)).weekday() == 0:
            dias_hasta_abierto += 1
        fecha_abierta = fecha_simulada + timedelta(days=dias_hasta_abierto)
        resultado = gestor.comprar_entradas(
            fecha_visita=fecha_abierta,
            edades=edades,
            entradas=entradas,
            forma_pago="Tarjeta",
            email="valido@example.com"
        )
        assert resultado["status"] == "confirmado"
        assert "email" in resultado
        assert resultado["cantidad"] == 2
        assert resultado["total_pagado"] == 10000 + 2500

def test_compra_con_tipos_combinados_y_varias_edades_parcheada():
    fecha_simulada = date(2025, 10, 8)
    edades = [10, 30, 65]
    tipos = ["Regular", "VIP", "Regular"]
    # creacion de entradas
    entradas = gestor.crear_entrada(tipos, fecha_simulada, edades)
    with patch("src.clases.gestorCompraEntradas.date") as mock_date:
        mock_date.today.return_value = fecha_simulada
        mock_date.side_effect = lambda *args, **kwargs: date(*args, **kwargs)
        fecha_valida = date(2025, 10, 9)
        resultado = gestor.comprar_entradas(
            fecha_visita=fecha_valida,
            edades=edades,
            entradas=entradas,
            forma_pago="Tarjeta",
            email="valido@example.com"
        )
        assert resultado["status"] == "confirmado"
        assert "email" in resultado
        assert resultado["cantidad"] == 3
        assert resultado["total_pagado"] == 2500 + 10000 + 2500

def test_dos_compras_en_el_mismo_dia():
    edades = [25] * 10
    tipos = ["Regular"] * 10
    fecha_visita = proxima_fecha_valida()
    # creacion de entradas
    entradas = gestor.crear_entrada(tipos, fecha_visita, edades)
    compra1 = gestor.comprar_entradas(fecha_visita, edades, entradas, "Tarjeta", email="valido@example.com")
    compra2 = gestor.comprar_entradas(fecha_visita, edades, entradas, "Tarjeta", email="valido@example.com")
    assert compra1["status"] == compra2["status"] == "confirmado"
    assert compra1["cantidad"] == compra2["cantidad"] == 10

def test_envio_email_confirmacion():
    mock_enviar = Mock()
    edades = [30, 10]
    tipos = ["VIP", "Regular"]
    fecha_visita = proxima_fecha_valida()
    # creacion de entradas
    entradas = gestor.crear_entrada(tipos, fecha_visita, edades)
    resultado = gestor.comprar_entradas(
        fecha_visita=fecha_visita,
        edades=edades,
        entradas=entradas,
        forma_pago="Tarjeta",
        email="valido@example.com",
        enviar_email=mock_enviar
    )
    mock_enviar.assert_called_once_with("valido@example.com", resultado)

# ---------------------------------------------
# ❌ Casos que deben fallar
# ---------------------------------------------
def test_compra_dia_anterior():
    tipos_pase = ["Regular"]
    fecha_simulada = hoy - timedelta(days=1)
    edades = [30]
    # creacion de entradas
    entradas = gestor.crear_entrada(tipos_pase, fecha_simulada, edades)
    with pytest.raises(FechaInvalidaError):
        gestor.comprar_entradas(
            fecha_visita=fecha_simulada,
            edades=edades,
            entradas=entradas,
            forma_pago="Tarjeta",
            email="valido@example.com"
        )

def test_compra_mas_de_30_dias():
    tipos_pase = ["Regular"]
    fecha_visita = hoy + timedelta(days=31)
    edades = [30]
    # creacion de entradas
    entradas = gestor.crear_entrada(tipos_pase, fecha_visita, [30])
    with pytest.raises(FechaInvalidaError):
        gestor.comprar_entradas(
            fecha_visita=fecha_visita,
            edades=edades,
            entradas=entradas,
            forma_pago="Tarjeta",
            email="valido@example.com"
        )

def test_compra_para_feriado():
    fecha_compra = date(2025, 12, 10)
    fecha_visita = date(2025, 12, 25)
    tipos_pase = ["VIP"]
    edades = [25]
    # creacion de entradas
    entradas = gestor.crear_entrada(tipos_pase, fecha_visita, edades)
    with patch("src.clases.gestorCompraEntradas.date") as mock_date:
        mock_date.today.return_value = fecha_compra
        mock_date.side_effect = lambda *args, **kwargs: date(*args, **kwargs)
        with pytest.raises(ParqueCerradoError):
            gestor.comprar_entradas(
                fecha_visita=fecha_visita,
                edades=edades,
                entradas=entradas,
                forma_pago="Tarjeta",
                email="valido@example.com"
            )

def test_compra_para_lunes():
    fecha_compra = date(2025, 12, 10)
    fecha_visita = date(2025, 12, 15)
    tipos_pase = ["VIP"]
    edades = [25]
    # creacion de entradas
    entradas = gestor.crear_entrada(tipos_pase, fecha_visita, edades)
    with patch("src.clases.gestorCompraEntradas.date") as mock_date:
        mock_date.today.return_value = fecha_compra
        mock_date.side_effect = lambda *args, **kwargs: date(*args, **kwargs)
        with pytest.raises(ParqueCerradoError):
            gestor.comprar_entradas(
                fecha_visita=fecha_visita,
                edades=edades,
                entradas=entradas,
                forma_pago="Tarjeta",
                email="valido@example.com"
            )

def test_compra_mas_de_10_entradas():
    tipos_pase = ["Regular"] * 11
    fechas_visita = proxima_fecha_valida()
    edades = [25] * 11
    # creacion de entradas
    entradas = gestor.crear_entrada(tipos_pase, fechas_visita, edades)
    with pytest.raises(CantidadInvalidaError):
        gestor.comprar_entradas(
            fecha_visita=fechas_visita,
            edades=edades,
            entradas=entradas,
            forma_pago="Tarjeta",
            email="valido@example.com"
        )

def test_sin_forma_pago():
    fecha_visita = proxima_fecha_valida()
    tipos_pase = ["Regular", "VIP"]
    edades = [20, 21]
    # creacion de entradas
    entradas = gestor.crear_entrada(tipos_pase, fecha_visita, edades)
    with pytest.raises(PagoInvalidoError):
        gestor.comprar_entradas(
            fecha_visita=fecha_visita,
            edades=edades,
            entradas=entradas,
            forma_pago=None,
            email="valido@example.com"
        )

def test_compra_email_invalido():
    fecha_visita = proxima_fecha_valida()
    tipos_pase = ["Regular", "VIP"]
    edades = [20, 21]
    # creacion de entradas
    entradas = gestor.crear_entrada(tipos_pase, fecha_visita, edades)
    with pytest.raises(EmailInvalidoError):
        gestor.comprar_entradas(
            fecha_visita=fecha_visita,
            edades=edades,
            entradas=entradas,
            forma_pago="Tarjeta",
            email="email_invalido"
        )

def test_compra_email_vacio():
    fecha_visita = proxima_fecha_valida()
    tipos_pase = ["Regular", "VIP"]
    edades = [20, 21]
    # creacion de entradas
    entradas = gestor.crear_entrada(tipos_pase, fecha_visita, edades)
    with pytest.raises(EmailInvalidoError):
        gestor.comprar_entradas(
            fecha_visita=fecha_visita,
            edades=edades,
            entradas=entradas,
            forma_pago="Tarjeta",
            email=""
        )

def test_compra_email_sin_arroba():
    with pytest.raises(EmailInvalidoError):
        fecha_visita = proxima_fecha_valida()
        tipos_pase = ["Regular", "VIP"]
        edades = [20, 21]
        # creacion de entradas
        entradas = gestor.crear_entrada(tipos_pase, fecha_visita, edades)
        gestor.comprar_entradas(
            fecha_visita=fecha_visita,
            edades=edades,
            entradas=entradas,
            forma_pago="Tarjeta",
            email="email.invalido.com"
        )
