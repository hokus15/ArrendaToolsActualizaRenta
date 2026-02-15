import unittest
from decimal import Decimal

from arrendatools.rent_update.base import RentUpdateInput, RentUpdateResult


class TestRentUpdateInput(unittest.TestCase):
    def test_validate_inputs_valid(self):
        try:
            RentUpdateInput(
                amount=Decimal("100.0"),
                data=Decimal("10.0"),
                month=5,
                year_start=2020,
                year_end=2021,
            )
        except ValueError:
            self.fail("RentUpdateInput raised ValueError unexpectedly!")

    def test_validate_inputs_invalid_amount(self):
        with self.assertRaises(ValueError) as context:
            RentUpdateInput(amount="100.0")
        self.assertEqual(
            str(context.exception),
            "Amount must be Decimal.",
        )

    def test_validate_inputs_invalid_data(self):
        with self.assertRaises(ValueError) as context:
            RentUpdateInput(amount=Decimal("100.0"), data="10.0")
        self.assertEqual(
            str(context.exception),
            "Data must be Decimal.",
        )

    def test_validate_inputs_invalid_month_upper(self):
        with self.assertRaises(ValueError) as context:
            RentUpdateInput(amount=Decimal("100.0"), month=13)
        self.assertEqual(
            str(context.exception),
            "Month must be between 1 and 12.",
        )

    def test_validate_inputs_invalid_month_lower(self):
        with self.assertRaises(ValueError) as context:
            RentUpdateInput(amount=Decimal("100.0"), month=0)
        self.assertEqual(
            str(context.exception),
            "Month must be between 1 and 12.",
        )

    def test_validate_inputs_invalid_start_year(self):
        with self.assertRaises(ValueError) as context:
            RentUpdateInput(amount=Decimal("100.0"), year_start="2020")
        self.assertEqual(
            str(context.exception),
            "Year start must be int.",
        )

    def test_validate_inputs_invalid_end_year(self):
        with self.assertRaises(ValueError) as context:
            RentUpdateInput(amount=Decimal("100.0"), year_end="2021")
        self.assertEqual(
            str(context.exception),
            "Year end must be int.",
        )

    def test_validate_inputs_end_year_before_start_year(self):
        with self.assertRaises(ValueError) as context:
            RentUpdateInput(
                amount=Decimal("100.0"), year_start=2021, year_end=2020
            )
        self.assertEqual(
            str(context.exception),
            "Year end cannot be earlier than year start.",
        )


class TestRentUpdateResult(unittest.TestCase):
    def test_as_dict_excludes_none_by_default(self):
        result = RentUpdateResult(
            amount=Decimal("10.00"),
            updated_amount=Decimal("11.00"),
        )
        self.assertEqual(
            result.as_dict(),
            {
                "amount": Decimal("10.00"),
                "updated_amount": Decimal("11.00"),
            },
        )

    def test_as_dict_includes_none_when_requested(self):
        result = RentUpdateResult(
            amount=Decimal("10.00"),
            updated_amount=Decimal("11.00"),
        )
        data = result.as_dict(include_none=True)
        self.assertIn("data", data)
        self.assertIsNone(data["data"])


if __name__ == "__main__":
    unittest.main()
