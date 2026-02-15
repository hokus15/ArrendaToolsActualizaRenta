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

    class _DummyEntryPoints:
        def __init__(self, entries):
            self._entries = entries

        def select(self, group):
            if group == "arrendatools.rent_update":
                return self._entries
            return []

    class _DummyEntryPoint:
        def __init__(self, name, klass):
            self.name = name
            self._klass = klass

        def load(self):
            return self._klass

    def setUp(self):
        self._registry = RentUpdateFactory._registry.copy()
        self._entry_points_loaded = RentUpdateFactory._entry_points_loaded
        self._builtins_loaded = RentUpdateFactory._builtins_loaded

    def tearDown(self):
        RentUpdateFactory._registry = self._registry
        RentUpdateFactory._entry_points_loaded = self._entry_points_loaded
        RentUpdateFactory._builtins_loaded = self._builtins_loaded

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

    def test_load_entry_points_select(self):
        entry_point = self._DummyEntryPoint("custom_ep", self.CustomUpdate)
        dummy_entry_points = self._DummyEntryPoints([entry_point])

        RentUpdateFactory._registry = {}
        RentUpdateFactory._entry_points_loaded = False
        RentUpdateFactory._builtins_loaded = True

        with unittest.mock.patch(
            "arrendatools.rent_update.factory.metadata.entry_points",
            return_value=dummy_entry_points,
        ):
            RentUpdateFactory._load_entry_points()

        instance = RentUpdateFactory.create("custom_ep")
        self.assertIsInstance(instance, RentUpdateMethod)

    def test_load_entry_points_fallback(self):
        entry_point = self._DummyEntryPoint("custom_ep", self.CustomUpdate)

        RentUpdateFactory._registry = {}
        RentUpdateFactory._entry_points_loaded = False
        RentUpdateFactory._builtins_loaded = True

        class _FallbackEntryPoints:
            def get(self, group, default=None):
                if group == "arrendatools.rent_update":
                    return [entry_point]
                return default or []

        with unittest.mock.patch(
            "arrendatools.rent_update.factory.metadata.entry_points",
            return_value=_FallbackEntryPoints(),
        ):
            RentUpdateFactory._load_entry_points()

        instance = RentUpdateFactory.create("custom_ep")
        self.assertIsInstance(instance, RentUpdateMethod)


if __name__ == "__main__":
    unittest.main()
