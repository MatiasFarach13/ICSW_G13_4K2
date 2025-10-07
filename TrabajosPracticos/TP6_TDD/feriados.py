# feriados.py
from datetime import date, timedelta
import holidays

class FeriadoError(Exception):
    """Excepción para indicar que la fecha es feriado o no permitida para compra."""
    pass


def obtener_feriados_argentina(anio: int = None):
    return holidays.CountryHoliday("AR", years=anio)


def es_feriado(fecha: date) -> bool:

    feriados = obtener_feriados_argentina(fecha.year)

    # Caso 1: es feriado directo (ej. 25/12)
    if fecha in feriados:
        return True

    # Caso 2: es lunes posterior a un feriado en domingo
    dia_anterior = fecha - timedelta(days=1)
    if dia_anterior in feriados and dia_anterior.weekday() == 6:
        return True

    return False


def assert_no_feriado(fecha: date):
    """
    Lanza FeriadoError si la fecha es feriado o feriado trasladado a lunes.
    """
    if es_feriado(fecha):
        raise FeriadoError(f"La fecha {fecha} es feriado o día no habilitado para la compra.")


if __name__ == "__main__":
    # --- Prueba rápida ---
    import calendar
    hoy = date.today()
    feriados = obtener_feriados_argentina(hoy.year)

    print("Feriados del año actual:")
    for f in sorted(feriados.keys()):
        print(f"{f} - {feriados[f]}")

    # Ejemplo: verificar casos típicos
    print()
    test_dates = [
        date(hoy.year, 1, 1),   # Año Nuevo
        date(hoy.year, 12, 25), # Navidad
        date(hoy.year, 6, 20),  # Paso a la Inmortalidad de Belgrano
        date(hoy.year, 10, 13), # Algún lunes trasladado
    ]
    for d in test_dates:
        print(f"{d} ({calendar.day_name[d.weekday()]}): {'FERIADO' if es_feriado(d) else 'NO'}")
