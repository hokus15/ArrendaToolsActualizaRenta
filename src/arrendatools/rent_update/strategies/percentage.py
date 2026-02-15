from decimal import Decimal, ROUND_HALF_UP

from arrendatools.rent_update.base import (
    RentUpdateInput,
    RentUpdateMethod,
    RentUpdateResult,
)


class PercentageUpdate(RentUpdateMethod):
    """Implementacion de actualizacion por porcentaje."""

    def calculate(
        self,
        inputs: RentUpdateInput,
    ) -> RentUpdateResult:
        if inputs.data is None:
            raise ValueError("Field 'data' is required.")
        if not (Decimal("-1.0") <= inputs.data <= Decimal("1.0")):
            raise ValueError(
                "Data must be a percentage between -1 (-100%) and 1 (100%)."
            )
        amount = Decimal(inputs.amount).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
        updated_amount = amount + (amount * Decimal(inputs.data)).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
        return RentUpdateResult(
            amount=amount,
            data=inputs.data,
            updated_amount=updated_amount,
            variation_rate=inputs.data,
        )
