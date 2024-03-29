import time
import unittest

from main import ExpHelper


class LearningCase(unittest.TestCase):

    def test_0(self):
        settings = {'a': [1, 2, 3], 'b': ['hu', 'hi', 'ho']}
        e = ExpHelper(name='e0', settings=settings)
        f = lambda a: (a ** 2)
        e.parallelize(f, ['a'])
        self.assertEqual(1, 1)

    def test_1(self):
        settings = {'a': [1, 2, 3], 'b': ['hu', 'hi', 'ho']}
        e = ExpHelper(name='e0', settings=settings)
        f = lambda a, b: (a, b)
        e.parallelize(f, ['a', 'b'])
        self.assertEqual(1, 1)

    def test_2(self):
        settings = {'a': [1, 2, 3], 'b': ['hu', 'hi', 'ho']}
        e = ExpHelper(name='e0', settings=settings)
        f = lambda a, b: (a, b)
        self.assertRaises(AssertionError, e.parallelize, f, ['a', 'c'])

    def test_3(self):
        settings = {'a': [1, 2, 3], 'b': ['hu', 'hi', 'ho']}
        e = ExpHelper(name='e0', settings=settings)
        e.do_or_load('data_store', ['a', 'b'], lambda a, b: str(a) + b, {'a': 1, 'b': 'hu'})

    def test_4(self):
        settings = {'a': [1, 2, 3], 'b': ['hu', 'hi', 'ho']}
        e = ExpHelper(name='e0', settings=settings)

        def f(a, b):
            def func_expensive(a, b):
                time.sleep(1)
                return str(a) + str(b)
            return e.do_or_load('data_store', ['a', 'b'], func_expensive, {'a': a, 'b': b})

        res = e.parallelize(f, ['a', 'b'])
        self.assertEqual(res, ['1hu', '1hi', '1ho', '2hu', '2hi', '2ho', '3hu', '3hi', '3ho'])


def main():
    unittest.main()


if __name__ == "__main__":
    main()
