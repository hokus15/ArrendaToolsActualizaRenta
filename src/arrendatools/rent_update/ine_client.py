import json
import logging
from datetime import date

import requests


class IneClient:
    """Clase para conexion con la API del INE."""

    _BASE_URL = "https://servicios.ine.es/wstempus/js/ES/DATOS_SERIE"

    @staticmethod
    def fetch_series_data(
        start_date: date, end_date: date, series: str
    ) -> dict:
        """
        Obtiene datos de una serie del INE.

        Args:
            start_date (date): Fecha de inicio para la serie.
            end_date (date): Fecha de fin para la serie.
            series (str): Codigo de la serie temporal.

        Returns:
            dict: Datos de la serie temporal proporcionados por la API.

        Raises:
            ValueError: Si las fechas no son validas.
            ConnectionError: Si hay un problema con la conexion a la API.
            json.JSONDecodeError: Si la respuesta de la API no es JSON valido.
        """
        if start_date > end_date:
            raise ValueError(
                "Start date cannot be later than end date."
            )

        start_date_str = start_date.strftime("%Y%m%d")
        end_date_str = end_date.strftime("%Y%m%d")
        url = (
            f"{IneClient._BASE_URL}/{series}?date={start_date_str}:{end_date_str}"
        )

        try:
            logging.info("Requesting INE API: %s", url)
            response = requests.get(url, timeout=30)
            response.raise_for_status()
        except requests.exceptions.Timeout:
            logging.error("INE API request timed out.")
            raise ConnectionError("The request timed out.")
        except requests.exceptions.HTTPError as err:
            logging.error("HTTP error while calling INE API: %s", err)
            raise ConnectionError(f"HTTP error while calling INE API: {err}")
        except requests.exceptions.RequestException as err:
            logging.error("Connection error while calling INE API: %s", err)
            raise ConnectionError(f"Connection error while calling INE API: {err}")

        try:
            data = response.json()
            logging.info("INE API response parsed successfully.")
            return data
        except json.JSONDecodeError as err:
            logging.error("Invalid JSON response from INE API: %s", err)
            raise json.JSONDecodeError(
                f"Invalid JSON response: {err}",
                response.text,
                0,
            )
