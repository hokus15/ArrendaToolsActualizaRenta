from decimal import ROUND_HALF_UP, Decimal

from arrendatools.rent_update.base import (
    RentUpdateInput,
    RentUpdateMethod,
    RentUpdateResult,
)
from arrendatools.rent_update.date_utils import DateUtils
from arrendatools.rent_update.strategies.ipc import IpcUpdate


class IpcThenPercentageUpdate(RentUpdateMethod):
    """Actualizacion basada en IPC y despues porcentaje."""

    def calculate(
        self,
        inputs: RentUpdateInput,
    ) -> RentUpdateResult:
        if inputs.year_start is None:
            raise ValueError("Year start is required.")
        if inputs.month is None:
            raise ValueError("Month is required.")
        if inputs.year_end is None:
            raise ValueError("Year end is required.")
        if (inputs.year_start < 1954) or (
            inputs.year_start == 1954 and inputs.month < 3
        ):
            raise ValueError("IPC data is only available from March 1954 onward.")
        if inputs.data is None:
            raise ValueError("Field 'data' is required.")
        if not (Decimal("-1.0") <= inputs.data <= Decimal("1.0")):
            raise ValueError(
                "Data must be a percentage between -1 (-100%) and 1 (100%)."
            )

        amount = Decimal(inputs.amount).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
        ipc_data = IpcUpdate().calculate(
            RentUpdateInput(
                amount=amount,
                month=inputs.month,
                year_start=inputs.year_start,
                year_end=inputs.year_end,
            )
        )
        percentage_delta = (ipc_data.updated_amount * inputs.data).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
        updated_amount = (ipc_data.updated_amount + percentage_delta).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
        variation_rate = ((updated_amount / amount) - Decimal(1)).quantize(
            Decimal("0.001"), rounding=ROUND_HALF_UP
        )
        return RentUpdateResult(
            amount=amount,
            month=DateUtils.month_name_es(inputs.month),
            data=inputs.data,
            year_start=inputs.year_start,
            year_end=inputs.year_end,
            index_start=ipc_data.index_start,
            index_end=ipc_data.index_end,
            updated_amount=updated_amount,
            variation_rate=variation_rate,
        )
