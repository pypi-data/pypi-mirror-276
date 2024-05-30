from .fib_number import rec_fibonacci_numbers


def calculate_numbers(numbers: list[int]) -> list[int]:
    return [rec_fibonacci_numbers(number) for number in numbers]
