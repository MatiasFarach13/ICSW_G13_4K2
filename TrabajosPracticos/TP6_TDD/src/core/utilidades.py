from pathlib import Path
import sys

def _base_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys._MEIPASS) # type: ignore[attr-defined]
    return Path(sys.modules["__main__"].__file__).resolve().parent

def aplicar_estilo(qapp, modo: str = "claro") -> None:
    archivo = "estilo_claro.qss" if modo == "claro" else "estilo_oscuro.qss"
    ruta_qss = _base_dir() / "recursos" / archivo

    try:
        with ruta_qss.open(encoding="utf-8") as f:
            qapp.setStyleSheet(f.read())
    except FileNotFoundError:
        print(f"[WARNING] No se encontró {ruta_qss}")
