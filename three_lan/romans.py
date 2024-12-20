def integer_to_roman(number):
    values = [
        (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
        (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")
    ]
    result = ""
    for value, symbol in values:
        while number >= value:
            result += symbol
            number -= value
    return result

if __name__ == "__main__":
    import sys
    for line in sys.stdin:
        try:
            number = int(line.strip())
            if 1 <= number <= 100:
                print(integer_to_roman(number))
            else:
                continue
        except ValueError:
            continue
