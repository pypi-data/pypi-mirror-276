from unittest import main, TestCase
from tiruka_fib_py.fib_calcs.fib_number import rec_fibonacci_numbers


class TestRecFibNumber(TestCase):
    def test_zero(self):
        self.assertEqual(0, rec_fibonacci_numbers(0))

    def test_negative(self):
        with self.assertRaises(ValueError) as raised_exception:
            rec_fibonacci_numbers(-1)
        self.assertEqual(
            "Number must be a non-negative integer", str(raised_exception.exception)
        )

    def test_one(self):
        self.assertEqual(1, rec_fibonacci_numbers(1))

    def test_two(self):
        self.assertEqual(1, rec_fibonacci_numbers(2))

    def test_twenty(self):
        self.assertEqual(6765, rec_fibonacci_numbers(20))


if __name__ == "__main__":
    main()
