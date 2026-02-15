from datetime import date
from decimal import Decimal, ROUND_HALF_UP

from arrendatools.rent_update.base import (
    RentUpdateInput,
    RentUpdateMethod,
    RentUpdateResult,
)
from arrendatools.rent_update.date_utils import DateUtils
from arrendatools.rent_update.ine_client import IneClient


class IravUpdate(RentUpdateMethod):
    """Actualizacion basada en el Indice de Rentas de Alquiler de Viviendas (IRAV)."""

    _SERIES_IRAV = "IRAV1"

    def _fetch_irav(self, year: int, month: int) -> Decimal:
        """Obtiene el IRAV del INE para el ano y mes indicado."""
        query_date = date(year, month, 1)
        payload = IneClient.fetch_series_data(
            query_date, query_date, self._SERIES_IRAV
        )
        if len(payload.get("Data", [])) > 0:
            value = Decimal(payload["Data"][0]["Valor"])
            return (value / Decimal("100")).quantize(
                Decimal("0.001"), rounding=ROUND_HALF_UP
            )
        raise ValueError(
            "Rent not updated: Could not fetch IRAV data for "
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
        if (inputs.year_start < 2024) or (
            inputs.year_start == 2024 and inputs.month < 11
        ):
            raise ValueError(
                "IRAV data is only available from November 2024 onward."
            )
        try:
            amount = Decimal(inputs.amount).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            )
            variation_rate = self._fetch_irav(inputs.year_start, inputs.month)
            if variation_rate is None or variation_rate.is_nan():
                raise ValueError(
                    "Rent not updated: Could not fetch IRAV data for "
                    f"{DateUtils.month_name_es(inputs.month)} {inputs.year_start}."
                )
            updated_amount = (
                amount * (Decimal("1") + variation_rate)
            ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        except ConnectionError as err:
            print(err)
            raise
        return RentUpdateResult(
            amount=amount,
            year_start=inputs.year_start,
            month=DateUtils.month_name_es(inputs.month),
            updated_amount=updated_amount,
            variation_rate=variation_rate,
        )
