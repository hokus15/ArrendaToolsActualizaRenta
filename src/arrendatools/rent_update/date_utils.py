class DateUtils:
    """Utilidades para manejo de fechas."""

    @staticmethod
    def month_name_es(month: int) -> str:
        """Convierte un numero de mes en su nombre en espanol."""
        months_es = [
            "enero",
            "febrero",
            "marzo",
            "abril",
            "mayo",
            "junio",
            "julio",
            "agosto",
            "septiembre",
            "octubre",
            "noviembre",
            "diciembre",
        ]
        if 1 <= month <= 12:
            return months_es[month - 1]
        raise ValueError(
            f"Month {month} is invalid. It must be between 1 and 12."
        )
