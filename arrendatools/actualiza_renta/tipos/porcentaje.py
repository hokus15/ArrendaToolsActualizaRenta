from decimal import Decimal, ROUND_HALF_UP
from arrendatools.actualiza_renta.actualizacion_renta import ActualizacionRenta


class Porcentaje(ActualizacionRenta):
    """Implementación de actualización por porcentaje."""

    def calcular(
        self,
        cantidad: Decimal,
        dato: Decimal = None,
        mes: int = None,
        anyo_inicial: int = None,
        anyo_final: int = None,
    ) -> dict:
        self.validar_datos(cantidad, dato, mes, anyo_inicial, anyo_final)
        cantidad = Decimal(cantidad)  # Convertir explícitamente a Decimal
        cantidad_actualizada = cantidad + (cantidad * Decimal(dato)).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
        return {
            "cantidad": cantidad,
            "dato": dato,
            "cantidad_actualizada": cantidad_actualizada,
            "tasa_variacion": dato,
        }

    def validar_datos(
        self,
        cantidad: Decimal,
        dato: Decimal = None,
        mes: int = None,
        anyo_inicial: int = None,
        anyo_final: int = None,
    ) -> None:
        """Valida los datos de entrada."""
        super().validar_datos(cantidad, dato, mes, anyo_inicial, anyo_final)
        if dato is None:
            raise ValueError("Debes proporcionar el campo 'dato'.")
        if not (Decimal("-1.0") <= dato <= Decimal("1.0")):
            raise ValueError(
                "El dato debe ser un porcentaje entre -1 (-100%) y 1 (100%)."
            )
        return None
