import unittest
from datetime import date
from decimal import Decimal

from arrendatools.rent_update.base import RentUpdateInput, RentUpdateResult
from arrendatools.rent_update.factory import RentUpdateFactory


class TestIpcUpdate(unittest.TestCase):
    def setUp(self):
        self.rent_update = RentUpdateFactory.create("ipc")

    def test_calculate_months_after_jan_2002(self):
        # Caso Actualización de rentas de alquiler con el IPC entre dos meses posteriores a enero de 2002
        # Se quiere actualizar una renta de 400€ con el IPC entre agosto de 2002 y agosto de 2003.
        result = self.rent_update.calculate(
            RentUpdateInput(
                amount=Decimal("400.00"),
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
            variation_rate=Decimal("0.03"),
        )
        self.assertEqual(result, expected)

    def test_calculate_cross_base_jan_2002(
        self,
    ):
        # Caso: Actualización de rentas de alquiler con el IPC entre un mes anterior a enero de 2002 y otro posterior
        # Se quiere actualizar una renta con el IPC entre enero de 2001 y enero de 2002.
        result = self.rent_update.calculate(
            RentUpdateInput(
                month=1,
                year_start=2001,
                year_end=2002,
                amount=Decimal("400.00"),
            )
        )
        expected = RentUpdateResult(
            amount=Decimal("400.00"),
            updated_amount=Decimal("412.40"),
            index_start=Decimal("133.413"),
            index_end=Decimal("137.484"),
            month="enero",
            year_start=2001,
            year_end=2002,
            variation_rate=Decimal("0.031"),
        )
        self.assertEqual(result, expected)

    def test_calculate_months_before_jan_2002(self):
        # Caso: Actualización de rentas de alquiler con el IPC entre dos meses anteriores a enero de 2002
        # Se quiere actualizar una renta con el IPC entre agosto de 1999 y agosto de 2001
        result = self.rent_update.calculate(
            RentUpdateInput(
                month=8,
                year_start=1999,
                year_end=2001,
                amount=Decimal("400.00"),
            )
        )
        expected = RentUpdateResult(
            amount=Decimal("400.00"),
            updated_amount=Decimal("429.6"),
            index_start=Decimal("127.312"),
            index_end=Decimal("136.745"),
            month="agosto",
            year_start=1999,
            year_end=2001,
            variation_rate=Decimal("0.074"),
        )
        self.assertEqual(result, expected)

    def test_calculate_before_1954(self):
        # Caso: Actualización de rentas de alquiler año inicial anterior a 1954
        with self.assertRaises(ValueError) as context:
            self.rent_update.calculate(
                RentUpdateInput(
                    month=8,
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
                    year_start=1953,
                    year_end=2023,
                    amount=Decimal("400.00"),
                )
            )
        self.assertEqual(
            str(context.exception),
            "IPC data is only available from March 1954 onward.",
        )


if __name__ == "__main__":
    unittest.main()
