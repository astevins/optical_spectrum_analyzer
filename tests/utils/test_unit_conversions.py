import unittest

from osa.utils.unit_conversions import *


class UnitConversionTests(unittest.TestCase):
    def test_m_to_nm(self):
        m = 1.342
        self.assertEqual(1.342e+9, m_to_nm(m))

    def test_small_m_to_nm(self):
        m = 0.00000000481
        self.assertEqual(4.81, m_to_nm(m))

    def test_nm_to_m(self):
        nm = 9214
        self.assertEqual(9.214e-6, nm_to_m(nm))

    def test_wavelength_to_frequency(self):
        wavelength_nm = 1550
        self.assertAlmostEqual(193.414489, wavelength_to_frequency(wavelength_nm))


if __name__ == "__main__":
    unittest.main()
