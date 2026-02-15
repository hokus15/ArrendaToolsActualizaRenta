import unittest
from decimal import Decimal

from arrendatools.rent_update.base import RentUpdateInput, RentUpdateResult
from arrendatools.rent_update.factory import RentUpdateFactory


class TestIpcThenPercentageUpdate(unittest.TestCase):
    def setUp(self):
        self.rent_update = RentUpdateFactory.create("ipc_then_percentage")

    def test_calculate_ipc_then_percentage_increase(self):
        result = self.rent_update.calculate(
            RentUpdateInput(
                amount=Decimal("400.00"),
                data=Decimal("0.05"),
                year_start=2002,
                year_end=2003,
                month=8,
            )
        )
        expected = RentUpdateResult(
            amount=Decimal("400.00"),
            updated_amount=Decimal("432.60"),
            index_start=Decimal("60.030"),
            index_end=Decimal("61.827"),
            month="agosto",
            year_start=2002,
            year_end=2003,
            data=Decimal("0.05"),
            variation_rate=Decimal("0.082"),
        )
        self.assertEqual(result, expected)

    def test_calculate_ipc_then_percentage_decrease(self):
        result = self.rent_update.calculate(
            RentUpdateInput(
                amount=Decimal("400.00"),
                data=Decimal("-0.05"),
                year_start=2002,
                year_end=2003,
                month=8,
            )
        )
        expected = RentUpdateResult(
            amount=Decimal("400.00"),
            updated_amount=Decimal("391.40"),
            index_start=Decimal("60.030"),
            index_end=Decimal("61.827"),
            month="agosto",
            year_start=2002,
            year_end=2003,
            data=Decimal("-0.05"),
            variation_rate=Decimal("-0.022"),
        )
        self.assertEqual(result, expected)

    def test_calculate_data_can_be_negative_one(self):
        result = self.rent_update.calculate(
            RentUpdateInput(
                amount=Decimal("400.00"),
                data=Decimal("-1.0"),
                year_start=2002,
                year_end=2003,
                month=8,
            )
        )
        expected = RentUpdateResult(
            amount=Decimal("400.00"),
            updated_amount=Decimal("0.00"),
            index_start=Decimal("60.030"),
            index_end=Decimal("61.827"),
            month="agosto",
            year_start=2002,
            year_end=2003,
            data=Decimal("-1.0"),
            variation_rate=Decimal("-1.0"),
        )
        self.assertEqual(result, expected)

    def test_calculate_missing_data(self):
        with self.assertRaises(ValueError) as context:
            self.rent_update.calculate(
                RentUpdateInput(
                    amount=Decimal("100.00"),
                    year_start=1954,
                    year_end=2001,
                    month=8,
                )
            )
        self.assertEqual(
            str(context.exception),
            "Field 'data' is required.",
        )

    def test_calculate_invalid_data(self):
        with self.assertRaises(ValueError) as context:
            self.rent_update.calculate(
                RentUpdateInput(
                    amount=Decimal("100.00"),
                    data=Decimal("1.10"),
                    year_start=1954,
                    year_end=2001,
                    month=8,
                )
            )
        self.assertEqual(
            str(context.exception),
            "Data must be a percentage between -1 (-100%) and 1 (100%).",
        )

    def test_calculate_missing_month(self):
        with self.assertRaises(ValueError) as context:
            self.rent_update.calculate(
                RentUpdateInput(
                    amount=Decimal("100.00"),
                    data=Decimal("0.05"),
                    year_start=2002,
                    year_end=2003,
                )
            )
        self.assertEqual(str(context.exception), "Month is required.")

    def test_calculate_missing_start_year(self):
        with self.assertRaises(ValueError) as context:
            self.rent_update.calculate(
                RentUpdateInput(
                    amount=Decimal("100.00"),
                    data=Decimal("0.05"),
                    year_end=2003,
                    month=8,
                )
            )
        self.assertEqual(str(context.exception), "Year start is required.")

    def test_calculate_missing_end_year(self):
        with self.assertRaises(ValueError) as context:
            self.rent_update.calculate(
                RentUpdateInput(
                    amount=Decimal("100.00"),
                    data=Decimal("0.05"),
                    year_start=2002,
                    month=8,
                )
            )
        self.assertEqual(str(context.exception), "Year end is required.")

    def test_calculate_before_1954(self):
        with self.assertRaises(ValueError) as context:
            self.rent_update.calculate(
                RentUpdateInput(
                    amount=Decimal("100.00"),
                    data=Decimal("0.05"),
                    year_start=1953,
                    year_end=2001,
                    month=8,
                )
            )
        self.assertEqual(
            str(context.exception),
            "IPC data is only available from March 1954 onward.",
        )


if __name__ == "__main__":
    unittest.main()
