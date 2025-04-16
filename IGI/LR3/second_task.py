from IGI.LR3.utils import input_int


def solve():
    '''
    Enter integers until 0 is entered. Then, output the arithmetic mean of all the numbers entered.
    '''
    numbers = []
    while True:
        value = input_int("Введите целое число (0 для выхода): ")
        if value == 0:
            break

        numbers.append(value)
    if numbers:
        average = sum(numbers) / len(numbers)
        print(f"Среднее арифметическое: {average}")
    else:
        print("Не введено ни одного числа.")


if __name__ == '__main__':
    solve()
