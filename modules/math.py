def sum_of_digits(number: int) -> int:
    digit_sum = 0
    for digit in str(number):
        digit_sum += int(digit)
    return digit_sum


def sum_of_digits_reduced(number: int) -> int:
    digit_sum = sum_of_digits(number)
    while digit_sum>9:
        digit_sum = sum_of_digits(digit_sum)
    return digit_sum
