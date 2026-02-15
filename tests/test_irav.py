import unittest
from unittest.mock import patch
from decimal import Decimal

from arrendatools.rent_update.base import RentUpdateInput, RentUpdateResult
from arrendatools.rent_update.factory import RentUpdateFactory
from arrendatools.rent_update.strategies.irav import IravUpdate


class TestIravUpdate(unittest.TestCase):
    def setUp(self):
        self.rent_update = RentUpdateFactory.create("irav")

    def test_calculate_raises_value_error_for_missing_start_year(self):
        with self.assertRaises(ValueError) as context:
            self.rent_update.calculate(
                RentUpdateInput(amount=Decimal("1000.00"), month=11)
            )
        self.assertEqual(
            str(context.exception),
            "Year start is required.",
        )

    def test_calculate_raises_value_error_for_missing_month(self):
        with self.assertRaises(ValueError) as context:
            self.rent_update.calculate(
                RentUpdateInput(amount=Decimal("1000.00"), year_start=2025)
            )
        self.assertEqual(str(context.exception), "Month is required.")

    def test_calculate_raises_value_error_for_invalid_start_year(self):
        with self.assertRaises(ValueError) as context:
            self.rent_update.calculate(
                RentUpdateInput(
                    amount=Decimal("1000.00"), month=10, year_start=2023
                )
            )
        self.assertEqual(
            str(context.exception),
            "IRAV data is only available from November 2024 onward.",
        )

    def test_calculate_irav(self):
        result = self.rent_update.calculate(
            RentUpdateInput(
                amount=Decimal("1000.00"),
                month=11,
                year_start=2024,
            )
        )

        expected = RentUpdateResult(
            amount=Decimal("1000.00"),
            updated_amount=Decimal("1022.00"),
            year_start=2024,
            month="noviembre",
            variation_rate=Decimal("0.022"),
        )
        self.assertEqual(result, expected)

    @patch.object(IravUpdate, "_fetch_irav", return_value=Decimal("0.05"))
    def test_calculate_success(self, mock_obtener_irav):
        result = self.rent_update.calculate(
            RentUpdateInput(
                amount=Decimal("1000.00"),
                month=11,
                year_start=2025,
                year_end=2026,
            )
        )
        expected = RentUpdateResult(
            amount=Decimal("1000.00"),
            updated_amount=Decimal("1050.00"),
            year_start=2025,
            month="noviembre",
            variation_rate=Decimal("0.05"),
        )
        self.assertEqual(result, expected)

    @patch.object(IravUpdate, "_fetch_irav", return_value=None)
    def test_calculate_raises_value_error_for_invalid_data(
        self, mock_obtener_irav
    ):
        with self.assertRaises(ValueError) as context:
            self.rent_update.calculate(
                RentUpdateInput(
                    amount=Decimal("1000.00"),
                    month=11,
                    year_start=2025,
                    year_end=2026,
                )
            )
        self.assertEqual(
            str(context.exception),
            "Rent not updated: Could not fetch IRAV data for noviembre 2025.",
        )


if __name__ == "__main__":
    unittest.main()
