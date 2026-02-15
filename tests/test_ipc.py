import unittest
from datetime import date
from decimal import Decimal
from unittest.mock import patch

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
            index_start=Decimal("60.030"),
            index_end=Decimal("61.827"),
            month="agosto",
            year_start=2002,
            year_end=2003,
            variation_rate=Decimal("0.03"),
        )
        self.assertEqual(result, expected)

    def test_calculate_jan_2025_to_jan_2026(self):
        # Caso: Actualización de rentas de alquiler con el IPC entre enero 2025 y enero 2026.
        # Este test comprueba el cambio de incide base 2025
        result = self.rent_update.calculate(
            RentUpdateInput(
                amount=Decimal("400.00"),
                year_start=2025,
                year_end=2026,
                month=1,
            )
        )
        expected = RentUpdateResult(
            amount=Decimal("400.00"),
            updated_amount=Decimal("409.20"),
            index_start=Decimal("98.579"),
            index_end=Decimal("100.836"),
            month="enero",
            year_start=2025,
            year_end=2026,
            variation_rate=Decimal("0.023"),
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
        print(result.as_dict())
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
        self.assertEqual(str(context.exception), "Year start is required.")

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
        self.assertEqual(str(context.exception), "Year end is required.")

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

    @patch("arrendatools.rent_update.strategies.ipc.IneClient.fetch_series_data")
    def test_fetch_ipc_no_data(self, mock_fetch):
        mock_fetch.return_value = {"Data": []}

        with self.assertRaises(ValueError) as context:
            self.rent_update._fetch_ipc(2024, 1)
        self.assertEqual(
            str(context.exception),
            "Rent not updated: Could not fetch IPC data for enero 2024.",
        )

    @patch("arrendatools.rent_update.strategies.ipc.IpcUpdate._fetch_ipc")
    def test_calculate_logs_connection_error(self, mock_fetch):
        mock_fetch.side_effect = ConnectionError("Boom")

        with self.assertLogs(
            "arrendatools.rent_update.strategies.ipc", level="ERROR"
        ) as logs:
            with self.assertRaises(ConnectionError):
                self.rent_update.calculate(
                    RentUpdateInput(
                        amount=Decimal("400.00"),
                        year_start=2002,
                        year_end=2003,
                        month=8,
                    )
                )
        self.assertTrue(
            any("INE IPC fetch failed: Boom" in message for message in logs.output)
        )

    @patch("arrendatools.rent_update.strategies.ipc.IpcUpdate._fetch_ipc")
    def test_calculate_cross_base_nan_ipc_raises_value_error(self, mock_fetch):
        mock_fetch.return_value = Decimal("NaN")

        with self.assertRaises(ValueError) as context:
            self.rent_update.calculate(
                RentUpdateInput(
                    month=1,
                    year_start=2001,
                    year_end=2002,
                    amount=Decimal("400.00"),
                )
            )
        self.assertEqual(
            str(context.exception),
            "Rent not updated: Could not fetch IPC data for enero 2002.",
        )

    @patch("arrendatools.rent_update.strategies.ipc.IpcUpdate._fetch_ipc")
    def test_calculate_2002_plus_nan_start_ipc_raises_value_error(self, mock_fetch):
        mock_fetch.side_effect = [Decimal("110.0"), Decimal("NaN")]

        with self.assertRaises(ValueError) as context:
            self.rent_update.calculate(
                RentUpdateInput(
                    amount=Decimal("400.00"),
                    year_start=2002,
                    year_end=2003,
                    month=8,
                )
            )
        self.assertEqual(
            str(context.exception),
            "Rent not updated: Could not fetch IPC data for agosto 2002.",
        )

    @patch("arrendatools.rent_update.strategies.ipc.IpcUpdate._fetch_ipc")
    def test_calculate_2002_plus_nan_end_ipc_raises_value_error(self, mock_fetch):
        mock_fetch.return_value = Decimal("NaN")

        with self.assertRaises(ValueError) as context:
            self.rent_update.calculate(
                RentUpdateInput(
                    amount=Decimal("400.00"),
                    year_start=2002,
                    year_end=2003,
                    month=8,
                )
            )
        self.assertEqual(
            str(context.exception),
            "Rent not updated: Could not fetch IPC data for agosto 2003.",
        )


if __name__ == "__main__":
    unittest.main()
