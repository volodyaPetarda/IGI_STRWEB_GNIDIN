from utils import input_int, input_float


def solve():
    '''
    function to solve the task, that finds the index of the maximum absolute value element in an array and the sum of elements after the first positive element
    :return:
    '''
    n = input_int("Введите количество элементов в массиве: ")
    array = [(input_float(f"Введите элемент {i + 1}: ")) for i in range(n)]
    max_abs_ind = max(range(n), key=lambda i: abs(array[i]))
    sum_after_first_positive = sum(array[next((i for i in range(n) if array[i] > 0), n) + 1:])
    print(f"Индекс максимального по модулю элемента: {max_abs_ind}")
    print(f"Сумма элементов после первого положительного: {sum_after_first_positive}")

if __name__ == '__main__':
    solve()
