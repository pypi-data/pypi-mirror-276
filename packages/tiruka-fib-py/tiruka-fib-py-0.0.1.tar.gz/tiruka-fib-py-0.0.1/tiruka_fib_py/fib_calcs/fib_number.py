from typing import Optional


def rec_fibonacci_numbers(number: int) -> Optional[str]:
    if number < 0:
        return None
    if number <= 1:
        return number
    return rec_fibonacci_numbers(number - 1) + rec_fibonacci_numbers(number - 2)
