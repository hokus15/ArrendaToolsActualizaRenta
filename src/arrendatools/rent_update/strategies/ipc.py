import logging
from datetime import date
from decimal import ROUND_HALF_UP, Decimal

from arrendatools.rent_update.base import (
    RentUpdateInput,
    RentUpdateMethod,
    RentUpdateResult,
)
from arrendatools.rent_update.date_utils import DateUtils
from arrendatools.rent_update.ine_client import IneClient
from arrendatools.rent_update.strategies.ipc_data import (
    COEFFICIENTS_LAU_BASE_2021,
    IPC_TABLE_BASE_1992,
)


class IpcUpdate(RentUpdateMethod):
    """Actualizacion de renta basada en IPC."""

    # IPC series: base 2025.
    _SERIES_IPC = "IPC290751"

    def _fetch_ipc(self, year: int, month: int) -> Decimal:
        """Obtiene el IPC del INE para el ano y mes indicado."""
        query_date = date(year, month, 1)
        payload = IneClient.fetch_series_data(query_date, query_date, self._SERIES_IPC)
        if len(payload.get("Data", [])) > 0:
            return Decimal(payload["Data"][0]["Valor"])
        raise ValueError(
            "Rent not updated: Could not fetch IPC data for "
            f"{DateUtils.month_name_es(month)} {year}."
        )

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

        amount = Decimal(inputs.amount).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
        dividend = Decimal(0)
        divisor = Decimal(0)
        try:
            if inputs.year_start < 2002 and inputs.year_end >= 2002:
                index_ipc = self._fetch_ipc(inputs.year_end, inputs.month)
                if index_ipc is None or index_ipc.is_nan():
                    raise ValueError(
                        "Rent not updated: Could not fetch IPC data for "
                        f"{DateUtils.month_name_es(inputs.month)} {inputs.year_end}."
                    )
                # Cross-base update: before 2002 to 2002+.
                dividend = (
                    index_ipc * Decimal(COEFFICIENTS_LAU_BASE_2021[inputs.month - 1])
                ).quantize(Decimal("0.001"), rounding=ROUND_HALF_UP)

                divisor = Decimal(
                    IPC_TABLE_BASE_1992[inputs.year_start][inputs.month - 1]
                ).quantize(Decimal("0.001"), rounding=ROUND_HALF_UP)

            elif inputs.year_start < 2002 and inputs.year_end < 2002:
                # Both dates in pre-2002 base.
                dividend = Decimal(
                    IPC_TABLE_BASE_1992[inputs.year_end][inputs.month - 1]
                ).quantize(Decimal("0.001"), rounding=ROUND_HALF_UP)

                divisor = Decimal(
                    IPC_TABLE_BASE_1992[inputs.year_start][inputs.month - 1]
                ).quantize(Decimal("0.001"), rounding=ROUND_HALF_UP)

            else:
                # Both dates in 2002+ base.
                index_ipc = self._fetch_ipc(inputs.year_end, inputs.month)
                if index_ipc is None or index_ipc.is_nan():
                    raise ValueError(
                        "Rent not updated: Could not fetch IPC data for "
                        f"{DateUtils.month_name_es(inputs.month)} {inputs.year_end}."
                    )
                dividend = index_ipc.quantize(Decimal("0.001"), rounding=ROUND_HALF_UP)
                index_ipc = self._fetch_ipc(inputs.year_start, inputs.month)
                if index_ipc is None or index_ipc.is_nan():
                    raise ValueError(
                        "Rent not updated: Could not fetch IPC data for "
                        f"{DateUtils.month_name_es(inputs.month)} {inputs.year_start}."
                    )
                divisor = index_ipc.quantize(Decimal("0.001"), rounding=ROUND_HALF_UP)
        except ConnectionError as err:
            logging.getLogger(__name__).error("INE IPC fetch failed: %s", err)
            raise

        # INE rounding: compute (dividend / divisor - 1) and round to 3 decimals.
        variation_rate = ((dividend / divisor) - Decimal(1)).quantize(
            Decimal("0.001"), rounding=ROUND_HALF_UP
        )

        updated_amount = (amount + (amount * variation_rate)).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )

        return RentUpdateResult(
            amount=amount,
            month=DateUtils.month_name_es(inputs.month),
            year_start=inputs.year_start,
            year_end=inputs.year_end,
            index_start=divisor,
            index_end=dividend,
            updated_amount=updated_amount,
            variation_rate=variation_rate,
        )
