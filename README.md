# ArrendaTools Actualiza Renta
![License](https://img.shields.io/github/license/hokus15/ArrendaToolsActualizaRenta)
[![Build Status](https://github.com/hokus15/ArrendaToolsActualizaRenta/actions/workflows/main.yml/badge.svg)](https://github.com/hokus15/ArrendaToolsActualizaRenta/actions)
![GitHub last commit](https://img.shields.io/github/last-commit/hokus15/ArrendaToolsActualizaRenta?logo=github)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/hokus15/ArrendaToolsActualizaRenta?logo=github)

Módulo de Python que te permite actualizar las rentas de alquiler en España por anualidades completas.
Puede hacer el cálculo usando el IPC (LAU), según lo descrito en la página web del [Instituto Nacional de Estadística (INE)](https://www.ine.es/ss/Satellite?c=Page&cid=1254735905720&pagename=ProductosYServicios%2FPYSLayout&L=0&p=1254735893337). Es equivalente a utilizar la calculadora publicada por el INE en el siguiente enlace [Actualización de rentas con el IPC general (sistema IPC base 2021) para periodos anuales completos](https://www.ine.es/calcula).

## Limitaciones
Este módulo es válido solamente:
- En España
- Para la actualización por IPC: Para los periodos comprendidos entre marzo de 1954 y el último mes con datos de IPC publicados por el INE.

## Descargo de responsabilidad
Este módulo proporciona una opción para actualizar una renta de alquiler en España por anualidades completas usando varios métodos como el IPC (LAU) y realiza los cálculos necesarios conectándose a la página web del INE. Sin embargo, es importante tener en cuenta que este módulo no garantiza el cálculo correcto ni sirve como certificación oficial ante el arrendatario. **El usuario es responsable de verificar la exactitud de los datos generados y de obtener el certificado correspondiente en la página web del INE si es necesario.**

Es importante destacar que **el autor de este módulo está exento de cualquier tipo de responsabilidad derivada del uso de la información generada por este módulo**. La veracidad y exactitud de los datos generados son responsabilidad exclusiva del usuario. Cualquier sanción que pudiera derivarse del uso correcto, incorrecto o fraudulento de los datos generados por este módulo será responsabilidad exclusiva del usuario.

Por tanto, se recomienda al usuario **revisar cuidadosamente la información generada antes de notificar al inquilino la actualización de la renta y asegurarse de que cumple con los requisitos y está libre de errores**.

## Requisitos

Este módulo requiere Python 3.7 o superior.

## Uso

La función `actualiza_renta_IPC` calcula la actualización de una renta con base en el IPC.

### Parámetros
`mes (int)`: el mes en que se quiere calcular la actualización de la renta (1 a 12).

`anyo_inicial (int)`: el año inicial de referencia para el cálculo.

`anyo_final (int)`: el año final de referencia para el cálculo.

`cantidad (float)`: la cantidad de la renta a actualizar.

### Retorno
La función devuelve un diccionario con los siguientes campos:

`cantidad_actualizada (float)`: la cantidad de la renta actualizada con el IPC.

`indice_mes_inicial (int)`: el índice del IPC del mes inicial.

`indice_mes_final (int)`: el índice del IPC del mes final.

`mes (str)`: el nombre del mes en que se calculó la actualización de la renta.

`anyo_inicial (int)`: el año inicial de referencia para el cálculo.

`anyo_final (int)`: el año final de referencia para el cálculo.

`tasa_variacion (float)`: la tasa de variación utilizada en el cálculo. Multiplicado por 100 es el porcentaje.

Para utilizar esta función, simplemente importa el módulo `arrendatools_ipc.ipc` y llama al método `actualiza_renta_IPC` con los parámetros correspondientes:

```python
from arrendatools.actualiza_renta.ipc import actualiza_renta_IPC

resultado = actualiza_renta_IPC(mes=4, anyo_inicial=2021, anyo_final=2022, cantidad=1000)

print(resultado)
```

Resultado:
```
{'cantidad_actualizada': 1083.0, 'indice_mes_inicial': 99.105, 'indice_mes_final': 107.375, 'mes': 'Abril', 'anyo_inicial': 2021, 'anyo_final': 2022, 'tasa_variacion': 0.083}
```
