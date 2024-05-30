from unittest import main, TestCase
from unittest.mock import patch

from tiruka_fib_py.fib_calcs.fib_numbers import calculate_numbers


class TestFibNumbers(TestCase):
    @patch("tiruka_fib_py.fib_calcs.fib_numbers." "rec_fibonacci_numbers")
    def test_calculate_numbers(self, mock_fib_calc):
        expected_outcome = [mock_fib_calc.return_value, mock_fib_calc.return_value]
        self.assertEqual(expected_outcome, calculate_numbers(numbers=[3, 4]))

        self.assertEqual(2, len(mock_fib_calc.call_args_list))

    def test_functional(self):
        self.assertEqual([2, 3, 5], calculate_numbers(numbers=[3, 4, 5]))


if __name__ == "__main__":
    main()
