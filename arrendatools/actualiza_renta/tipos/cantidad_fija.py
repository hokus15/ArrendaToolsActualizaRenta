from decimal import Decimal, ROUND_HALF_UP
from arrendatools.actualiza_renta.actualizacion_renta import ActualizacionRenta


class CantidadFija(ActualizacionRenta):
    """Implementación de actualización por cantidad fija."""

    def calcular(
        self,
        cantidad: Decimal,
        dato: Decimal = None,
        mes: int = None,
        anyo_inicial: int = None,
        anyo_final: int = None,
    ) -> dict:
        self.validar_datos(cantidad, dato, mes, anyo_inicial, anyo_final)
        # Convertir explícitamente a Decimal y redondear a dos decimales
        cantidad = Decimal(cantidad).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
        cantidad_actualizada = cantidad + Decimal(dato)
        result = {
            "cantidad": cantidad,
            "dato": dato,
            "cantidad_actualizada": cantidad_actualizada,
        }
        return result

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
        return None
