import unittest
from dt_utils.parsers import T
from dt_utils.format import *

import numpy as np


class TestFormat(unittest.TestCase):
    def test_minimal_timestr(self):
        self.assertEqual(minimal_timestr(T(202305010000)), '20230501')
        self.assertEqual(minimal_timestr(T(202305010800)), '2023050108')
        self.assertEqual(minimal_timestr(T(20240601231500)), '202406012315')
        self.assertEqual(minimal_timestr(T(20240601231523)), '20240601231523')
        self.assertEqual(minimal_timestr('202301031200'), '2023010312')
        self.assertEqual(minimal_timestr(None), None)

        self.assertListEqual(minimal_timestr(['202301', '2023021500']), ['20230101', '20230215'])
        arr_result = minimal_timestr(np.array(['202301', '2023021500']))
        self.assertIsInstance(arr_result, np.ndarray)
        self.assertListEqual(list(arr_result), ['20230101', '20230215'])


if __name__ == '__main__':
    unittest.main()
