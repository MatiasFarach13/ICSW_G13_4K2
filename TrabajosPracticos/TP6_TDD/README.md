# TP6 - Test Driven Development (TDD)

## Descripción
Sistema de compra de entradas para un parque temático desarrollado aplicando metodología TDD (Test Driven Development). El proyecto incluye validaciones de negocio, cálculo de precios con descuentos por edad, y una interfaz gráfica desarrollada con PyQt5.

## Características del Sistema

### Reglas de Negocio
- **Tipos de pase**: VIP ($10,000) y Regular ($5,000)
- **Descuentos por edad**:
  - Infantes (≤3 años): Gratis
  - Niños (4-15 años): 50% descuento
  - Seniors (≥60 años): 50% descuento
- **Restricciones**:
  - Máximo 10 entradas por compra
  - Compra hasta 30 días de anticipación
  - Parque cerrado los lunes y feriados (25/12, 1/1)

### Funcionalidades
- Validación de fechas de visita
- Cálculo automático de precios con descuentos
- Validación de formas de pago
- Interfaz gráfica intuitiva
- Sistema de confirmación por email

## Estructura del Proyecto

```
TP6_TDD/
├── src/
│   ├── entradas.py          # Lógica principal del sistema
│   ├── main.py             # Aplicación principal con interfaz gráfica
│   ├── core/
│   │   └── utilidades.py   # Utilidades y estilos
│   └── paginas/
│       ├── PaginaInicio.py
│       ├── PaginaComprar.py
│       ├── PaginaConfirmacion.py
│       └── ...
├── tests/
│   └── test_compra_entradas.py  # Suite completa de pruebas
├── recursos/
│   ├── estilo_claro.qss    # Estilos CSS para tema claro
│   └── estilo_oscuro.qss   # Estilos CSS para tema oscuro
├── requirements.txt        # Dependencias del proyecto
└── README.md              # Este archivo
```

## Requisitos

- Python 3.8+
- PyQt5
- pytest (para ejecutar las pruebas)

## Instalación y Configuración

1. **Crear entorno virtual**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # En Linux/Mac
   # venv\Scripts\activate  # En Windows
   ```

2. **Instalar dependencias**:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   pip install pytest
   ```

## Uso

### Ejecutar la aplicación
```bash
# Activar entorno virtual
source venv/bin/activate

# Ejecutar la aplicación
python src/main.py
```

### Ejecutar las pruebas
```bash
# Desde la raíz del proyecto
pytest tests/ -v

# O usando PYTHONPATH para las importaciones
PYTHONPATH=src pytest tests/ -v
```

## Metodología TDD

Este proyecto fue desarrollado siguiendo la metodología **Test Driven Development**:

1. **Red**: Escribir una prueba que falle
2. **Green**: Escribir el código mínimo para que pase
3. **Refactor**: Mejorar el código manteniendo las pruebas verdes

### Cobertura de Pruebas

Las pruebas cubren:
- ✅ Casos de compra exitosa
- ✅ Validaciones de fecha (pasado, futuro lejano, lunes, feriados)
- ✅ Validaciones de cantidad (límites 1-10)
- ✅ Validaciones de pago
- ✅ Cálculo correcto de precios con descuentos
- ✅ Manejo de excepciones personalizadas

## Excepciones del Sistema

- `ParqueError`: Base para errores del dominio
- `ParqueCerradoError`: Parque cerrado por día o feriado
- `PagoInvalidoError`: Forma de pago inválida
- `CantidadInvalidaError`: Cantidad de entradas fuera de rango
- `FechaInvalidaError`: Fecha de visita inválida

## Contribución

Este proyecto forma parte del Trabajo Práctico 6 de la materia **Ingeniería y Calidad de Software**.

### Equipo de Desarrollo
- Grupo 13 - 4K2

## Notas del Desarrollo

- Se aplicó TDD de forma estricta: todas las funcionalidades fueron desarrolladas primero escribiendo las pruebas.
- La interfaz gráfica utiliza PyQt5 con soporte para temas claro y oscuro.
- El sistema simula la generación de emails de confirmación.
- Se implementaron validaciones robustas siguiendo las reglas de negocio especificadas.

---

*Trabajo Práctico desarrollado para la materia Ingeniería y Calidad de Software - Universidad Tecnológica Nacional*