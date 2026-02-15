import unittest

from arrendatools.rent_update.date_utils import DateUtils


class TestDateUtils(unittest.TestCase):
    def test_month_name_es_first_month(self):
        self.assertEqual(DateUtils.month_name_es(1), "enero")

    def test_month_name_es_last_month(self):
        self.assertEqual(DateUtils.month_name_es(12), "diciembre")

    def test_month_name_es_invalid_low(self):
        with self.assertRaises(ValueError) as context:
            DateUtils.month_name_es(0)
        self.assertEqual(
            str(context.exception),
            "Month 0 is invalid. It must be between 1 and 12.",
        )

    def test_month_name_es_invalid_high(self):
        with self.assertRaises(ValueError) as context:
            DateUtils.month_name_es(13)
        self.assertEqual(
            str(context.exception),
            "Month 13 is invalid. It must be between 1 and 12.",
        )


if __name__ == "__main__":
    unittest.main()
