from __future__ import annotations

from importlib import metadata
from typing import Dict, Type

from arrendatools.rent_update.base import RentUpdateMethod
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


class RentUpdateFactory:
    """Factory para crear instancias de RentUpdateMethod."""

    _registry: Dict[str, Type[RentUpdateMethod]] = {}
    _entry_points_loaded = False
    _builtins_loaded = False
    _builtin_classes = {
        "percentage": PercentageUpdate,
        "fixed_amount": FixedAmountUpdate,
        "ipc": IpcUpdate,
        "ipc_then_percentage": IpcThenPercentageUpdate,
        "irav": IravUpdate,
        "min_ipc_or_percentage": MinIpcOrPercentageUpdate,
    }

    @classmethod
    def _normalize_key(cls, key: str) -> str:
        return key.strip().lower()

    @classmethod
    def register(cls, key: str, klass: Type[RentUpdateMethod]) -> None:
        """Registra una clase bajo una clave para la factory."""
        cls._registry[cls._normalize_key(key)] = klass

    @classmethod
    def _load_builtins(cls) -> None:
        if cls._builtins_loaded:
            return

        for key, klass in cls._builtin_classes.items():
            cls.register(key, klass)

        cls._builtins_loaded = True

    @classmethod
    def _load_entry_points(cls) -> None:
        if cls._entry_points_loaded:
            return

        entry_points = metadata.entry_points()
        if hasattr(entry_points, "select"):
            candidates = entry_points.select(group="arrendatools.rent_update")
        else:
            candidates = entry_points.get("arrendatools.rent_update", [])

        for entry_point in candidates:
            cls.register(entry_point.name, entry_point.load())

        cls._entry_points_loaded = True

    @classmethod
    def create(cls, update_type: str) -> RentUpdateMethod:
        """
        Crea una instancia de una clase que extiende RentUpdateMethod.

        :param update_type: Clave registrada o entry point.
        :return: Instancia de la clase especificada.
        :raises ValueError: Si no existe una clase con el nombre especificado.
        """
        cls._load_builtins()
        cls._load_entry_points()

        klass = cls._registry.get(cls._normalize_key(update_type))
        if not klass:
            available = ", ".join(sorted(cls._registry))
            raise ValueError(
                f"Unknown update type: {update_type}. Available: {available}"
            )
        return klass()
