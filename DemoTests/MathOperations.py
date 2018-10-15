import TestCase


class Sums(TestCase.TestCase):

    def test_sum_one(self):
        """2 equals 1 + 1"""
        assert 2 == 1 + 1

    def test_sum_two(self):
        """20 equals 9 + 9"""
        assert 20 == 9 + 9

    def test_sum_three(self):
        """18 equals 9 + 9"""
        assert 18 == 9 + 9

    def test_sum_four(self):
        "1 equals 0 + 1.0"
        assert 1 == 0 + 1.0

class Multiply(TestCase.TestCase):

    def test_one(self):
        """ 20 divided by 0 """
        a = 20 / 0

