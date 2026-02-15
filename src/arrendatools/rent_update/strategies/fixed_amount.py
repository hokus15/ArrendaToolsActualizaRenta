from decimal import Decimal, ROUND_HALF_UP

from arrendatools.rent_update.base import (
    RentUpdateInput,
    RentUpdateMethod,
    RentUpdateResult,
)


class FixedAmountUpdate(RentUpdateMethod):
    """Implementacion de actualizacion por cantidad fija."""

    def calculate(
        self,
        inputs: RentUpdateInput,
    ) -> RentUpdateResult:
        if inputs.data is None:
            raise ValueError("Field 'data' is required.")
        amount = Decimal(inputs.amount).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
        updated_amount = amount + Decimal(inputs.data)
        return RentUpdateResult(
            amount=amount,
            data=inputs.data,
            updated_amount=updated_amount,
        )
