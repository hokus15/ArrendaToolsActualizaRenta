# ArrendaTools Actualiza Renta
![License](https://img.shields.io/github/license/hokus15/ArrendaToolsActualizaRenta)
[![Build Status](https://github.com/hokus15/ArrendaToolsActualizaRenta/actions/workflows/main.yml/badge.svg)](https://github.com/hokus15/ArrendaToolsActualizaRenta/actions)
![GitHub last commit](https://img.shields.io/github/last-commit/hokus15/ArrendaToolsActualizaRenta?logo=github)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/hokus15/ArrendaToolsActualizaRenta?logo=github)

Módulo de python para calcular la actualización de rentas de alquiler en España por anualidades completas. Compatible con múltiples métodos, incluyendo:
- Porcentaje
- Cantidad fija
- Actualización basada en IPC (Índice de Precios al Consumo)
- IRAV (Índice de Rentas de Alquiler de Viviendas)
- Combinación mínima entre IPC y porcentaje

El cálculo usando el IPC (LAU), se basa según lo descrito en la página web del [Instituto Nacional de Estadística (INE)](https://www.ine.es/ss/Satellite?c=Page&cid=1254735905720&pagename=ProductosYServicios%2FPYSLayout&L=0&p=1254735893337). Es equivalente a utilizar la calculadora publicada por el INE en el siguiente enlace [Actualización de rentas con el IPC general (sistema IPC base 2021) para periodos anuales completos](https://www.ine.es/calcula).

## Limitaciones

Este módulo es válido solamente:
- En España
- Actualización usando el IPC: Para los periodos comprendidos entre marzo de 1954 y el último mes con datos de IPC publicados por el INE.
- Actualización usando el IRAV: Para los periodos comprendidos entre noviembre de 2024 y el último mes con datos de IRAV publicados por el INE.

## Estructura

El modulo utiliza una arquitectura basada en clases con un patron Factory para la creacion dinamica de diferentes metodos de actualizacion:

1. **`RentUpdateMethod`**: Clase base abstracta que define la interfaz para las actualizaciones.
2. **`RentUpdateFactory`**: Proporciona una forma dinamica de instanciar clases de actualizacion segun el tipo requerido.
3. **Estrategias**:

    - `PercentageUpdate` (`percentage`)
    - `FixedAmountUpdate` (`fixed_amount`)
    - `IpcUpdate` (`ipc`)
    - `MinIpcOrPercentageUpdate` (`min_ipc_or_percentage`)
    - `IpcThenPercentageUpdate` (`ipc_then_percentage`)
    - `IravUpdate` (`irav`)

4. **`IneClient`**: Clase que se conecta al INE para obtener los datos del IPC e IRAV.

Las estrategias viven en el paquete `arrendatools.rent_update.strategies`, y la factory carga las estrategias internas y las registradas via entry points (grupo `arrendatools.rent_update`).

## Requisitos

Este módulo requiere Python 3.10 o superior.

## Uso

La factory espera un `RentUpdateInput` y devuelve un `RentUpdateResult`.


### Parámetros de entrada

Los parametros se proporcionan a traves de `RentUpdateInput`.
`amount (Decimal)`: **Obligatorio**. La cantidad de la renta a actualizar.

`month (int)`: Obligatorio para los tipos de actualizacion **ipc**, **irav** y **min_ipc_or_percentage**. El mes en que se quiere calcular la actualizacion de la renta (1 a 12).

`year_start (int)`: Obligatorio para los tipos de actualizacion **ipc**, **irav** y **min_ipc_or_percentage**. El ano inicial de referencia para el calculo.

`year_end (int)`: Obligatorio para los tipos de actualizacion **ipc** y **min_ipc_or_percentage**. El ano final de referencia para el calculo.

`data (Decimal)`: Obligatorio para los tipos de actualizacion **percentage**, **fixed_amount** y **min_ipc_or_percentage**. Dato adicional para hacer los calculos, por ejemplo en la actualizacion por porcentaje es el porcentaje de actualizacion (-1 -> -100% y 1 -> 100%). En la actualizacion por cantidad fija es la cantidad a actualizar.

### Retorno

La funcion devuelve un `RentUpdateResult` (puedes usar `as_dict()` para obtener un diccionario) con los siguientes campos:

`amount (Decimal)`: **Obligatorio**. La cantidad pasada inicialmente por el usuario.

`updated_amount (Decimal)`: **Obligatorio**. La cantidad de la renta actualizada con el metodo escogido.

`index_start (int)`: **Opcional**, solo se devuelve para la actualizacion por IPC o min_ipc_or_percentage. El indice del IPC del mes inicial.

`index_end (int)`: **Opcional**, solo se devuelve para la actualizacion por IPC o min_ipc_or_percentage. El indice del IPC del mes final.

`month (str)`: **Opcional**, solo se devuelve para la actualizacion por IPC, min_ipc_or_percentage o IRAV. El nombre del mes en que se calculo la actualizacion de la renta.

`year_start (int)`: **Opcional**, solo se devuelve para la actualizacion por IPC, min_ipc_or_percentage o IRAV. El ano inicial de referencia para el calculo. 

`year_end (int)`: **Opcional**, solo se devuelve para la actualizacion por IPC o min_ipc_or_percentage. El ano final de referencia para el calculo.

`variation_rate (Decimal)`: **Opcional**, solo se devuelve para la actualizacion por IPC, min_ipc_or_percentage, IRAV, percentage. La tasa de variacion utilizada en el calculo. Multiplicado por 100 es el porcentaje.

## Ejemplo de uso

```python
from decimal import Decimal
from arrendatools.rent_update.base import RentUpdateInput
from arrendatools.rent_update.factory import RentUpdateFactory

# Crear una instancia usando el Factory
actualizacion_renta = RentUpdateFactory.create("percentage")

# Calcular pasando los datos al método calcular
resultado = actualizacion_renta.calculate(
    RentUpdateInput(
        amount=Decimal("1000.00"),
        data=Decimal("0.05"),
    )
)

print(resultado.as_dict())
```

Resultado:
```
{'amount': Decimal('1000.00'), 'data': Decimal('0.05'), 'updated_amount': Decimal('1050.00'), 'variation_rate': Decimal('0.05')}
```

## Tests

Instala el paquete en modo editable y ejecuta los tests:

```bash
python -m pip install -e .
python -m pytest
```

## Guia de migracion (v1 -> v2)

Esta version introduce cambios de entorno y tooling. Pasos recomendados:

1. **Python minimo**: actualiza tu runtime a Python 3.10 o superior.
2. **Instalacion**: reinstala el paquete en editable si trabajas en local.

    ```bash
    python -m pip install -e .
    ```

3. **Tests**: si tenias scripts con `unittest`, migra a `pytest`.

    ```bash
    python -m pytest
    ```

4. **CI**: si tu pipeline usaba `unittest`, cambia a `tox` o `pytest`.

    ```bash
    tox -e py310
    ```

5. **Nuevas estrategias**: se anade `ipc_then_percentage` en la factory.

    ```python
    from arrendatools.rent_update.factory import RentUpdateFactory

    strategy = RentUpdateFactory.create("ipc_then_percentage")
    ```

### Cambios relevantes desde v1

- **Python minimo**: se eleva a 3.10+ (antes 3.8+).
- **Tests**: se estandariza el uso de `pytest` y `tox` en lugar de `unittest` directo.
- **Cobertura**: se anade ejecucion con `pytest-cov` en CI.
- **Nueva estrategia**: `ipc_then_percentage` disponible via `RentUpdateFactory`.
- **Factory**: las claves siguen normalizandose a minusculas; usa `RentUpdateFactory.create("ipc_then_percentage")` para la nueva estrategia.
- **Input/Output**: ahora `calculate()` recibe un `RentUpdateInput` (dataclass) en lugar de parametros sueltos, y devuelve un `RentUpdateResult` (dataclass). Si necesitas un `dict`, usa `result.as_dict()`.

Ejemplo v1 vs v2:

```python
# v1 (parametros sueltos + dict)
resultado = actualizacion_renta.calculate(
    amount=Decimal("1000.00"),
    data=Decimal("0.05"),
)
print(resultado)

# v2 (dataclass + as_dict)
resultado = actualizacion_renta.calculate(
    RentUpdateInput(
        amount=Decimal("1000.00"),
        data=Decimal("0.05"),
    )
)
print(resultado.as_dict())
```

## Crear y registrar nuevas estrategias

### 1) Implementar una estrategia

Crea una clase que herede de `RentUpdateMethod` y reimplemente `calculate()` (y opcionalmente `validate_inputs()`):

```python
from decimal import Decimal
from typing import Optional

from arrendatools.rent_update.base import (
    RentUpdateInput,
    RentUpdateMethod,
    RentUpdateResult,
)


class CustomUpdate(RentUpdateMethod):
    def calculate(self, inputs: RentUpdateInput) -> RentUpdateResult:
        return RentUpdateResult(
            amount=inputs.amount,
            updated_amount=inputs.amount,
        )
```

### 2) Registrar via entry points (recomendado)

En tu propio paquete, declara el entry point en `pyproject.toml`:

```toml
[project.entry-points."arrendatools.rent_update"]
custom = "mi_paquete.strategies.custom:CustomUpdate"
```

Luego, en tiempo de ejecucion:

```python
from arrendatools.rent_update.factory import RentUpdateFactory

custom_update = RentUpdateFactory.create("custom")
```

Nota: las claves de estrategia son case-insensitive y se normalizan a `snake_case` en minusculas. Usa nombres claros y estables (por ejemplo, `custom`, `ipc`, `min_ipc_or_percentage`) para evitar colisiones.

### 3) Registro manual (para uso local)

Si no quieres entry points, puedes registrar la clase en runtime:

```python
from arrendatools.rent_update.factory import RentUpdateFactory
from mi_paquete.strategies.custom import CustomUpdate

RentUpdateFactory.register("custom", CustomUpdate)
custom_update = RentUpdateFactory.create("custom")
```

## Descargo de responsabilidad

Este módulo proporciona una opción para actualizar una renta de alquiler en España por anualidades completas usando varios métodos como el IPC (LAU) o IRAV y realiza los cálculos necesarios conectándose a la página web del INE. Sin embargo, es importante tener en cuenta que este módulo no garantiza el cálculo correcto ni sirve como certificación oficial ante el arrendatario. **El usuario es responsable de verificar la exactitud de los datos generados y de obtener el certificado correspondiente en la página web del INE si es necesario.**

Es importante destacar que **el autor de este módulo está exento de cualquier tipo de responsabilidad derivada del uso de la información generada por este módulo**. La veracidad y exactitud de los datos generados son responsabilidad exclusiva del usuario. Cualquier sanción que pudiera derivarse del uso correcto, incorrecto o fraudulento de los datos generados por este módulo será responsabilidad exclusiva del usuario.

Por tanto, se recomienda al usuario **revisar cuidadosamente la información generada antes de notificar al inquilino la actualización de la renta y asegurarse de que cumple con los requisitos y está libre de errores**.
