"""Estrategias de actualizacion de renta."""

from arrendatools.rent_update.strategies.fixed_amount import FixedAmountUpdate
from arrendatools.rent_update.strategies.ipc import IpcUpdate
from arrendatools.rent_update.strategies.ipc_then_percentage import (
    IpcThenPercentageUpdate,
)
from arrendatools.rent_update.strategies.irav import IravUpdate
from arrendatools.rent_update.strategies.min_ipc_or_percentage import (
    MinIpcOrPercentageUpdate,
)
from arrendatools.rent_update.strategies.percentage import PercentageUpdate

__all__ = [
    "FixedAmountUpdate",
    "IpcUpdate",
    "IpcThenPercentageUpdate",
    "IravUpdate",
    "MinIpcOrPercentageUpdate",
    "PercentageUpdate",
]
