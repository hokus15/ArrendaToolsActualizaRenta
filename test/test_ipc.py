import unittest
from datetime import date
from arrendatools.actualiza_renta.ipc import actualiza_renta_IPC


class ActualizaRentaIPCTestCase(unittest.TestCase):

    def test_actualiza_renta_IPC_meses_posteriores_enero_2002(self):
        # Caso Actualización de rentas de alquiler con el IPC entre dos meses posteriores a enero de 2002
        # Se quiere actualizar una renta de 400€ con el IPC entre agosto de 2002 y agosto de 2003.
        resultado = actualiza_renta_IPC(8, 2002, 2003, 400.00)
        esperado = {
            'cantidad_actualizada': 412.00,
            'indice_mes_inicial': 71.085,
            'indice_mes_final': 73.213,
            'mes': "Agosto",
            'anyo_inicial': 2002,
            'anyo_final': 2003,
            'tasa_variacion': 0.030
        }
        self.assertEqual(resultado, esperado)

    def test_actualiza_renta_IPC_entre_mes_anterior_2002_y_mes_posterior_enero_2002(self):
        # Caso: Actualización de rentas de alquiler con el IPC entre un mes anterior a enero de 2002 y otro posterior
        # Se quiere actualizar una renta con el IPC entre enero de 2001 y enero de 2002.
        resultado = actualiza_renta_IPC(1, 2001, 2002, 400.00)
        esperado = {
            'cantidad_actualizada': 412.40,
            'indice_mes_inicial': 133.413,
            'indice_mes_final': 137.484,
            'mes': "Enero",
            'anyo_inicial': 2001,
            'anyo_final': 2002,
            'tasa_variacion': 0.031
        }
        self.assertEqual(resultado, esperado)

    def test_actualiza_renta_IPC_entre_meses_anteriores_enero_2002(self):
        # Caso: Actualización de rentas de alquiler con el IPC entre dos meses anteriores a enero de 2002
        # Se quiere actualizar una renta con el IPC entre agosto de 1999 y agosto de 2001
        resultado = actualiza_renta_IPC(8, 1999, 2001, 400.00)
        esperado = {
            'cantidad_actualizada': 429.6,
            'indice_mes_inicial': 127.312,
            'indice_mes_final': 136.745,
            'mes': "Agosto",
            'anyo_inicial': 1999,
            'anyo_final': 2001,
            'tasa_variacion': 0.074
        }
        self.assertEqual(resultado, esperado)

    def test_actualiza_renta_IPC_anterior_1954(self):
        # Caso: Actualización de rentas de alquiler año inicial anterior a 1954
        with self.assertRaisesRegex(ValueError, "El año debe ser posterior a 1953."):
            actualiza_renta_IPC(8, 1953, 2001, 400.00)

    def test_actualiza_renta_IPC_anterior_marzo_1954(self):
        # Caso: Actualización de rentas de alquiler año inicial anterior a 1954
        with self.assertRaisesRegex(ValueError, "Sólo hay datos de IPC a partir de Marzo de 1954."):
            actualiza_renta_IPC(2, 1954, 2001, 400.00)

    def test_actualiza_renta_IPC_sin_IPC(self):
        hoy = date.today()  # Obtiene la fecha actual
        anyo_siguiente = hoy.year + 1  # Año que viene
        # Caso: Actualización de rentas de alquiler de un periodo en el que todavía no se ha publacado los datos del IPC
        with self.assertRaisesRegex(ValueError, f"Renta no actualizada: No he podido recuperar los datos de IPC para Febrero de {anyo_siguiente}"):
            actualiza_renta_IPC(2, 2022, anyo_siguiente, 400.00)


if __name__ == '__main__':
    unittest.main()
