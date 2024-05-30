import argparse
from tiruka_fib_py.fib_calcs.fib_number import rec_fibonacci_numbers


def fib_numb() -> None:
    parser = argparse.ArgumentParser(description="Calculate Fibonacci numbers")
    parser.add_argument(
        "--number",
        action="store",
        type=int,
        required=True,
        help="Fibonacci number to be calculated",
    )
    args = parser.parse_args()
    print(f"Your Fibonacci number is: {rec_fibonacci_numbers(number=args.number)}")
