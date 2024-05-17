"""
Tests de pruebas
"""
from django.test import SimpleTestCase
from app import calc


class CalcTest(SimpleTestCase):
    """
    Usamos la clase mas sencilla para comprobar calc.
    """
    def test_add_numbers(self):
        """ testeamos la suma"""
        res = calc.add(5,6)

        self.assertEqual(res, 12)