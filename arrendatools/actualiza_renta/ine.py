import requests
import json


def obtener_serie_INE(fechaInicio, fechaFin, serie):
    """Obtiene los datos de una serie temporal del Instituto Nacional de Estadística (INE) a través de su API web.

    Args:
        fechaInicio (datetime): Fecha de inicio en la que se quiere obtener los datos de la serie.
        fechaFin (datetime): Fecha de fin en la que se quiere obtener los datos de la serie.
        serie (str): Código de la serie temporal en la que se están interesado en obtener datos. Este código se puede encontrar en la web del INE.

    Returns:
        dict: Un diccionario con los datos de la serie temporal obtenidos de la API del INE.

    Raises:
        requests.exceptions.RequestException: Se produce si hay algún problema al hacer la petición a la API del INE.
        json.JSONDecodeError: Se produce si hay algún problema al decodificar el contenido de la respuesta de la API del INE como un objeto JSON.

    """
    anyoInicial = fechaInicio.strftime('%Y')
    mesInicial = fechaInicio.strftime('%m')
    diaInicial = fechaInicio.strftime('%d')

    anyoFinal = fechaFin.strftime('%Y')
    mesFinal = fechaFin.strftime('%m')
    diaFinal = fechaFin.strftime('%d')

    url = f'https://servicios.ine.es/wstempus/js/ES/DATOS_SERIE/{serie}?date={anyoInicial}{mesInicial}{diaInicial}:{anyoFinal}{mesFinal}{diaFinal}'
    print(url)
    try:
        res = requests.get(url, timeout=30)
        res.raise_for_status()
        # print(res.status_code)
        contenidos = res.text
        # print(contenidos)
    except requests.exceptions.Timeout as err:
        raise ConnectionError(err)
    except requests.exceptions.HTTPError as err:
        raise ConnectionError(err)
    return json.loads(contenidos)
