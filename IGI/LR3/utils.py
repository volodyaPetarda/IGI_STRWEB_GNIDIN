def input_int(message = "Enter an integer: "):
    '''
    Function to input an integer.
    :param message:
    :return:
    '''
    while True:
        try:
            return int(input(message))
        except ValueError:
            print("Invalid input. Please enter an integer.")

def input_float(message = "Enter a float: "):
    '''
    Function to input a float.
    :param message:
    :return:
    '''
    while True:
        try:
            return float(input(message))
        except ValueError:
            print("Invalid input. Please enter a float.")

def input_str(message = "Enter a string: "):
    '''
    Function to input a string.
    :param message:
    :return:
    '''
    while True:
        try:
            return str(input(message))
        except ValueError:
            print("Invalid input. Please enter a string.")
