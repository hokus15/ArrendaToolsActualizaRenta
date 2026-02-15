import unittest
from datetime import date
from decimal import Decimal

from arrendatools.rent_update.base import RentUpdateInput, RentUpdateResult
from arrendatools.rent_update.factory import RentUpdateFactory


class TestMinIpcOrPercentageUpdate(unittest.TestCase):
    def setUp(self):
        self.rent_update = RentUpdateFactory.create(
            "min_ipc_or_percentage"
        )

    def test_calculate_same_rate(self):
        result = self.rent_update.calculate(
            RentUpdateInput(
                amount=Decimal("400.00"),
                data=Decimal("0.03"),
                year_start=2002,
                year_end=2003,
                month=8,
            )
        )
        expected = RentUpdateResult(
            amount=Decimal("400.00"),
            updated_amount=Decimal("412.00"),
            index_start=Decimal("71.085"),
            index_end=Decimal("73.213"),
            data=Decimal("0.03"),
            month="agosto",
            year_start=2002,
            year_end=2003,
            variation_rate=Decimal("0.03"),
        )
        self.assertEqual(result, expected)

    def test_calculate_data_is_minimum(self):
        result = self.rent_update.calculate(
            RentUpdateInput(
                amount=Decimal("400.00"),
                data=Decimal("0.022"),
                year_start=2002,
                year_end=2003,
                month=8,
            )
        )
        expected = RentUpdateResult(
            amount=Decimal("400.00"),
            updated_amount=Decimal("408.80"),
            index_start=Decimal("71.085"),
            index_end=Decimal("73.213"),
            month="agosto",
            year_start=2002,
            year_end=2003,
            data=Decimal("0.022"),
            variation_rate=Decimal("0.022"),
        )
        self.assertEqual(result, expected)

    def test_calculate_ipc_is_minimum(self):
        result = self.rent_update.calculate(
            RentUpdateInput(
                amount=Decimal("400.00"),
                data=Decimal("0.055"),
                year_start=2002,
                year_end=2003,
                month=8,
            )
        )
        expected = RentUpdateResult(
            amount=Decimal("400.00"),
            updated_amount=Decimal("412.00"),
            index_start=Decimal("71.085"),
            index_end=Decimal("73.213"),
            month="agosto",
            year_start=2002,
            year_end=2003,
            data=Decimal("0.055"),
            variation_rate=Decimal("0.030"),
        )
        self.assertEqual(result, expected)

    def test_calculate_before_1954(self):
        # Caso: Actualización de rentas de alquiler año inicial anterior a 1954
        with self.assertRaises(ValueError) as context:
            self.rent_update.calculate(
                RentUpdateInput(
                    month=8,
                    data=Decimal("0.05"),
                    year_start=1953,
                    year_end=2001,
                    amount=Decimal("400.00"),
                )
            )
        self.assertEqual(
            str(context.exception),
            "IPC data is only available from March 1954 onward.",
        )

    def test_calculate_before_march_1954(self):
        # Caso: Actualización de rentas de alquiler año inicial anterior a 1954
        with self.assertRaises(ValueError) as context:
            self.rent_update.calculate(
                RentUpdateInput(
                    month=2,
                    data=Decimal("0.05"),
                    year_start=1954,
                    year_end=2001,
                    amount=Decimal("400.00"),
                )
            )
        self.assertEqual(
            str(context.exception),
            "IPC data is only available from March 1954 onward.",
        )

    def test_calculate_future(self):
        today = date.today()  # Obtiene la fecha actual
        next_year = today.year + 1  # Año que viene
        # Caso: Actualización de rentas de alquiler de un periodo en el que todavía no se ha publicado los datos del IPC
        with self.assertRaises(ValueError) as context:
            self.rent_update.calculate(
                RentUpdateInput(
                    month=2,
                    data=Decimal("0.05"),
                    year_start=2022,
                    year_end=next_year,
                    amount=Decimal("400.00"),
                )
            )
        self.assertEqual(
            str(context.exception),
            f"Rent not updated: Could not fetch IPC data for febrero {next_year}.",
        )

    def test_calculate_missing_month(self):
        # Caso: Actualización de rentas de alquiler sin proporcionar el mes
        with self.assertRaises(ValueError) as context:
            self.rent_update.calculate(
                RentUpdateInput(
                    data=Decimal("0.05"),
                    year_start=2022,
                    year_end=2023,
                    amount=Decimal("400.00"),
                )
            )
        self.assertEqual(str(context.exception), "Month is required.")

    def test_calculate_missing_start_year(self):
        # Caso: Actualización de rentas de alquiler sin proporcionar el año inicial
        with self.assertRaises(ValueError) as context:
            self.rent_update.calculate(
                RentUpdateInput(
                    month=2,
                    data=Decimal("0.05"),
                    year_end=2023,
                    amount=Decimal("400.00"),
                )
            )
        self.assertEqual(
            str(context.exception), "Year start is required."
        )

    def test_calculate_missing_end_year(self):
        # Caso: Actualización de rentas de alquiler sin proporcionar el año final
        with self.assertRaises(ValueError) as context:
            self.rent_update.calculate(
                RentUpdateInput(
                    month=2,
                    data=Decimal("0.05"),
                    year_start=2022,
                    amount=Decimal("400.00"),
                )
            )
        self.assertEqual(
            str(context.exception), "Year end is required."
        )

    def test_calculate_invalid_start_year(self):
        # Caso: Actualización de rentas de alquiler con año inicial no válido
        with self.assertRaises(ValueError) as context:
            self.rent_update.calculate(
                RentUpdateInput(
                    month=2,
                    data=Decimal("0.05"),
                    year_start=1953,
                    year_end=2023,
                    amount=Decimal("400.00"),
                )
            )
        self.assertEqual(
            str(context.exception),
            "IPC data is only available from March 1954 onward.",
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
            index_start=Decimal("71.085"),
            index_end=Decimal("73.213"),
            month="agosto",
            year_start=2002,
            year_end=2003,
            data=Decimal("-1.0"),
            variation_rate=Decimal("-1.0"),
        )
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
