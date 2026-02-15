import unittest
from decimal import Decimal

from arrendatools.rent_update.base import RentUpdateInput, RentUpdateResult
from arrendatools.rent_update.factory import RentUpdateFactory


class TestPercentageUpdate(unittest.TestCase):

    def setUp(self):
        self.rent_update = RentUpdateFactory.create("percentage")

    def test_calculate_increase(self):
        result = self.rent_update.calculate(
            RentUpdateInput(amount=Decimal("100.00"), data=Decimal("0.10"))
        )
        expected = RentUpdateResult(
            amount=Decimal("100.00"),
            updated_amount=Decimal("110.00"),
            data=Decimal("0.10"),
            variation_rate=Decimal("0.10"),
        )
        self.assertEqual(result, expected)

    def test_calculate_decrease(self):
        result = self.rent_update.calculate(
            RentUpdateInput(amount=Decimal("100.00"), data=Decimal("-0.10"))
        )
        expected = RentUpdateResult(
            amount=Decimal("100.00"),
            updated_amount=Decimal("90.00"),
            data=Decimal("-0.10"),
            variation_rate=Decimal("-0.10"),
        )
        self.assertEqual(result, expected)

    def test_calculate_no_change(self):
        result = self.rent_update.calculate(
            RentUpdateInput(amount=Decimal("100.00"), data=Decimal("0.00"))
        )
        expected = RentUpdateResult(
            amount=Decimal("100.00"),
            updated_amount=Decimal("100.00"),
            data=Decimal("0.00"),
            variation_rate=Decimal("0.00"),
        )
        self.assertEqual(result, expected)

    def test_calculate_invalid_data(self):
        with self.assertRaises(ValueError) as context:
            self.rent_update.calculate(
                RentUpdateInput(amount=Decimal("100.00"), data=Decimal("1.10"))
            )
        self.assertEqual(
            str(context.exception),
            "Data must be a percentage between -1 (-100%) and 1 (100%).",
        )

    def test_calculate_missing_data(self):
        with self.assertRaises(ValueError) as context:
            self.rent_update.calculate(
                RentUpdateInput(amount=Decimal("100.00"))
            )
        self.assertEqual(
            str(context.exception),
            "Field 'data' is required.",
        )

    def test_calculate_percentage_boundaries(self):
        result_min = self.rent_update.calculate(
            RentUpdateInput(amount=Decimal("100.00"), data=Decimal("-1.0"))
        )
        expected_min = RentUpdateResult(
            amount=Decimal("100.00"),
            updated_amount=Decimal("0.00"),
            data=Decimal("-1.0"),
            variation_rate=Decimal("-1.0"),
        )
        self.assertEqual(result_min, expected_min)

        result_max = self.rent_update.calculate(
            RentUpdateInput(amount=Decimal("100.00"), data=Decimal("1.0"))
        )
        expected_max = RentUpdateResult(
            amount=Decimal("100.00"),
            updated_amount=Decimal("200.00"),
            data=Decimal("1.0"),
            variation_rate=Decimal("1.0"),
        )
        self.assertEqual(result_max, expected_max)


if __name__ == "__main__":
    unittest.main()
