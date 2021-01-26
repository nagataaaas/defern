import unittest

from defern import defern, deferner, defern_this, here


class TestDefern(unittest.TestCase):

    @staticmethod
    def _test_func_1(result):
        result.append(1)

        defern(result.append, 3)
        defern(lambda: result.append(4))

        @defern_this
        def append_5():
            result.append(5)

        @deferner
        def append_num(num):
            result.append(num)

        append_num(6)

        result.append(2)

    def test_core(self):
        result = []

        self._test_func_1(result)
        self.assertEqual(result, [1, 2, 3, 4, 5, 6])

if __name__ == '__main__':
    unittest.main()