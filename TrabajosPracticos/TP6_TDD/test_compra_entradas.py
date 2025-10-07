import pytest
from datetime import date, timedelta
from entradas import (
    comprar_entradas,
    ParqueCerradoError,
    PagoInvalidoError,
    CantidadInvalidaError,
    FechaInvalidaError,
)
from feriados import es_feriado

# --- Variables de apoyo ---
hoy = date.today()
dia_disponible = hoy + timedelta(days=2)
dia_cerrado = hoy + timedelta(days=5)

def test_compra_exitosa_con_multiples_edades_y_calculo_de_precio():
    """
    Simula una compra completa y válida, verificando que el monto final
    sea el correcto aplicando todas las reglas de descuento y precios.
    - 1 adulto (100%)
    - 1 niño (50%)
    - 1 senior (50%)
    - 1 infante (Gratis)
    Total esperado: $10,000 (VIP) + $5,000 (Niño VIP) + $5,000 (Senior VIP) + $0 (Infante) = $20,000
    """
    fecha_valida = date.today() + timedelta(days=15)
    edades = [30, 10, 65, 2]  # Adulto, Niño, Senior, Infante
    
    resultado = comprar_entradas(
        fecha_visita=fecha_valida,
        cantidad=len(edades),
        edades=edades,
        tipo_pase="VIP",
        forma_pago="MercadoPago"
    )
    
    assert resultado["status"] == "confirmado"
    assert resultado["monto_total"] == 20000


def test_falla_por_fecha_fuera_de_rango():
    """
    Verifica que el sistema rechace las compras para fechas pasadas
    o para más de 30 días en el futuro.
    """
    # Caso 1: Fecha pasada
    with pytest.raises(FechaInvalidaError, match="no puede ser en el pasado"):
        comprar_entradas(
            fecha_visita=date.today() - timedelta(days=1),
            cantidad=1,
            edades=[30],
            tipo_pase="Regular",
            forma_pago="MercadoPago"
        )
        
    # Caso 2: Fecha muy lejana
    with pytest.raises(FechaInvalidaError):
        comprar_entradas(
            fecha_visita=date.today() + timedelta(days=32),
            cantidad=1,
            edades=[30],
            tipo_pase="Regular",
            forma_pago="MercadoPago"
        )


def test_falla_si_parque_esta_cerrado():
    """Prueba que el sistema levanta un error si la fecha es un lunes."""
    hoy = date.today()
    proximo_lunes = hoy + timedelta(days=(7 - hoy.weekday()))
    
    with pytest.raises(ParqueCerradoError):
        comprar_entradas(proximo_lunes, 1, [30], "Regular", "MercadoPago")


def test_falla_por_exceder_cantidad_maxima():
    """Prueba que no se pueden comprar más de 10 entradas."""
    with pytest.raises(CantidadInvalidaError):
        comprar_entradas(
            fecha_visita=date.today(),
            cantidad=11,
            edades=[25] * 11,
            tipo_pase="Regular",
            forma_pago="MercadoPago"
        )


def test_sin_forma_pago():
    """Verifica que se levante error si no se proporciona forma de pago."""
    with pytest.raises(PagoInvalidoError):
        comprar_entradas(
            fecha_visita=dia_disponible,
            cantidad=2,
            edades=[20, 21],
            tipo_pase="Regular",
            forma_pago=None,
        )


def test_fecha_cerrado():
    """Verifica que la fecha marcada como cerrada levante error."""
    with pytest.raises(ParqueCerradoError):
        comprar_entradas(
            fecha_visita=dia_cerrado,
            cantidad=2,
            edades=[18, 19],
            tipo_pase="Regular",
            forma_pago="MercadoPago",
        )


def test_cantidad_mayor_10():
    """Verifica que no se puedan comprar más de 10 entradas."""
    with pytest.raises(CantidadInvalidaError):
        comprar_entradas(
            fecha_visita=dia_disponible,
            cantidad=11,
            edades=[25] * 11,
            tipo_pase="Regular",
            forma_pago="MercadoPago",
        )
        
def test_no_se_puede_comprar_en_feriados_nacionales():
    """
    Verifica que el sistema rechace compras en feriados nacionales argentinos.
    Usa el módulo 'feriados.py' con la librería 'holidays'.
    """
    # Seleccionamos feriados seguros
    feriados = [
        date(2025, 1, 1),   # Año Nuevo
        date(2025, 5, 25),  # Revolución de Mayo
        date(2025, 12, 25), # Navidad
    ]

    for f in feriados:
        assert es_feriado(f), f"{f} debería ser feriado en Argentina"

        # Validamos que el sistema no permita la compra
        with pytest.raises(ParqueCerradoError, match="feriado"):
            comprar_entradas(
                fecha_visita=f,
                cantidad=2,
                edades=[25, 30],
                tipo_pase="Regular",
                forma_pago="MercadoPago",
            )
