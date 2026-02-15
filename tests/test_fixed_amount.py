import unittest
from decimal import Decimal

from arrendatools.rent_update.base import RentUpdateInput, RentUpdateResult
from arrendatools.rent_update.factory import RentUpdateFactory


class TestFixedAmountUpdate(unittest.TestCase):

    def setUp(self):
        self.rent_update = RentUpdateFactory.create("fixed_amount")

    def test_calculate_valid_inputs(self):
        result = self.rent_update.calculate(
            RentUpdateInput(
                amount=Decimal("100.00"),
                data=Decimal("50.00"),
            )
        )
        expected = RentUpdateResult(
            amount=Decimal("100.00"),
            data=Decimal("50.00"),
            updated_amount=Decimal("150.00"),
        )
        self.assertEqual(result, expected)

    def test_calculate_missing_data(self):
        with self.assertRaises(ValueError) as context:
            self.rent_update.calculate(
                RentUpdateInput(
                    amount=Decimal("100.00"),
                    month=1,
                    year_start=2020,
                    year_end=2021,
                )
            )
        self.assertEqual(
            str(context.exception),
            "Field 'data' is required.",
        )

    def test_calculate_edge_case_month(self):
        result = self.rent_update.calculate(
            RentUpdateInput(
                amount=Decimal("100.00"),
                data=Decimal("50.00"),
                month=12,
                year_start=2020,
                year_end=2021,
            )
        )
        expected = RentUpdateResult(
            amount=Decimal("100.00"),
            data=Decimal("50.00"),
            updated_amount=Decimal("150.00"),
        )
        self.assertEqual(result, expected)

    def test_calculate_edge_case_year_bounds(self):
        result = self.rent_update.calculate(
            RentUpdateInput(
                amount=Decimal("100.00"),
                data=Decimal("50.00"),
                month=1,
                year_start=1900,
                year_end=2100,
            )
        )
        expected = RentUpdateResult(
            amount=Decimal("100.00"),
            data=Decimal("50.00"),
            updated_amount=Decimal("150.00"),
        )
        self.assertEqual(result, expected)

    def test_calculate_rounding_amount(self):
        result = self.rent_update.calculate(
            RentUpdateInput(
                amount=Decimal("100.005"),
                data=Decimal("0.005"),
            )
        )
        expected = RentUpdateResult(
            amount=Decimal("100.01"),
            data=Decimal("0.005"),
            updated_amount=Decimal("100.015"),
        )
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
