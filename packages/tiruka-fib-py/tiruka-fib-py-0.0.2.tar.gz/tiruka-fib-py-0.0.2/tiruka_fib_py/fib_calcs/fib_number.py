def rec_fibonacci_numbers(number: int) -> int:
    if number < 0:
        raise ValueError("Number must be a non-negative integer")
    if number <= 1:
        return number
    return rec_fibonacci_numbers(number - 1) + rec_fibonacci_numbers(number - 2)
