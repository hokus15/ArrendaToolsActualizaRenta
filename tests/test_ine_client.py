import json
import unittest
from datetime import date
from unittest.mock import Mock, patch

import requests

from arrendatools.rent_update.ine_client import IneClient


class TestIneClient(unittest.TestCase):
    def test_fetch_series_data_invalid_dates(self):
        with self.assertRaises(ValueError) as context:
            IneClient.fetch_series_data(
                start_date=date(2024, 2, 1),
                end_date=date(2024, 1, 1),
                series="IPC290751",
            )
        self.assertEqual(
            str(context.exception),
            "Start date cannot be later than end date.",
        )

    @patch("arrendatools.rent_update.ine_client.requests.get")
    def test_fetch_series_data_success(self, mock_get):
        response = Mock()
        response.raise_for_status.return_value = None
        response.json.return_value = {"Data": [{"Valor": "100.0"}]}
        mock_get.return_value = response

        start_date = date(2024, 1, 1)
        end_date = date(2024, 1, 1)
        result = IneClient.fetch_series_data(
            start_date=start_date,
            end_date=end_date,
            series="IPC290751",
        )

        expected_url = (
            "https://servicios.ine.es/wstempus/js/ES/DATOS_SERIE/IPC290751"
            "?date=20240101:20240101"
        )
        mock_get.assert_called_once_with(expected_url, timeout=30)
        self.assertEqual(result, {"Data": [{"Valor": "100.0"}]})

    @patch("arrendatools.rent_update.ine_client.requests.get")
    def test_fetch_series_data_timeout(self, mock_get):
        mock_get.side_effect = requests.exceptions.Timeout()

        with self.assertRaises(ConnectionError) as context:
            IneClient.fetch_series_data(
                start_date=date(2024, 1, 1),
                end_date=date(2024, 1, 1),
                series="IPC290751",
            )
        self.assertEqual(str(context.exception), "The request timed out.")

    @patch("arrendatools.rent_update.ine_client.requests.get")
    def test_fetch_series_data_http_error(self, mock_get):
        response = Mock()
        response.raise_for_status.side_effect = requests.exceptions.HTTPError(
            "Bad Request"
        )
        mock_get.return_value = response

        with self.assertRaises(ConnectionError) as context:
            IneClient.fetch_series_data(
                start_date=date(2024, 1, 1),
                end_date=date(2024, 1, 1),
                series="IPC290751",
            )
        self.assertIn("HTTP error while calling INE API", str(context.exception))

    @patch("arrendatools.rent_update.ine_client.requests.get")
    def test_fetch_series_data_request_exception(self, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException("Boom")

        with self.assertRaises(ConnectionError) as context:
            IneClient.fetch_series_data(
                start_date=date(2024, 1, 1),
                end_date=date(2024, 1, 1),
                series="IPC290751",
            )
        self.assertIn(
            "Connection error while calling INE API",
            str(context.exception),
        )

    @patch("arrendatools.rent_update.ine_client.requests.get")
    def test_fetch_series_data_invalid_json(self, mock_get):
        response = Mock()
        response.raise_for_status.return_value = None
        response.json.side_effect = json.JSONDecodeError("Bad", "{}", 0)
        response.text = "{}"
        mock_get.return_value = response

        with self.assertRaises(json.JSONDecodeError):
            IneClient.fetch_series_data(
                start_date=date(2024, 1, 1),
                end_date=date(2024, 1, 1),
                series="IPC290751",
            )


if __name__ == "__main__":
    unittest.main()
