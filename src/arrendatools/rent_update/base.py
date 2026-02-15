from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal
from typing import Optional


@dataclass(frozen=True)
class RentUpdateInput:
    amount: Decimal
    data: Optional[Decimal] = None
    month: Optional[int] = None
    year_start: Optional[int] = None
    year_end: Optional[int] = None

    def __post_init__(self) -> None:
        if not isinstance(self.amount, Decimal):
            raise ValueError("Amount must be Decimal.")
        if self.data is not None and not isinstance(self.data, Decimal):
            raise ValueError("Data must be Decimal.")
        if self.month is not None and (
            not isinstance(self.month, int) or self.month < 1 or self.month > 12
        ):
            raise ValueError("Month must be between 1 and 12.")
        if self.year_start is not None and not isinstance(self.year_start, int):
            raise ValueError("Year start must be int.")
        if self.year_end is not None and not isinstance(self.year_end, int):
            raise ValueError("Year end must be int.")
        if self.year_start is not None and self.year_end is not None:
            if self.year_end < self.year_start:
                raise ValueError("Year end cannot be earlier than year start.")


@dataclass(frozen=True)
class RentUpdateResult:
    amount: Decimal
    updated_amount: Decimal
    data: Optional[Decimal] = None
    variation_rate: Optional[Decimal] = None
    month: Optional[str] = None
    year_start: Optional[int] = None
    year_end: Optional[int] = None
    index_start: Optional[Decimal] = None
    index_end: Optional[Decimal] = None

    def as_dict(self, include_none: bool = False) -> dict:
        result = {
            "amount": self.amount,
            "updated_amount": self.updated_amount,
            "data": self.data,
            "variation_rate": self.variation_rate,
            "month": self.month,
            "year_start": self.year_start,
            "year_end": self.year_end,
            "index_start": self.index_start,
            "index_end": self.index_end,
        }
        if include_none:
            return result
        return {key: value for key, value in result.items() if value is not None}


class RentUpdateMethod(ABC):
    """Clase base abstracta para las actualizaciones de renta."""

    @abstractmethod
    def calculate(
        self,
        inputs: RentUpdateInput,
    ) -> RentUpdateResult:
        """Calcula la actualizacion de la renta."""
        raise NotImplementedError
