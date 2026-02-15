import unittest
from decimal import Decimal

from arrendatools.rent_update.base import (
    RentUpdateInput,
    RentUpdateMethod,
    RentUpdateResult,
)
from arrendatools.rent_update.factory import RentUpdateFactory


class TestRentUpdateFactory(unittest.TestCase):
    class CustomUpdate(RentUpdateMethod):
        def calculate(self, inputs: RentUpdateInput) -> RentUpdateResult:
            return RentUpdateResult(
                amount=inputs.amount,
                updated_amount=inputs.amount,
            )

    def test_create_unknown_type_raises(self):
        with self.assertRaises(ValueError) as context:
            RentUpdateFactory.create("unknown")
        self.assertIn("Unknown update type", str(context.exception))

    def test_register_custom_strategy(self):
        RentUpdateFactory.register("custom", self.CustomUpdate)
        instance = RentUpdateFactory.create("custom")
        result = instance.calculate(RentUpdateInput(amount=Decimal("10.00")))
        expected = RentUpdateResult(
            amount=Decimal("10.00"),
            updated_amount=Decimal("10.00"),
        )
        self.assertEqual(result, expected)

    def test_create_ipc_then_percentage_builtin(self):
        instance = RentUpdateFactory.create("ipc_then_percentage")
        self.assertIsInstance(instance, RentUpdateMethod)


if __name__ == "__main__":
    unittest.main()
