import unittest

import data.curve as curve

class TestCurveFunctions(unittest.TestCase):
    def test_get_bond_curve(self):
        curve_data = curve.get_bond_curve("CN_TREAS_STD", '2024-05-27 00:00:00', '2024-05-27 18:00:00', '1m')
        if curve_data is not None:
            for data in curve_data:
                print(data)
        else:
            print(curve_data)

    def test_get_credit_curve(self):
        curve_data = curve.get_credit_curve("CN_RAILWAY_SPRD_STD", '2024-05-27 00:00:00', '2024-05-27 18:00:00',
                                            '1m')
        if curve_data is not None:
            for data in curve_data:
                print(data)
        else:
            print(curve_data)

    def test_get_ir_curve(self):
        curve_data = curve.get_ir_curve("CNY_FR_007", '2024-05-22 00:00:00', '2024-05-27 18:00:00', '1d')
        if curve_data is not None:
            for data in curve_data:
                print(data)
        else:
            print(curve_data)
