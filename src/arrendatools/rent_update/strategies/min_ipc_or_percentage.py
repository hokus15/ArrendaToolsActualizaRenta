from decimal import Decimal, ROUND_HALF_UP

from arrendatools.rent_update.base import (
    RentUpdateInput,
    RentUpdateMethod,
    RentUpdateResult,
)
from arrendatools.rent_update.date_utils import DateUtils
from arrendatools.rent_update.strategies.ipc import IpcUpdate


class MinIpcOrPercentageUpdate(RentUpdateMethod):
    """Actualizacion basada en el minimo entre IPC y porcentaje."""

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
            raise ValueError(
                "IPC data is only available from March 1954 onward."
            )
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
        ipc_variation = ipc_data.variation_rate
        variation_rate = min(ipc_variation, inputs.data)
        updated_amount = (
            amount + (amount * Decimal(variation_rate))
        ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
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
