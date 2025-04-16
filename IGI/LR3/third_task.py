from utils import input_str

def solve():
    '''
    Count the number of non-space characters in a line entered from the keyboard.
    '''
    string = input_str("Введите строку: ")
    answer = len(string) - string.count(" ")
    print(f"Количество символов, отличных от пробельных: {answer}")

if __name__ == '__main__':
    solve()
